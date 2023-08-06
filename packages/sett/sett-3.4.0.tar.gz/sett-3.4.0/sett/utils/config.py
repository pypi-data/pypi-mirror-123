import os
import platform
import json
import dataclasses
import warnings
import enum
from dataclasses import dataclass, field as _field, fields
from pathlib import Path
from typing import Tuple, Dict, Any, Optional, Callable

import gpg_lite as gpg
from libbiomedit.lib.deserialize import deserialize, serialize

from .validation import REGEX_URL, PACKAGE_SUFFIX
from .log import get_default_log_dir, create_logger
from ..core.error import UserError
from ..core.portal_api import PortalApi
from .. import APP_NAME_SHORT


CONFIG_FILE_NAME = "config.json"
CONFIG_FILE_ENVIRON_VAR = "SETT_CONFIG_FILE"

conf_sub_dir_by_os: Dict[str, Tuple[str, ...]] = {
    "Linux": (".config",),
    "Darwin": (".config",),
    "Windows": ("AppData", "Roaming"),
}

logger = create_logger(__name__)


@dataclass(frozen=True)
class Connection:
    """dataclass holding config of a connection (sftp / liquid files)"""

    protocol: str
    parameters: Dict[str, Any]


class FileType(enum.Enum):
    file = enum.auto()
    directory = enum.auto()


@dataclass
class FieldMetadata:
    description: Optional[str]
    label: Optional[str]
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    file_type: Optional[FileType] = None
    regex: Optional[str] = None


def reverse_expanduser(path: str) -> str:
    """Performs the reverse operation of os.path.expanduser(). It checks
    whether a path starts with a user's home directory, and if so, changes
    it to the "~" shortcut. It also removes any trailing path separator.

    Example:
      * On linux  : /home/user/foo/bar/ -> ~/foo/bar
      * On windows: /home/user/foo/bar/ -> ~\\foo\\bar
    """
    path_as_posix = Path(path).as_posix()
    home_as_posix = Path.home().as_posix()
    if path_as_posix.startswith(home_as_posix):
        return str(Path("~" + path_as_posix[len(home_as_posix) :]))

    # Note: conversion to Path and back is to remove trailing path separators.
    return str(Path(path))


def reverse_expanduser_if_path_exists(path: Optional[str]) -> Optional[str]:
    return reverse_expanduser(path) if path else path


def field_ext(
    serializer: Optional[Callable] = None,
    deserializer: Optional[Callable] = None,
    **kwargs,
):
    field_names = {f.name for f in fields(FieldMetadata)}
    field_kwargs = {key: val for key, val in kwargs.items() if key not in field_names}
    metadata = {
        key: val
        for key, val in kwargs.items()
        if key not in field_kwargs and val is not None
    }
    if metadata:
        # The dataclasses doc specifies, that metadata should be a mapping.
        # Therefore we wrap our dataclass in a dict:
        field_kwargs["metadata"] = {"metadata": FieldMetadata(**metadata)}
        if serializer:
            field_kwargs["metadata"]["serialize"] = serializer
        if deserializer:
            field_kwargs["metadata"]["deserialize"] = deserializer
    return _field(**field_kwargs)


LABEL_COMPRESSION_LEVEL = "Compression level"
DESCRIPTION_COMPRESSION_LEVEL = (
    "Compression level used in data encryption, from 0 (no compression) to "
    "9 (highest). Higher compression levels require more computing time."
)


@dataclass
class Config:
    """dataclass holding config data"""

    dcc_portal_url: str = field_ext(
        default="https://portal.dcc.sib.swiss",
        label="DCC portal URL",
        description="URL of portal instance. The portal is used for key signing and "
        "DTR (Data Transfer Request) validation.",
        regex=REGEX_URL,
    )
    keyserver_url: Optional[str] = field_ext(
        default="keyserver.dcc.sib.swiss",
        label="Keyserver URL",
        description="URL of the keyserver: used for publishing/fetching public PGP keys.",
        # no validation, as specifying http:// is optional
    )
    gpg_home_dir: str = field_ext(
        serializer=reverse_expanduser_if_path_exists,
        deserializer=os.path.expanduser,
        default=gpg.get_default_gnupg_home_dir(),
        label="GPG home directory",
        description="Path of the directory where GnuPG stores its keyrings and "
        "configuration files.",
        file_type=FileType.directory,
    )
    key_authority_fingerprint: Optional[str] = field_ext(
        default="B37CE2A101EBFA70941DF885881685B5EE0FCBD3",
        label="Key validation authority fingerprint",
        description="Fingerprint (40 characters) of the key validation authority's "
        "PGP key. If a value is specified, only keys signed the "
        "authority's key can be used.",
    )
    sign_encrypted_data: bool = field_ext(
        default=True,
        label="Sign encrypted data",
        description="Whether encrypted data should be signed with sender's key.",
    )
    always_trust_recipient_key: bool = field_ext(
        default=True,
        label="Always trust recipient key",
        description="If unchecked, the encryption key must be signed by the local user.",
    )
    repo_url: str = field_ext(
        default="https://pypi.org",
        label="Repo URL",
        description="Python package repository, used when looking for updates.",
        regex=REGEX_URL,
    )
    check_version: bool = field_ext(
        default=True,
        label="Check version",
        description="Check whether you have the latest version of sett on startup.",
    )
    offline: bool = field_ext(
        default=False,
        label="Offline mode",
        description="In offline mode, sett will not make any network connections: "
        "DTR verification and automatic PGP key downloading/updating is disabled.",
    )
    log_dir: str = field_ext(
        serializer=reverse_expanduser_if_path_exists,
        deserializer=os.path.expanduser,
        default=get_default_log_dir(),
        label="Log directory",
        description="Path to log files directory.",
        file_type=FileType.directory,
    )
    error_reports: bool = field_ext(
        default=True,
        label="Create error reports",
        description="Write an error report if some error happens.",
    )
    log_max_file_number: int = field_ext(
        default=1000,
        label="Log max. file number",
        description="Maximum number of logfiles to keep as backup. Set to 0 to disable logging.",
        minimum=0,
    )
    connections: Dict[str, Connection] = _field(default_factory=dict)
    output_dir: Optional[str] = field_ext(
        serializer=reverse_expanduser_if_path_exists,
        deserializer=os.path.expanduser,
        default=None,
        label="Output directory",
        description="Default output directory, relevant for encryption/decryption.",
        file_type=FileType.directory,
    )
    ssh_password_encoding: str = field_ext(
        default="utf_8",
        label="SSH password encoding",
        description="Character encoding used for the SSH key password.",
    )
    default_sender: Optional[str] = field_ext(
        default=None,
        label="Default sender",
        description="Default sender fingerprint for encryption.",
    )
    gui_quit_confirmation: bool = field_ext(
        default=True,
        label="Quit confirmation",
        description="Ask for confirmation before closing the application.",
    )
    compression_level: int = field_ext(
        default=5,
        label=LABEL_COMPRESSION_LEVEL,
        description=DESCRIPTION_COMPRESSION_LEVEL,
        minimum=0,
        maximum=9,
    )
    package_name_suffix: Optional[str] = field_ext(
        default=None,
        label="Default package suffix",
        description="Default suffix for encrypted package name",
        regex=PACKAGE_SUFFIX,
    )
    max_cpu: int = field_ext(
        default=0,
        label="Max CPU",
        description="Maximum number of CPU cores for parallel computation (use all CPU cores if value equals 0)",
        minimum=0,
        maximum=os.cpu_count()
        or 4,  # In case cpu_count fails to detect the number of available cores
        # use a reasonable default
    )
    gpg_key_autodownload: bool = field_ext(
        default=True,
        label="Allow PGP key auto-download",
        description="Allow the automatic download and refresh of PGP keys from the Keyserver.",
    )

    verify_package_name: bool = field_ext(
        default=True,
        label="Verify package name",
        description="Verify that the name of data packages follows the "
        f"{APP_NAME_SHORT} naming convention",
    )

    def __post_init__(self):
        for url in ("dcc_portal_url", "repo_url"):
            setattr(
                self, url, getattr(self, url).rstrip("/")  # pylint: disable=no-member
            )

    @property
    def portal_api(self):
        return PortalApi(self.dcc_portal_url)

    @property
    def gpg_store(self):
        return open_gpg_dir(self.gpg_home_dir)

    @property
    def allow_gpg_key_autodownload(self) -> bool:
        """Property indicating whether GPG keys can be automatically downloaded
        and refreshed from a keyserver, if a keyserver is specified.
        Key auto-download is not allowed in the following situations:
         * There is no defined validation authority. If keys do not need to be
           certified by a central key authority, auto-downloading them presents
           a security risk (keys should be manually downloaded and checked) and
           is therefore not allowed.
         * The 'offline' mode is activated, no network access is allowed.
         * The user has decided to not allow it.
        """
        return (
            self.key_authority_fingerprint is not None
            and not self.offline
            and self.gpg_key_autodownload
        )


class ConnectionStore:
    """Connection configuration storage manager"""

    config_field_name = "connections"

    def __init__(self, config_path: Optional[str] = None):
        self.path = get_config_file() if config_path is None else config_path

    def _read(self) -> dict:
        """Load data from config file"""
        try:
            with open(self.path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _write(self, data: dict):
        """Write data to config file"""
        save_config(data, self.path)

    def save(self, name: str, connection: Connection, exclude_pattern: str = "pass"):
        """Save a new connection to the config file.

        The "exclude_pattern" argument is used to remove all fields whose name
        contain the specified string. The default is "pass", meaning that
        fields named e.g. "password" or "passphrase" will be removed from the
        Connection object before it gets written to a file.

        :param name: name of the new connection.
        :param connection: new connection object to write to the config file.
        :param exclude_pattern: exclude all connection fields containing the
            specified pattern.
        """
        # Load entire sett configuration file data as a dict. It might or might
        # not already contain a "connections" field containing data for one or
        # more connections. If not, an empty "connections" field is added.
        data = self._read()
        connections = data.setdefault(self.config_field_name, {})
        connection_dict = dataclasses.asdict(connection)

        # Note: in principle, the "pkey_password" parameter of a Connection
        # object should not be present anymore at this point, but we
        # nevertheless check to be sure.
        for parameter_to_delete in {
            k for k in connection_dict["parameters"] if exclude_pattern in k
        }:
            del connection_dict["parameters"][parameter_to_delete]

        connections[name] = connection_dict
        self._write(data)

    def delete(self, name: str):
        """Delete a new connection from the config file"""
        data = self._read()
        try:
            data.get(self.config_field_name, {}).pop(name)
            self._write(data)
        except KeyError as e:
            raise UserError(f"Connection '{name}' does not exist.") from e

    def rename(self, old: str, new: str):
        """Rename an existing connection from the config file"""
        data = self._read()
        try:
            connection = data.get(self.config_field_name, {}).pop(old)
            data[self.config_field_name][new] = connection
            self._write(data)
        except KeyError as e:
            raise UserError(f"Connection '{new}' does not exist.") from e


def load_config() -> Config:
    """Loads the config, returning a Config object."""

    # TODO: remove migration (see issue 283)
    migrate_user_config_file()

    cfg_dct = {}
    try:
        cfg_dct = sys_config_dict()
        cfg_dct.update(load_config_dict(get_config_file()))
    except UserError as e:
        warnings.warn(format(e))

    return deserialize(Config)(cfg_dct)


def save_config(config: dict, path: Optional[str] = None) -> str:
    """Save config to a file.
    :return: path of the created config file.
    """
    config_file = Path(get_config_file() if path is None else path)
    if not config_file.parent.is_dir():
        config_file.parent.mkdir(parents=True)

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, sort_keys=True)

    return config_file.as_posix()


def create_config() -> str:
    """Creates a new config file in the home directory's config folder
    :return: path of the created config file.
    """
    return save_config(config_to_dict(default_config()))


def config_to_dict(config: Config) -> dict:
    """Converts a Config object into a dict."""
    return serialize(Config)(config)


def default_config() -> Config:
    """Creates a new Config object with default values."""
    return deserialize(Config)(sys_config_dict())


def sys_config_dict() -> dict:
    """On linux only: try to load global sys config. If the env variable
    SYSCONFIG is set search there, else in /etc/{APP_NAME_SHORT}.
    """
    if platform.system() == "Linux":
        sys_cfg_dir = os.environ.get("SYSCONFIG", os.path.join("/etc", APP_NAME_SHORT))
        return load_config_dict(os.path.join(sys_cfg_dir, CONFIG_FILE_NAME))
    return {}


def load_config_dict(path: str) -> dict:
    """Load raw config as a dict."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError as e:
        raise UserError(f"Failed to load configuration from '{path}'. {e}") from e


def get_config_file() -> str:
    """Retrieve the platform-specific path of the config file. If the user has
    the correct config file path environmental variable defined in their
    current environment, this file gets used instead.

    :return: path of the config.
    :raises UserError:
    """
    # Case 1: a config file path environmental variable is defined.
    if CONFIG_FILE_ENVIRON_VAR in os.environ:
        config_file = os.environ[CONFIG_FILE_ENVIRON_VAR]
        if os.path.isdir(config_file):
            raise UserError(
                f"Environmental variable {CONFIG_FILE_ENVIRON_VAR} "
                f"must point to a file, not a directory "
                f"[{config_file}]."
            )
        return config_file

    # Case 2: use the default platform-specific config file.
    return os.path.join(get_config_dir(), CONFIG_FILE_NAME)


def get_config_dir() -> str:
    """Return platform specific default config direcory."""
    return os.path.join(
        os.path.expanduser("~"), *conf_sub_dir_by_os[platform.system()], APP_NAME_SHORT
    )


def open_gpg_dir(gpg_dir: str) -> gpg.GPGStore:
    """Open the database inside a GnuPG directory and return it as a gpg
    object.

    :param gpg_dir: path of the GnuPG directory to open.
    :return: a gpg-lite GPGStore
    :raises UserError:
    """
    if not Path(gpg_dir).is_dir():
        os.makedirs(gpg_dir, mode=0o700)

    try:
        return gpg.GPGStore(gnupg_home_dir=gpg_dir)
    except ValueError:
        raise UserError(f"unable to open GnuPG directory [{gpg_dir}].") from None


def migrate_user_config_file():
    """Temporary migration to auto-update user's config files after arguments
    are modified or deprecated in sett.
    """
    config_file = get_config_file()
    config_needs_update = False

    try:
        config_dict = load_config_dict(config_file)
    except UserError:
        return

    # Migrations to auto-update user's config files after changes from
    # https://gitlab.com/biomedit/sett/-/merge_requests/56
    # Migrations added in June 2021, can be removed after about a year.
    if "gpg_config_dir" in config_dict:
        config_dict["gpg_home_dir"] = config_dict.pop("gpg_config_dir")
        config_needs_update = True

    if "key_validation_authority_keyid" in config_dict:
        fingerprint = Config().key_authority_fingerprint
        key_id = config_dict.pop("key_validation_authority_keyid")
        if key_id == fingerprint[-16:]:
            config_dict["key_authority_fingerprint"] = fingerprint
        else:
            config_dict["key_authority_fingerprint"] = key_id
            warnings.warn(
                f"This new version of {APP_NAME_SHORT} requires the full "
                "fingerprint of the key validation authority. Please update "
                "the 'key_authority_fingerprint' field in your config file: "
                f"{config_file}"
            )

        config_needs_update = True

    # Remove "temp_dir" from config. This is done here rather than in its
    # own migration function to avoid loading/writing the config file twice.
    # Migration added in July 2021, can be removed after about a year.
    if "temp_dir" in config_dict:
        del config_dict["temp_dir"]
        config_needs_update = True

    if "connections" in config_dict:
        for connection in config_dict["connections"].values():
            if "pkey_password" in connection["parameters"]:
                del connection["parameters"]["pkey_password"]
                config_needs_update = True

    if config_needs_update:
        save_config(config_dict, path=config_file)
