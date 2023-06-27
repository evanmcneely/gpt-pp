import os
from typing import Optional

from .file_utils import (ValidationError, resolve_path, validate_file_path,
                         with_permissions)


@with_permissions
def _open(path, method) -> None:
    """Opens the file for reading and writing"""
    file = open(path, method)
    return file


class WrappedFile:
    """A wrapper for a file object that provides utility
    methods for working working with file content"""

    path: str  # path to the file within the project
    abs_path: str  # absolute path to the file from the root directory

    def __init__(self, path: str, absolute_path: str):
        self.path = path
        self.abs_path = absolute_path

    @classmethod
    def from_path(cls, path: str, project_path: str) -> Optional["WrappedFile"]:
        """Returns a WrappedFile object for the file at the given path. Creates a file at the specified if it does not exist"""
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
        """Returns the content of the file as a string with
        line numbers, with the file path as a header."""
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
        """Writes the content to the file"""
        file = _open(self.abs_path, "r+")
        file.write(content)
        file.close()

    def update(self, content: str, start: int) -> None:
        """Updates the file content starting from a particular index"""
        file = _open(self.abs_path, "r+")
        file.seek(start)
        file.write(content)
        file.close()

    def delete(self) -> None:
        """Deletes the file at the given path."""
        os.remove(self.abs_path)
