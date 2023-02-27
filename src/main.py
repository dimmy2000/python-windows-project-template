# Standard Library
import zipfile

# Local Modules
from src.constants import (
    DEBUG,
    LOG_FILE_NAME,
    LOGS_FOLDER,
    PROJECT_AUTHOR,
    PROJECT_FOLDER,
    PROJECT_NAME,
    PROJECT_VERSION,
)
from src.loggers import logger
from src.utils import send_email


def start_action():
    try:
        logger.start_msg()
        logger.info(f"{PROJECT_NAME} version {PROJECT_VERSION} by {PROJECT_AUTHOR}")
        logger.info(f"{PROJECT_FOLDER=}")
        logger.finish_msg()
    except Exception:
        logger.exception("An error has occurred")
    finally:
        if not DEBUG:
            zip_file = PROJECT_FOLDER / "logs.zip"
            subject = LOG_FILE_NAME.stem
            with zipfile.ZipFile(zip_file, "w") as zip_archive:
                for file in LOGS_FOLDER.glob("*"):
                    zip_archive.write(filename=file, arcname=file.name)
            send_email(
                addrs=PROJECT_AUTHOR,
                subject=subject,
                attachment=str(zip_file),
            )
            zip_file.unlink(missing_ok=True)
