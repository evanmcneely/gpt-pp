import os


def _change_permissions(path: str, permissions=0o777) -> None:
    try:
        os.chmod(path, permissions)
    except OSError:
        # TODO: handle this properly
        raise


def _path_exists(path: str) -> bool:
    _change_permissions(path)
    return os.path.exists(path)


def _is_dir(path: str) -> bool:
    _change_permissions(path)
    return os.path.isdir(path)


def _is_file(path: str) -> bool:
    _change_permissions(path)
    return os.path.isfile(path)


def _get_file_extension(path: str) -> str:
    return os.path.splitext(path)[1].lower()


def resolve_path(*args: str) -> str:
    return os.path.abspath(os.path.join(os.getcwd(), *args))


DISALLOWED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"]


def validate_file_path(abs_path: str) -> None:
    # TODO: specific error messaging

    if not _path_exists(abs_path):
        raise ValueError(f"{abs_path} does not exist")

    if _is_dir(abs_path):
        raise ValueError(f"{abs_path} is a directory, not a file")

    if not _is_file(abs_path):
        raise ValueError(f"{abs_path} is not a file")

    file_extension = _get_file_extension(abs_path)
    if file_extension in DISALLOWED_FILE_EXTENSIONS:
        raise ValueError(f"File extension {file_extension} is not allowed")


def validate_directory_path(abs_path: str) -> bool:
    # TODO: specific error messaging

    created = False

    if not _path_exists(abs_path):
        os.makedirs(abs_path)
        created = True

    if _is_file(abs_path):
        raise ValueError(f"{abs_path} is a file, not a directory")

    if not _is_dir(abs_path):
        raise ValueError(f"{abs_path} is not a directory")

    return created
