import os
from typing import Optional

from .file_utils import resolve_path, with_permissions


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
        """Returns a WrappedFile object for the file at the given path."""
        abs_path = resolve_path(project_path, path)

        return cls(path, abs_path)

    def read_with_line_numbers(self) -> str:
        """Returns the content of the file as a string with
        line numbers, with the file path as a header."""
        with open(self.abs_path, "r") as file:
            lines = file.readlines()
            file_string = f"-- {self.path}\n"
            line_number = 1
            for line in lines:
                file_string += f"{line_number}: {line}"
                line_number += 1

            return file_string

    @with_permissions
    def write(self, content: str) -> None:
        """Writes the content to the file"""
        with open(self.abs_path, "r+") as file:
            file.write(content)

    @with_permissions
    def update(self, content: str, start: int) -> None:
        """Updates the file content starting from a particular index"""
        with open(self.abs_path, "r+") as file:
            file.seek(start)
            file.write(content)

    @with_permissions
    def delete(self) -> None:
        """Deletes the file at the given path."""
        os.remove(self.abs_path)
