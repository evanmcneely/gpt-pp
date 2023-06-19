import os


def resolve_path(*args: str) -> str:
    return os.path.abspath(os.path.join(os.getcwd(), *args))


DISALLOWED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"]


def validate_file_path(abs_path: str):
    # TODO: specific error messaging

    os.chmod(abs_path, 0o777)

    if not os.path.exists(abs_path):
        raise ValueError(f"{abs_path} does not exist")

    if os.path.isdir(abs_path) or not os.path.isfile(abs_path):
        raise ValueError(f"{abs_path} is a directory, not a file")

    file_extension = os.path.splitext(abs_path)[1]
    if file_extension.lower() in DISALLOWED_FILE_EXTENSIONS:
        raise ValueError(f"File extension {file_extension} is not allowed")


def supermakedirs(path, mode):
    if not path or os.path.exists(path):
        return []
    (head, tail) = os.path.split(path)
    res = supermakedirs(head, mode)
    os.mkdir(path)
    os.chmod(path, mode)
    res += [path]
    return res


def validate_directory_path(abs_path: str) -> bool:
    # TODO: specific error messaging

    created = False
    os.chmod(abs_path, 0o777)

    if not os.path.exists(abs_path):
        supermakedirs(abs_path, 0o777)
        created = True

    if os.path.isfile(abs_path):
        raise ValueError(f"{abs_path} is a file, not a directory")

    if not os.path.isdir(abs_path):
        raise ValueError(f"{abs_path} is not a directory")

    return created
