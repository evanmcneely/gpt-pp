import os, errno, sys, tempfile, stat, functools


class ValidationError(ValueError):
    pass


# Sadly, Python fails to provide the following magic number for us.
ERROR_INVALID_NAME = 123

# not an exhaustive list, just because it isn't here doesn't mean it shouldn't be allowed
DISALLOWED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"]
DISALLOWED_FILE_DIRECTORIES = ["node_modules"]


# see https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
def _is_pathname_valid(pathname: str) -> bool:
    """
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    """
    try:
        if not isinstance(pathname, str) or not pathname:
            return False
        _, pathname = os.path.splitdrive(pathname)

        root_dirname = (
            os.environ.get("HOMEDRIVE", "C:")
            if sys.platform == "win32"
            else os.path.sep
        )
        # ? need permissions ?
        # assert os.path.isdir(root_dirname)
        os.access(root_dirname, os.F_OK)

        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep
        for pathname_part in pathname.split(os.path.sep):
            try:
                # ? need permissions ?
                # os.lstat(root_dirname + pathname_part)
                os.access(root_dirname + pathname_part, os.F_OK)
            except OSError as exc:
                if hasattr(exc, "winerror"):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    except TypeError as exc:
        return False
    else:
        return True


# see https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
def _is_path_sibling_creatable(pathname: str) -> bool:
    """
    `True` if the current user has sufficient permissions to create **siblings**
    (i.e., arbitrary files in the parent directory) of the passed pathname;
    `False` otherwise.
    """
    dirname = os.path.dirname(pathname) or os.getcwd()

    try:
        with tempfile.TemporaryFile(dir=dirname):
            pass
        return True
    except EnvironmentError:
        return False


# see https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
def _is_path_exists_or_creatable_portable(pathname: str) -> bool:
    """
    `True` if the passed pathname is a valid pathname on the current OS _and_
    either currently exists or is hypothetically creatable in a cross-platform
    manner optimized for POSIX-unfriendly filesystems; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    """
    try:
        return _is_pathname_valid(pathname) and _is_path_sibling_creatable(pathname)

    except OSError:
        return False


def _change_permissions(path: str, permissions=0o777) -> None:
    try:
        os.chmod(path, permissions)
    except Exception:
        # ignore
        pass


def _get_file_extension(path: str) -> str:
    return os.path.splitext(path)[1].lower()


def with_permissions(func):
    @functools.wraps(func)
    def wrapper(path, *args, **kwargs):
        mode = os.stat(path).st_mode
        _change_permissions(path)
        result = func(path, *args, **kwargs)
        _change_permissions(path, permissions=mode)
        return result

    return wrapper


@with_permissions
def _is_dir(path: str) -> bool:
    return os.path.isdir(path)


@with_permissions
def _is_file(path: str) -> bool:
    return os.path.isfile(path)


def _is_file_extension_valid(file_path: str) -> bool:
    file_extension = _get_file_extension(file_path)

    return False if file_extension in DISALLOWED_FILE_EXTENSIONS else True


def _is_parent_directory_valid(dir_path: str) -> bool:
    for dir in DISALLOWED_FILE_DIRECTORIES:
        if dir in dir_path:
            return False

    return True


def resolve_path(*args: str) -> str:
    if len(args) == 0:
        return ""
    return os.path.abspath(os.path.join(os.getcwd(), *args))


def sanitize_path(path: str) -> str:
    return path.strip(" \n") if path else ""


def sanitize_input(input: str) -> str:
    if not input:
        return ""

    # only using the first line
    input = input.split("\n")[0]

    return sanitize_path(input)


@with_permissions
def is_directory_empty(path: str) -> bool:
    """Determines if a given directory is empty or not
    :param dir_path: absolute path of the directory
    :return: True if directory is empty, else False
    """
    abs_path = resolve_path(path)
    return len(os.listdir(abs_path)) == 0


def validate_file_path(abs_path: str) -> None:
    abs_path = sanitize_path(abs_path)

    if not _is_file_extension_valid(abs_path):
        raise ValidationError("Invalid file extension")

    if not _is_parent_directory_valid(abs_path):
        raise ValidationError("Invalid directory in path")

    if not _is_pathname_valid(abs_path):
        raise ValidationError("Path does not exist")

    if not _is_file(abs_path):
        raise ValidationError("Path is not a file")


def validate_directory_path(abs_path: str) -> None:
    abs_path = sanitize_path(abs_path)

    if not _is_parent_directory_valid(abs_path):
        raise ValidationError("Invalid directory in path")

    if not _is_pathname_valid(abs_path):
        raise ValidationError("Path does not exist")

    if not _is_dir(abs_path):
        raise ValidationError("Path is not a directory")
