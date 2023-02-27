# Standard Library
import os
import sys
from logging import NOTSET, FileHandler, Formatter, Logger, StreamHandler
from pathlib import Path

# Local Modules
from src.constants import BACKUP_COUNT, LOG_FILE_NAME, LOGGING_LEVEL, PROJECT_NAME

STDOUT_LOG_FORMATTER = Formatter("%(asctime)s - %(levelname)s - %(message)s")
FILE_LOG_FORMATTER = Formatter("%(asctime)s - %(name)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s")


class ProjectLogger(Logger):
    def __init__(self, name: str, filename: Path, level=NOTSET, backupCount=0) -> None:
        super().__init__(name, level)
        self.backup_count = backupCount
        self.filename = filename
        self.folder = self.filename.parent

        stdout_handler = StreamHandler(sys.stdout)
        stdout_handler.setFormatter(STDOUT_LOG_FORMATTER)
        file_handler = FileHandler(
            filename=filename,
            encoding="utf-8",
        )
        file_handler.setFormatter(FILE_LOG_FORMATTER)
        self.addHandler(stdout_handler)
        self.addHandler(file_handler)
        self.propagate = False
        if self.backup_count > 0:
            self.delete_stale_copies()

    def start_msg(self):
        self.info("Start task")

    def finish_msg(self):
        self.info("Task finished")

    def delete_stale_copies(self):
        log_files_list = list(self.folder.glob("*.log"))
        log_files_list.sort(key=os.path.getmtime, reverse=True)
        log_files_list = log_files_list[self.backup_count :]
        [log_file.unlink() for log_file in log_files_list]


logger = ProjectLogger(
    name=PROJECT_NAME,
    filename=LOG_FILE_NAME,
    level=LOGGING_LEVEL,
    backupCount=BACKUP_COUNT,
)
