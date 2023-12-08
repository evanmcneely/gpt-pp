import errno
import functools
import os
import re
import sys
from pathlib import Path

from .ui import UI


class ValidationError(ValueError):
    pass


# just because it isn't here doesn't mean it shouldn't be allowed
DISALLOWED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"]
DISALLOWED_FILE_DIRECTORIES = ["node_modules"]


def resolve_path(*args: Path) -> Path:
    """Resolve a path relative to the current working directory
    into an absolute path.
    """
    if len(args) == 0:
        return Path("")
    return Path.cwd().joinpath(*args).resolve()


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


def with_permissions(func):
    """Wrap a function and change the permissions of a file at the
    specified path and change the permissions back afterwards.
    """

    def _change_permissions(path: Path, permissions=0o777) -> None:
        """Change the permissions of the file at the given path."""
        try:
            path.chmod(permissions)
        except Exception:
            # ignore
            pass

    @functools.wraps(func)
    def wrapper(path: Path, *args, **kwargs):
        mode = path.stat().st_mode

        _change_permissions(path)  # change to write
        result = func(path, *args, **kwargs)
        _change_permissions(path, permissions=mode)  # change back

        return result

    return wrapper


# see https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
def _is_pathname_valid(path: str) -> bool:
    """`True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    """
    # Sadly, Python fails to provide the following magic number for us.
    ERROR_INVALID_NAME = 123

    try:
        if not isinstance(path, str) or not path:
            return False
        _, path = os.path.splitdrive(path)

        root_dirname = (
            os.environ.get("HOMEDRIVE", "C:")
            if sys.platform == "win32"
            else os.path.sep
        )
        os.access(root_dirname, os.F_OK)

        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep
        for pathname_part in path.split(os.path.sep):
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


@with_permissions
def _path_exists(path: Path) -> bool:
    """`True` if the given path exists; `False` otherwise."""
    try:
        return path.exists()
    except FileNotFoundError:
        return False


@with_permissions
def _is_dir(path: Path) -> bool:
    """`True` if the given path is a directory; `False` otherwise."""
    try:
        return path.is_dir()
    except FileNotFoundError:
        return False


@with_permissions
def _is_file(path: Path) -> bool:
    """`True` if the given path is a file; `False` otherwise."""
    try:
        return path.is_file()
    except FileNotFoundError:
        return False


def _get_file_extension(path: str) -> str:
    """Get the file extension of a file path."""
    return os.path.splitext(path)[1].lower()


def _is_file_extension_valid(file_path: Path) -> bool:
    """`True` if the given file path is a valid file extension for
    the appliciton; `False` otherwise.
    """
    file_extension = _get_file_extension(str(file_path))

    return False if file_extension in DISALLOWED_FILE_EXTENSIONS else True


def _is_parent_directory_valid(dir_path: Path) -> bool:
    """False if the path contains any directory disallowed by the application."""
    for dir in DISALLOWED_FILE_DIRECTORIES:
        if dir in str(dir_path):
            return False

    return True


# @with_permissions
def is_directory_empty(path: Path) -> bool:
    """Determine if a given directory is empty or not."""
    directory = path.iterdir()

    count = 0
    for file in directory:
        f = file.name
        if not str(f).startswith(".") and not str(f).startswith(".."):
            count += 1

    return count == 0


def validate_file_path(path: Path, warn: bool = False) -> bool:
    """Validate that a file path contains no disallowed file extensions
    or directories and that a file exists at the given path.
    """
    absolute_path = path.absolute()

    try:
        if not _is_file_extension_valid(absolute_path):
            raise ValidationError("Invalid file extension")
        if not _is_parent_directory_valid(absolute_path):
            raise ValidationError("Invalid directory in path")
        if not _is_pathname_valid(str(absolute_path)):
            raise ValidationError("Path is not valid")
        if not _path_exists(absolute_path):
            raise FileNotFoundError("Path does not exist")
        if not _is_file(absolute_path):
            raise ValidationError("Path is not a file")

    except FileNotFoundError or ValidationError as e:
        if warn:
            UI.error(f"{e} - {path}")
        return False

    except Exception as e:
        UI.error(f"Error validating file")
        raise

    else:
        return True


def validate_directory_path(path: Path, warn: bool = False) -> bool:
    """Validate that a directory path contains no disallowed file extensions
    or directories and that a directory exists at the given path.
    """
    absolute_path = path.absolute()

    try:
        if not _is_parent_directory_valid(absolute_path):
            raise ValidationError("Invalid directory in path")
        if not _is_pathname_valid(str(absolute_path)):
            raise ValidationError("Path is not valid")
        if not _path_exists(absolute_path):
            raise ValidationError("Path does not exist")
        if not _is_dir(absolute_path):
            raise ValidationError("Path is not a directory")

    except FileNotFoundError or ValidationError as e:
        if warn:
            UI.error(f"{e} - {path}")
        return False

    except Exception as e:
        UI.error(f"Error validating directory")
        raise

    else:
        return True


def apply_diff_patch(o: str, p: str, revert=False):
    """Apply unified diff patch to string s to recover newer string.
    If revert is True, treat s as the newer string, recover older string.
    """
    header_regex = re.compile("^@@ -(\d+),?(\d+)? \+(\d+),?(\d+)? @@$")

    original = o.splitlines(True)
    patch = p.splitlines(True)
    result = ""
    current = sl = 0
    (midx, sign) = (1, "+") if not revert else (3, "-")
    while current < len(patch) and patch[current].startswith(("---", "+++")):
        current += 1  # skip header lines
    while current < len(patch):
        match = header_regex.match(patch[current])
        if not match:
            raise Exception("Cannot process diff")
        current += 1
        l = int(match.group(midx)) - 1 + (match.group(midx + 1) == "0")
        result += "".join(original[sl:l])
        sl = l
        while current < len(patch) and patch[current][0] != "@":
            if current + 1 < len(patch) and patch[current + 1][0] == "\\":
                line = patch[current][:-1]
                current += 2
            else:
                line = patch[current]
                current += 1
            if len(line) > 0:
                if line[0] == sign or line[0] == " ":
                    result += line[1:]
                sl += line[0] != sign
    result += "".join(original[sl:])
    return result
