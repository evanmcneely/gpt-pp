import os
from typing import Dict, Optional
from functools import total_ordering

from .WrappedFile import WrappedFile
from .utils import resolve_path, validate_directory_path, validate_file_path


@total_ordering
class FileManager:
    """Manages all files in the project."""

    files: Dict[str, WrappedFile]
    project_path: str  # path to the project
    seed_file_path: str = None  # path to the "seed file" within the project

    def __init__(self, project_path: str, seed_file_path: str = None):
        self.files = {}
        self.project_path = project_path
        self.seed_file_path = seed_file_path

    @classmethod
    def from_seed_file(
        cls, project_path: str, seed_file_path: str
    ) -> Optional["FileManager"]:
        """Returns a FileManager object with the seed file included."""
        abs_path = resolve_path(project_path)
        validate_directory_path(abs_path)

        file = WrappedFile.from_path(seed_file_path, project_path)
        if file:
            manager = cls(project_path, seed_file_path)
            manager.files[file.path] = file

    def get_file(self, path: str) -> Optional[WrappedFile]:
        """Returns the WrappedFile object corresponding to the given file path."""
        if path in self.files:
            return self.files[path]
        else:
            return None

    def create(self, path: str, content: str):
        """Creates a new file with the given path and content."""
        if path in self.files or os.path.exists:
            raise ValueError("File already exists")

        # TODO: validate file path

        file = WrappedFile.from_path(path, self.project_path)
        if file:
            file.write(content)
            self.files[path] = file

    def update(self, path: str, content: str, start: int):
        """Updates the content of an existing file with the given content, starting at the given offset."""
        file = self.get_file(path)
        if file:
            file.update(content, start)

    def delete(self, path: str):
        """Deletes a file from the FileManager's dictionary of files and removes it from disk."""
        file = self.get_file(path)
        if file:
            file.delete()
            self.files.pop(path, None)

    def get_content(self, path: str) -> str:
        """Returns the content of the file at the given path."""
        file = self.get_file(path)
        if file:
            return file.read_with_line_numbers()

    def get_all_file_content(self) -> str:
        """Returns a string with the content of all files, each with line numbers, sorted by file path."""
        files_content = []
        for _, file in sorted(self.files.items()):
            files_content.append(file.read_with_line_numbers())

        return "\n\n".join(files_content)

    def add(self, path: str, seed: bool = False) -> Optional[WrappedFile]:
        """Adds a new file to the FileManager's dictionary of files."""
        # TODO: validate file path

        if seed:
            self.seed_file_path = path
        file = WrappedFile.from_path(path, self.project_path)
        if file:
            self.files[path] = file
            return file

    def number_of_files(self) -> int:
        return len(self.files)

    def get_seed_file_content(self) -> str:
        return self.get_content(self.seed_file_path)

    def get_seed_file(self) -> Optional[WrappedFile]:
        return self.get_file(self.seed_file_path)

    def __eq__(self, other):
        if isinstance(other, FileManager):
            return self.files == other.files
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, FileManager):
            return self.files < other.files
        return NotImplemented
