import os
import re
from typing import Optional

from gpt_pp.file_utils import (  # isort:skip
    ValidationError,
    validate_file_path,
    with_permissions,
)


# https://stackoverflow.com/questions/2307472/generating-and-applying-diffs-in-python
def apply_diff_patch(o: str, p:str, revert=False):
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


class WrappedFile:
    """Wrap a file path and provide utility methods for working
    with the file content at the path.
    """

    abs_path: str  # absolute path to the file from the root directory

    def __init__(self,  absolute_path: str):
        """Initialize the WrappedFile object with the given path and absolute path."""
        self.abs_path = absolute_path

    @classmethod
    def from_path(cls, path: str) -> Optional["WrappedFile"]:
        """Create a WrappedFile object from the given path and return it."""
        try:
            validate_file_path(path)
        except ValidationError:
            raise
        except FileNotFoundError:
            # create the file
            with open(path, "w"):
                pass

        return cls(path)

    @with_permissions
    def read_with_line_numbers(self) -> str:
        """Return the content of the file as a string with line numbers
        and file path as a header.
        """
        file = open(self.abs_path, "r")
        lines = file.readlines()
        file.close()

        file_string = f"-- {self.abs_path}\n"
        line_number = 1
        for line in lines:
            file_string += f"{line_number}: {line}"
            line_number += 1

        return file_string

    @with_permissions
    def write(self, content: str) -> None:
        """Write content to the file"""
        with open(self.abs_path, "w") as file:
            file.write(content)

    @with_permissions
    def apply_patch(self, patch: str) -> None:
        """Apply the diff patch to the file system."""
        with open(self.abs_path, "r") as file:
            content = file.read()
        modified = apply_diff_patch(content, patch)
        self.write(modified)

    @with_permissions
    def delete(self) -> None:
        """Delete the file at the path."""
        os.remove(self.abs_path)
