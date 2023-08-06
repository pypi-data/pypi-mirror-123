#!/usr/bin/env python3
# The {} placeholders in the docstring are to be replaced with URL_HELP
# and URL_GITLAB_ISSUES whenever the docstring is used.
"""Secure Encryption and Transfer Tool
For detailed documentation see: {}
To report an issue, please use: {}
"""

import os
import json
import shlex
import subprocess  # nosec B404:blacklist import_subprocess
from functools import wraps
from getpass import getpass
from typing import List, Dict, Any, Optional, Callable

from .progress import CliProgress
from .. import VERSION_WITH_DEPS
from ..utils.config import Config, load_config, config_to_dict
from .cli_builder import (
    rename,
    return_to_stdout,
    partial,
    lazy_partial,
    Subcommands,
    Subcommand,
    SubcommandGroup,
    decorate,
)
from ..utils.log import (
    log_to_stream,
    log_to_rotating_file,
    create_logger,
)
from ..utils.error_handling import (
    exit_on_exception,
    log_exceptions,
    error_report_hint_at_exit,
)
from ..workflows.config import create as create_config
from ..workflows.transfer import transfer as workflows_transfer
from ..workflows.decrypt import decrypt as workflows_decrypt
from ..workflows.encrypt import encrypt as workflows_encrypt
from ..workflows.request_sigs import request_sigs
from ..workflows.upload_keys import upload_keys
from ..protocols import Protocol, parse_protocol, __all__ as available_protocols, sftp
from ..core.versioncheck import check_version
from ..core.error import UserError
from ..core.filesystem import OutOfSpaceError
from .. import URL_READTHEDOCS, URL_GITLAB_ISSUES

logger = create_logger(__name__)


def parse_dict(s):
    return json.loads(s)


def parse_protocol_args(s):
    args = parse_dict(s)
    not_provided = object()
    pw = args.get("pkey_password", not_provided)
    if pw is None:  # pw is provided and is None
        args["pkey_password"] = getpass("Please enter your ssh private key password:")
    return args


def two_factor_cli_prompt():
    return input("Verification code: ")


def get_passphrase_from_cmd(passphrase_cmd: str) -> str:
    try:
        # B603:subprocess_without_shell_equals_true
        # Suppress the warning, user can easily execute the same command
        # directly in the shell.
        proc = subprocess.run(  # nosec
            shlex.split(passphrase_cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return proc.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        raise UserError(
            "Failed to read passphrase from "
            f"'{passphrase_cmd}'. "
            f"{e.stderr.decode().strip()}"
        ) from e


def get_passphrase_from_cmd_or_prompt(msg: str, passphrase_cmd: Optional[str]) -> str:
    if passphrase_cmd:
        return get_passphrase_from_cmd(passphrase_cmd)
    return getpass(msg)


@wraps(workflows_encrypt)
def encrypt(
    *args,
    config: Config,
    dry_run: bool,
    passphrase_cmd: Optional[str],
    dtr_id: Optional[int] = None,
    verify_dtr: Optional[bool] = None,
    **kwargs,
):
    if verify_dtr is None:
        verify_dtr = not config.offline and dtr_id is not None
    if config.offline and verify_dtr:
        raise UserError(
            "--verify_dtr is not possible when offline is enabled in the config."
        )
    if config.sign_encrypted_data and not dry_run:
        kwargs["passphrase"] = get_passphrase_from_cmd_or_prompt(
            "Please enter your gpg private key password:", passphrase_cmd
        )
    else:
        kwargs["passphrase"] = None
    try:
        return workflows_encrypt(
            *args,
            dtr_id=dtr_id,
            verify_dtr=verify_dtr,
            config=config,
            dry_run=dry_run,
            **kwargs,
        )
    except OutOfSpaceError as e:
        raise OutOfSpaceError(f"{e} Use --force or -f to ignore this error.") from e


@wraps(workflows_decrypt)
def decrypt(*args, dry_run: bool, passphrase_cmd: Optional[str], **kwargs):
    if dry_run:
        kwargs["passphrase"] = None
    else:
        kwargs["passphrase"] = get_passphrase_from_cmd_or_prompt(
            "Please enter your gpg private key password:", passphrase_cmd
        )
    return workflows_decrypt(*args, dry_run=dry_run, **kwargs)


def transfer(
    files: List[str],
    *,
    connection: str = None,
    two_factor_callback,
    passphrase_cmd: Optional[str] = None,
    config: Config,
    protocol=None,
    protocol_args: Dict[str, Any] = None,
    dry_run: bool = False,
    verify_dtr: Optional[bool] = None,
    progress=None,
):
    if connection is not None:
        if protocol is not None:
            raise UserError(
                "Arguments 'protocol' and 'connection' " "cannot be given together"
            )
        connection_obj = config.connections[connection]
        protocol = parse_protocol(connection_obj.protocol)
        if protocol_args is None:
            protocol_args = {}
        protocol_args = {**connection_obj.parameters, **protocol_args}
    if protocol is None or protocol_args is None:
        raise UserError(
            "Either 'protocol' together with 'protocol_args' "
            "or 'connection' "
            "has to be given as an argument"
        )
    specific_protocol_args = {
        sftp.Protocol: {"two_factor_callback": two_factor_callback}
    }
    try:
        protocol_instance: Protocol = protocol(
            **protocol_args, **specific_protocol_args.get(protocol, {})
        )
    except TypeError as e:
        raise UserError(format(e).replace("__init__", protocol.__module__)) from None
    for pw_arg in protocol_instance.required_password_args():
        if protocol_args.get(pw_arg) is None:
            setattr(
                protocol_instance,
                pw_arg,
                get_passphrase_from_cmd_or_prompt(
                    f"Please enter the password for the argument `{pw_arg}`:",
                    passphrase_cmd,
                ),
            )
    return workflows_transfer(
        files,
        protocol=protocol_instance,
        config=config,
        dry_run=dry_run,
        verify_dtr=verify_dtr,
        progress=progress,
    )


def load_config_check():
    cfg = load_config()
    if not cfg.offline and cfg.check_version:
        check_version(cfg.repo_url)
    return cfg


class Cli(Subcommands):
    description = __doc__.format(URL_READTHEDOCS, URL_GITLAB_ISSUES)
    version = VERSION_WITH_DEPS
    config = load_config_check()
    passphrase_override = dict(
        help="Instead of asking for passphrase, "
        "get it from an external command "
        "(passphrase must be returned to the "
        "standard output).",
        name="passphrase-cmd",
        dest="passphrase_cmd",
    )
    dry_run_override = dict(
        help="Perform checks on the input data, without running the actual command."
    )
    verify_dtr_override = dict(
        help="Verify DTR ID against online database.", default=None
    )
    subcommands = (
        Subcommand(
            decorate(
                encrypt,
                partial(config=config),
                lazy_partial(progress=CliProgress),
            ),
            overrides={
                "files": dict(help="Input file(s) or directories."),
                "sender": dict(
                    help="Fingerprint, key ID or email associated "
                    "with GPG key of data sender.",
                    alias="-s",
                ),
                "recipient": dict(
                    help="Fingerprint, key ID or email associated with "
                    "GPG key of data recipient(s).",
                    alias="-r",
                ),
                "dtr_id": dict(
                    help="Data Transfer Request (DTR) ID (optional).", alias="-t"
                ),
                "verify_dtr": verify_dtr_override,
                "purpose": dict(
                    help="Purpose of the DTR (PRODUCTION, TEST). "
                    "Mandatory only if `transfer_id` is specified."
                ),
                "force": dict(
                    help="Ignore errors about missing disk space", alias="-f"
                ),
                "output": dict(
                    help="Output path (file or directory) to the "
                    "encrypted package. If no path is specified, "
                    "the output package is saved in the current working "
                    "directory. If this argument is missing or path is a "
                    "directory the file name is generated based on the "
                    "current date and an optional suffix.",
                    default=None,
                    alias="-o",
                ),
                "output_suffix": dict(help="Output file name suffix (optional)"),
                "dry_run": dry_run_override,
                "compression_level": dict(
                    help="Compression level for inner tarball in the range "
                    "0 (no compression) to 9 (highest compression). "
                    "Higher compression levels require more computing "
                    "time."
                ),
                "passphrase": passphrase_override,
            },
        ),
        Subcommand(
            decorate(
                transfer,
                partial(config=config, two_factor_callback=two_factor_cli_prompt),
                lazy_partial(progress=CliProgress),
            ),
            overrides={
                "files": dict(help="Path(s) to encrypted package(s)"),
                "protocol": dict(
                    help=f"The protocol for the file transfer."
                    f"Currently available: {', '.join(available_protocols)}",
                    type=parse_protocol,
                    alias="-p",
                ),
                "protocol_args": dict(
                    help="Protocol specific arguments. "
                    "Must be passed as a json string",
                    type=parse_protocol_args,
                ),
                "connection": dict(
                    help="Instead of the option 'protocol', load a connection "
                    "named by the argument of this option to use the "
                    "protocol and protocol args from the config. The "
                    "protocol args can be overwritten by the "
                    "protocol_args option"
                ),
                "passphrase_cmd": dict(help=passphrase_override["help"]),
                "dry_run": dry_run_override,
                "verify_dtr": verify_dtr_override,
            },
        ),
        Subcommand(
            decorate(
                decrypt, partial(config=config), lazy_partial(progress=CliProgress)
            ),
            overrides={
                "files": dict(help="Path(s) to encrypted package(s)"),
                "output_dir": dict(
                    help="Path to the directory where package content is saved after decryption. "
                    "If no path is specified, current working directory is taken.",
                    default=os.getcwd(),
                    alias="-o",
                ),
                "decrypt_only": dict(help="Skip extraction."),
                "dry_run": dry_run_override,
                "passphrase": passphrase_override,
            },
        ),
        SubcommandGroup(
            "config",
            decorate(
                config_to_dict, rename("show"), return_to_stdout, partial(config=config)
            ),
            create_config,
            help="Commands related to config file",
        ),
        Subcommand(
            decorate(request_sigs, partial(config=config)),
            overrides={"key_ids": dict(help="Key ids to request signatures for")},
        ),
        Subcommand(
            decorate(upload_keys, partial(config=config)),
            overrides={"key_ids": dict(help="Key ids to upload")},
        ),
    )


def when(
    condition: bool, decorator: Callable[[Callable], Callable]
) -> Callable[[Callable], Callable]:
    if condition:
        return decorator
    return lambda x: x


log_to_rotating_file(
    log_dir=Cli.config.log_dir, file_max_number=Cli.config.log_max_file_number
)
log_to_stream()


@exit_on_exception
@when(Cli.config.error_reports, error_report_hint_at_exit(Cli.config))
@log_exceptions(logger)
def run():
    if Cli():
        return 0
    return 1


if __name__ == "__main__":
    run()
