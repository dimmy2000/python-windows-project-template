# Standard Library
import os
from datetime import datetime
from logging import INFO
from pathlib import Path

# Third Party Library
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
# Project
PROJECT_AUTHOR = os.getenv("PROJECT_AUTHOR")
PROJECT_NAME = os.getenv("PROJECT_NAME")
PROJECT_VERSION = os.getenv("PROJECT_VERSION")
# Paths
PROJECT_FOLDER = Path.cwd()
LOGS_FOLDER = PROJECT_FOLDER / "logs"
LOGS_FOLDER.mkdir(parents=True, exist_ok=True)
# Other
TODAY = datetime.today()
LOGGING_LEVEL = INFO
LOG_FILE_NAME = LOGS_FOLDER / f"{PROJECT_NAME}-run-{TODAY:%Y-%m-%d-%H-%M-%S}.log"
BACKUP_COUNT = 0 if DEBUG is True else 2  # number of backup copies
