import os
from typing import Dict, Optional
from functools import total_ordering
from .WrappedFile import WrappedFile


@total_ordering
class FileManager:
    def __init__(self, project_path: str):
        self.files: Dict[str, WrappedFile] = {}
        self.project_path = project_path

    @staticmethod
    def resolve_path(
        project_path: str,
        path: str,
    ) -> str:
        return os.path.join(os.getcwd(), project_path, path)

    def does_file_exist(cls, self, path: str) -> bool:
        return os.path.exists(cls.resolve_path(self.project_path, path))

    def get_file(self, path: str) -> WrappedFile:
        """Returns the WrappedFile object corresponding to the given file path."""
        if path in self.files:
            return self.files[path]
        else:
            return None

    def create(self, path: str, content: str) -> None:
        """Creates a new file with the given path and content."""
        file = WrappedFile.from_path(path, self.project_path)
        if file:
            file.write_file(content)
            self.files[path] = file

    def update(self, path: str, content: str, start: int) -> None:
        """Updates the content of an existing file with the given content, starting at the given offset."""
        file = self.get_file(path)
        if file:
            file.update_file(content, start)

    # TODO: add - add code to a file

    # TODO: remove - remove code from a file between two lines

    def delete(self, path: str) -> None:
        """Deletes a file from the FileManager's dictionary of files and removes it from disk."""
        file = self.get_file(path)
        if file:
            file.delete_file()
            self.files.pop(path, None)

    def get_all_files_content(self) -> str:
        """Returns a string with the content of all files, each with line numbers, sorted by file path."""
        files_content = []
        for _, file in sorted(self.files.items()):
            files_content.append(file.get_file_content())

        return "\n\n".join(files_content)

    def add_file(self, path: str = None, seed: bool = False) -> None:
        """Adds a new file to the FileManager's dictionary of files."""
        if seed:
            self.seed_file_path = path

        # TODO: input validation

        file = WrappedFile.from_path(path, self.project_path)
        if file:
            self.files[path] = file

    def get_seed_file_content(self) -> Optional[str]:
        """Returns the content of the seed file."""
        if self.seed_file_path:
            return self.get_file(self.seed_file_path).get_file_content()

    def close_all_files(self) -> None:
        """Closes all open files."""
        for _, file in self.files.items():
            file.close_file()

    def __eq__(self, other):
        if isinstance(other, FileManager):
            return self.files == other.files
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, FileManager):
            return self.files < other.files
        return NotImplemented
