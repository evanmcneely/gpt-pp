from typing import Dict, Optional

from gpt_pp.file_utils import resolve_path, validate_file_path
from gpt_pp.wrapped_file import WrappedFile


class FileManager:
    """Manage all files in a project."""

    files: Dict[str, WrappedFile]
    project_path: str  # path to the project

    def __init__(self, project_path: str):
        """Initialize the FileManager with an empty dictionary of files
        and the project path.
        """
        self.files = {}
        self.project_path = project_path

    def num_files(self) -> int:
        """Return the number of files in the FileManager's dictionary"""
        return len(self.files)

    def get_file(self, path: str) -> Optional[WrappedFile]:
        """Return the file at the given path."""
        if path in self.files:
            return self.files[path]
        else:
            return None

    def add(self, path: str, content: Optional[str] = None) -> Optional[WrappedFile]:
        """Adds a new file to the FileManager's dictionary of files."""
        abs_path = resolve_path(self.project_path, path)
        file: Optional[WrappedFile] = WrappedFile.from_path(abs_path)
        if file and content:
            file.write(content)

        return file

    def apply_patch(self, path: str, patch: str):
        """Apply the diff patch to the file system."""
        file = self.files[path]
        if file:
            file.apply_patch(patch)

    def delete(self, path: str):
        """Delete a file from the FileManager's dictionary of
        files and remove it from disk.
        """
        file = self.files[path]
        if file:
            file.delete()
            self.files.pop(path, None)

    def get_content(self, path: str) -> Optional[str]:
        """Return the content of the file at the given path with line numbers
        prepended to each line of the file.
        """
        file = self.get_file(path)
        if file:
            return file.read_with_line_numbers()

    def get_all_file_content(self) -> str:
        """Return a string with the content of all files, each
        with line numbers, sorted by file path.
        """
        files_content = []
        for _, file in sorted(self.files.items()):
            files_content.append(file.read_with_line_numbers())

        return "\n\n".join(files_content)
