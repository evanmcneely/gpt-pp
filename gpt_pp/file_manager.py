import os
from pathlib import Path
from typing import Dict, Optional

from gpt_pp.file_utils import apply_diff_patch, validate_file_path


class FileManager:
    """Manage all files in a project."""

    file_paths: Dict[str, Path]
    path: Path  # path to the project from cwd
    absolute_path: Path  # absolute path to the project
    name: str # name of the project

    def __init__(self, path: Path):
        """Initialize the FileManager with an empty dictionary of files
        and the project path.
        """
        absolute_path = path.absolute().resolve()
        self.file_paths = {}
        self.name = path.name
        self.path = path
        self.absolute_path = absolute_path

    def num_files(self) -> int:
        """Return the number of files in the FileManager's dictionary"""
        return len(self.file_paths)

    def get_file(self, path_name: str) -> Optional[Path]:
        """Return the file at the given path."""
        if path_name in self.file_paths:
            return self.file_paths[path_name]
        else:
            return None

    def already_added(self, path_name: str) -> bool:
        return path_name in self.file_paths

    def add(self, path: Path) -> Optional[Path]:
        """Adds a new file to the FileManager's dictionary of files."""
        if self.already_added(str(path)):
            return None

        absolute_file_path = self.absolute_path / path
        valid = validate_file_path(absolute_file_path)

        if not valid:
            return None

        self.file_paths[str(path)] = absolute_file_path
        return absolute_file_path

    def create(self, path_name: str, content: str) -> Optional[Path]:
        path = Path(path_name)
        file = self.add(path)

        if not file:
            return None

        with file.open("w") as f:
            f.write(content)

        return file

    def apply_patch(self, path_name: str, patch: str) -> Optional[Path]:
        """Apply the diff patch to the file system."""
        file = self.file_paths[path_name]
        if not file:
            return None

        with file.open("r+") as f:
            content = file.read_text()
            patched = apply_diff_patch(content, patch)
            f.write(patched)

        return file

    def delete(self, path_name: str):
        """Delete a file from the FileManager's dictionary of
        files and remove it from disk.
        """
        file = self.file_paths[path_name]
        if file:
            os.remove(file)
            self.file_paths.pop(path_name, None)

    def _read_with_line_numbers(self, path_name: str, file: Path) -> str:
        with file.open("r") as f:
            lines = f.readlines()

            file_string = f"-- {path_name}\n"
            line_number = 1
            for line in lines:
                file_string += f"{line_number}: {line}"
                line_number += 1

            return file_string

    def get_content(self, path_name: str) -> Optional[str]:
        """Return the content of the file at the given path with line numbers
        prepended to each line of the file.
        """
        file = self.get_file(path_name)
        if not file:
            return None

        return self._read_with_line_numbers(path_name, file)

    def get_all_file_content(self) -> str:
        """Return a string with the content of all files, each
        with line numbers, sorted by file path.
        """
        files_content = []
        for path_name, path in sorted(self.file_paths.items()):
            content = self._read_with_line_numbers(path_name, path)
            files_content.append(content)

        return "\n\n".join(files_content)
