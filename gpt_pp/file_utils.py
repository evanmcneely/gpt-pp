import errno
import functools
import os
import sys
from pathlib import Path
from typing import Any

from .ui import UI


class ValidationError(ValueError):
    pass


# just because it isn't here doesn't mean it shouldn't be allowed
DISALLOWED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"]
DISALLOWED_FILE_DIRECTORIES = ["node_modules"]


def resolve_path(*args: str) -> str:
    """Resolve a path relative to the current working directory
    into an absolute path.
    """
    if len(args) == 0:
        return ""
    return os.path.abspath(os.path.join(os.getcwd(), *args))


def sanitize_path(path: str) -> str:
    """Sanitize a path by removing leading and trailing spaces and newlines."""
    return path.strip(" \n") if path else ""


def sanitize_input(input: str) -> str:
    """Sanitize an input by removing leading and trailing spaces and newlines
    and return only the first line."""
    if not input:
        return ""

    # only using the first line
    input = input.split("\n")[0]

    return sanitize_path(input)


# see https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
def _is_pathname_valid(pathname: str) -> bool:
    """`True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    """
    # Sadly, Python fails to provide the following magic number for us.
    ERROR_INVALID_NAME = 123

    try:
        if not isinstance(pathname, str) or not pathname:
            return False
        _, pathname = os.path.splitdrive(pathname)

        root_dirname = (
            os.environ.get("HOMEDRIVE", "C:")
            if sys.platform == "win32"
            else os.path.sep
        )
        os.access(root_dirname, os.F_OK)

        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.access(root_dirname + pathname_part, os.F_OK)
            except OSError as exc:
                if hasattr(exc, "winerror"):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    except TypeError:
        return False
    else:
        return True


def with_permissions(func):
    """Wrap a function and change the permissions of a file at the
    specified path and change the permissions back afterwards.
    """

    def _change_permissions(path: str, permissions=0o777) -> None:
        """Change the permissions of the file at the given path."""
        try:
            os.chmod(path, permissions)
        except Exception:
            # ignore
            pass

    @functools.wraps(func)
    def wrapper(blob: Any, *args, **kwargs):
        # NOTE: delay import circular dependency
        from gpt_pp.wrapped_file import WrappedFile

        path = blob
        if isinstance(blob, WrappedFile):
            path = blob.abs_path

        mode = os.stat(path).st_mode
        _change_permissions(path)

        result = func(blob, *args, **kwargs)

        _change_permissions(path, permissions=mode)
        return result

    return wrapper


@with_permissions
def _path_exists(path: str) -> bool:
    """`True` if the given path exists; `False` otherwise."""
    try:
        return os.path.exists(path)
    except FileNotFoundError:
        return False


@with_permissions
def _is_dir(path: str) -> bool:
    """`True` if the given path is a directory; `False` otherwise."""
    try:
        return os.path.isdir(path)
    except FileNotFoundError:
        return False


@with_permissions
def _is_file(path: str) -> bool:
    """`True` if the given path is a file; `False` otherwise."""
    try:
        return os.path.isfile(path)
    except FileNotFoundError:
        return False


def _get_file_extension(path: str) -> str:
    """Get the file extension of a file path."""
    return os.path.splitext(path)[1].lower()


def _is_file_extension_valid(file_path: str) -> bool:
    """`True` if the given file path is a valid file extension for
    the appliciton; `False` otherwise.
    """
    file_extension = _get_file_extension(file_path)

    return False if file_extension in DISALLOWED_FILE_EXTENSIONS else True


def _is_parent_directory_valid(dir_path: str) -> bool:
    """False if the path contains any directory disallowed by the application."""
    for dir in DISALLOWED_FILE_DIRECTORIES:
        if dir in dir_path:
            return False

    return True


@with_permissions
def is_directory_empty(path: Path) -> bool:
    """Determine if a given directory is empty or not."""
    try:
        contents = path.iterdir()
        filtered_contents = [
            f
            for f in contents
            if not str(f).startswith(".") and not str(f).startswith("..")
        ]
        return len(filtered_contents) == 0
    except Exception as e:
        UI.error(f"Error while checking if directory is empty: {e}")
        return False


def validate_file_path(abs_path: str) -> None:
    """Validate that a file path contains no disallowed file extensions
    or directories and that a file exists at the given path.
    """
    abs_path = sanitize_path(abs_path)

    if not _is_file_extension_valid(abs_path):
        raise ValidationError("Invalid file extension")

    if not _is_parent_directory_valid(abs_path):
        raise ValidationError("Invalid directory in path")

    if not _is_pathname_valid(abs_path):
        raise ValidationError("Path is not valid")

    if not _path_exists(abs_path):
        raise FileNotFoundError("Path does not exist")

    if not _is_file(abs_path):
        raise ValidationError("Path is not a file")


def validate_directory_path(abs_path: str) -> None:
    """Validate that a directory path contains no disallowed file extensions
    or directories and that a directory exists at the given path.
    """
    abs_path = sanitize_path(abs_path)

    if not _is_parent_directory_valid(abs_path):
        raise ValidationError("Invalid directory in path")

    if not _is_pathname_valid(abs_path):
        raise ValidationError("Path is not valid")

    if not _path_exists(abs_path):
        raise ValidationError("Path does not exist")

    if not _is_dir(abs_path):
        raise ValidationError("Path is not a directory")
