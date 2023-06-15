from typing import Dict
from functools import total_ordering
from FileWrapper import FileWrapper


@total_ordering
class FileManager:
    def __init__(self, project_path: str):
        self.files: Dict[str, FileWrapper] = {}
        self.project_path = project_path

    def get_file(self, path: str) -> FileWrapper:
        """Returns the FileWrapper object corresponding to the given file path."""
        if path in self.files:
            return self.files[path]
        else:
            return None

    def create(self, path: str, content: str) -> None:
        """Creates a new file with the given path and content."""
        file = FileWrapper.from_path(path, self.project_path)
        if file:
            file.write_file(content)
            self.files[path] = file

    def update(self, path: str, content: str, start: int) -> None:
        """Updates the content of an existing file with the given content, starting at the given offset."""
        file = self.get_file(path)
        if file:
            file.update_file(content, start)

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
            files_content.append(file.get_file_content_with_line_numbers())

        return "\n\n".join(files_content)

    def add_file(self, path: str) -> None:
        """Adds a new file to the FileManager's dictionary of files."""
        file = FileWrapper.from_path(path, self.project_path)
        if file:
            self.files[path] = file

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
