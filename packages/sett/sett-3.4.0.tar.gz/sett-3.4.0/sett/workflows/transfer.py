import json
import os
import re
import time
from typing import List, Tuple, Dict, Optional

from .encrypt import DATE_FMT_FILENAME
from ..utils.config import Config
from ..utils.log import create_logger, log_runtime_info, log_timing
from ..utils.progress import ProgressInterface
from ..core.crypt import get_recipient_email, retrieve_refresh_and_validate_keys, gpg
from ..core.archive import check_package, extract, METADATA_FILE, DATA_FILE_ENCRYPTED
from ..core.metadata import load_metadata
from ..core.error import UserError
from ..protocols import Protocol


logger = create_logger(__name__)


@log_timing(logger)
@log_runtime_info(logger)
def transfer(
    files: List[str],
    *,
    protocol: Protocol,
    config: Config,
    dry_run: bool = False,
    verify_dtr: Optional[bool] = None,
    progress: ProgressInterface = None,
):
    """Transfer file(s) to the selected recipient on the BiomedIT network."""

    logger.info(
        "File(s) to transfer: [%s]%s",
        ", ".join(files),
        " (dry_run)" if dry_run else "",
    )

    with logger.log_task("Input data check"):
        for archive_path in files:
            check_package(archive_path)

    files_by_recipient: Dict[Tuple[gpg.Key, ...], List[str]] = {}
    with logger.log_task("Extracting destination for each package"):
        for archive_path in files:
            logger.info("Processing: %s", archive_path)
            with extract(archive_path, METADATA_FILE, DATA_FILE_ENCRYPTED) as (
                metadata,
                encrypted_file,
            ):
                metadata = json.load(metadata)
                keys = tuple(
                    retrieve_refresh_and_validate_keys(
                        key_search_terms=gpg.extract_key_id(encrypted_file),
                        gpg_store=config.gpg_store,
                        key_authority_fingerprint=config.key_authority_fingerprint,
                        keyserver_url=config.keyserver_url,
                        allow_key_download=config.allow_gpg_key_autodownload,
                    )
                )
            metadata = load_metadata(metadata)
            if verify_dtr is None:
                verify_dtr = metadata.transfer_id is not None
            if verify_dtr:
                if metadata.transfer_id is None:
                    raise UserError(
                        "DTR (Data Transfer Request) ID is missing in file metadata."
                    )

                try:
                    project_code = config.portal_api.verify_transfer(
                        metadata=metadata, filename=archive_path
                    )
                    logger.info(
                        "DTR ID '%s' is valid for project '%s'",
                        metadata.transfer_id,
                        project_code,
                    )
                except RuntimeError as e:
                    raise UserError(format(e)) from e

            if config.verify_package_name:
                check_archive_name_follows_convention(
                    archive_path=archive_path,
                    project_code=project_code if verify_dtr else None,
                    package_name_suffix=config.package_name_suffix,
                )
            files_by_recipient.setdefault(keys, []).append(archive_path)

    if dry_run:
        logger.info("Dry run completed successfully")
        return

    for recipient_keys, r_files in files_by_recipient.items():
        emails = [get_recipient_email(k) for k in recipient_keys]
        if hasattr(protocol, "recipients"):
            setattr(protocol, "recipients", emails)
        if hasattr(protocol, "pkey_password_encoding"):
            setattr(protocol, "pkey_password_encoding", config.ssh_password_encoding)
        with logger.log_task(
            "Transferring files encrypted for " f"{', '.join(emails)}"
        ):
            protocol.upload(r_files, progress=progress)


def check_archive_name_follows_convention(
    archive_path: str,
    project_code: Optional[str],
    package_name_suffix: Optional[str],
) -> None:
    """Verify that the given archive_path file name follows the naming
    convention for data packages:

        <project_code>_<date_format>_<package_name_suffix>.zip

    Raises an error if the file name does not match the convention.
    """

    def join_strings(*args: Optional[str]) -> str:
        return "_".join(filter(None, args))

    error_msg = (
        f"File {archive_path} does not follow the standard data package "
        "naming convention: '"
        f"{join_strings(project_code, DATE_FMT_FILENAME, package_name_suffix)}"
        ".zip/.tar'. Please make sure that the file name does not contain "
        "any confidential information. "
        "To resolve this error, either modify the name of the file to "
        "match the naming convention, or disable the 'verify_package_name'"
        "option in the settings of the configuration file."
    )

    # Capture the date+time part of the archive file using a regexp.
    m = re.fullmatch(
        join_strings(project_code, r"(?P<ts>\S+?)", package_name_suffix)
        + r"\.(zip|tar)",
        os.path.basename(archive_path),
    )

    # Testing for the length of the date+time string is needed because
    # strftime() does support incomplete strings: e.g. "20210908T140302"
    # and "202198T1432" are both converted to the same date and time.
    if m is None or len(m.group("ts")) != len(
        time.strftime(DATE_FMT_FILENAME, time.localtime())
    ):
        raise UserError(error_msg)

    # Try to do a string-to-time conversion: failure indicates that the
    # captured group does not follow the date format specifications, or
    # that some additional, unexpected, text is in the archive name.
    try:
        time.strptime(m.group("ts"), DATE_FMT_FILENAME)
    except ValueError:
        raise UserError(error_msg) from None
