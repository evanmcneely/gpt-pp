import os
from typing import Optional, IO, Any

from .file_utils import (ValidationError, resolve_path, validate_file_path,
                         with_permissions)


@with_permissions
def _open(path: str, method: str) -> IO[Any]:
    """Open a file for reading and writing with permissions set."""
    file = open(path, method)
    return file


class WrappedFile:
    """Wrap a file path and provide utility methods for working 
    with the file content at the path.
    """

    path: str  # path to the file within the project
    abs_path: str  # absolute path to the file from the root directory

    def __init__(self, path: str, absolute_path: str):
        """Initialize the WrappedFile object with the given path and absolute path."""
        self.path = path
        self.abs_path = absolute_path

    @classmethod
    def from_path(cls, path: str, project_path: str) -> Optional["WrappedFile"]:
        """Create a WrappedFile object from the given path and return it."""
        abs_path = resolve_path(project_path, path)

        try:
            validate_file_path(abs_path)
        except ValidationError:
            raise
        except FileNotFoundError:
            # create the file
            with open(abs_path, "w"):
                pass

        return cls(path, abs_path)

    def read_with_line_numbers(self) -> str:
        """Return the content of the file as a string with line numbers 
        and file path as a header.
        """
        file = _open(self.abs_path, "r")
        lines = file.readlines()
        file.close()

        file_string = f"-- {self.path}\n"
        line_number = 1
        for line in lines:
            file_string += f"{line_number}: {line}"
            line_number += 1

        return file_string

    def write(self, content: str) -> None:
        """Write content to the file"""
        file = _open(self.abs_path, "r+")
        file.write(content)
        file.close()

    def update(self, content: str, start: int) -> None:
        """Update the file content starting from a particular index"""
        file = _open(self.abs_path, "r+")
        file.seek(start)
        file.write(content)
        file.close()

    def delete(self) -> None:
        """Delete the file at the path."""
        os.remove(self.abs_path)
