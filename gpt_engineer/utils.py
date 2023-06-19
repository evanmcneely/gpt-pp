import os


def resolve_path(**args: str) -> str:
    return os.path.abspath(os.path.join(os.getcwd(), **args))


DISALLOWED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"]


def validate_file_path(path: str):
    if os.path.isdir(path) or not os.path.isfile(path):
        raise ValueError(f"{path} is a directory, not a file")

    file_extension = os.path.splitext(path)[1]
    if file_extension.lower() in DISALLOWED_FILE_EXTENSIONS:
        raise ValueError(f"File extension {file_extension} is not allowed")


def validate_directory_path(path: str) -> bool:
    if not os.path.isdir(path) or not os.path.isfile(path):
        raise ValueError(f"{path} is a file, not a directory")


def create_directory(path) -> bool:
    try:
        os.makedirs(path)
    except FileExistsError:
        raise ValueError(f"{path} already exists")
