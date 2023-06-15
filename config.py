import logging
import pathlib

from dotenv import load_dotenv
from decouple import config

from db import DBs, DB
from utils import validate_directory, validate_file_path, FileManager

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

CODE_MODEL = config("CODE_MODEL", default="gpt-3.5-turbo-16k")
INTERPRETATION_MODEL = config("INTERPRETATION_MODEL", default="gpt-3.5-turbo-16k")
CONVERSATION_MODEL = config("CONVERSE_MODEL", default="gpt-3.5-turbo")


def init_app(project_path: str, seed_file_path: str, run_prefix: str):
    validate_directory(project_path)
    seed_file_exists = validate_file_path(seed_file_path)

    dbs = DBs(
        logs=DB(pathlib.Path(__file__).parent / (run_prefix + "logs")),
        preferences=DB(pathlib.Path(__file__).parent / "preferences"),
    )

    file_manager = FileManager(project_path)

    if seed_file_exists:
        file_manager.add_file(seed_file_path)

    return dbs, file_manager
