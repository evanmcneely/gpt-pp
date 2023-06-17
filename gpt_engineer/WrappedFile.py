import pathlib
import io
import os
from typing import Optional


class WrappedFile:
    """A wrapper for a file object that provides utility methods for working with files."""

    def __init__(self, file: io.TextIOWrapper, path: str, project_path: str):
        self.path = path
        self.project_path = project_path
        self.file = file

    @classmethod
    def from_path(cls, path: str, project_path: str) -> Optional["WrappedFile"]:
        """Returns a WrappedFile object for the file at the given path."""
        wrapper = None
        full_path = cls._resolve_path(path, project_path)
        file = cls._open_file(full_path)
        if file:
            wrapper = cls(file=file, path=path, project_path=project_path)

        return wrapper

    def get_file_content(self) -> str:
        """Returns the content of the file as a string with line numbers, with the file path as a header."""
        lines = self.file.readlines()
        file_string = f"-- {self.path}\n"
        line_number = 1
        for line in lines:
            file_string += f"{line_number}: {line}\n"
            line_number += 1

        self._reset_file()
        return file_string

    def _resolve_path(path: str = None, project_path: str = None) -> pathlib.Path:
        """Returns the full path to the file based on the project path and file path."""
        return os.path.join(os.getcwd(), project_path, path)

    def write_file(self, content: str) -> None:
        """Writes the content to the file"""
        self.file.write(content)
        self._reset_file()

    def update_file(self, content, start) -> None:
        """Updates the file content starting from a particular index"""
        self.file.seek(start)
        self.file.write(content)
        self._reset_file()

    def delete_file(self) -> None:
        """Deletes the file at the given path."""
        file_path = self._resolve_path(path=self.path, project_path=self.project_path)
        self.close_file()
        os.remove(file_path)

    def _open_file(path) -> Optional[io.TextIOWrapper]:
        """Opens the file at the given path."""
        try:
            with open(path, "r+") as file:
                return file
        except PermissionError:
            print(
                f"Error: User does not have permission to access the file at {path}\n"
            )
        except Exception:
            print(f"Error: Could not open file at path {path}\n")

    def close_file(self) -> None:
        """Closes the file."""
        self.file.close()

    def _reset_file(self) -> None:
        """Resets the file pointer to the beginning of the file."""
        self.file.seek(0)
