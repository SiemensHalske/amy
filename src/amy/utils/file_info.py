import hashlib
import os
from dataclasses import dataclass
from typing import List


@dataclass
class FileInfo:
    """Data class to store file information."""
    input_path: str
    output_path: str = None

    @property
    def size(self) -> int:
        """Returns the file size in bytes."""
        try:
            return os.path.getsize(self.input_path)
        except OSError as err:
            raise ValueError(
                f"Unable to determine size of file '{self.input_path}': {err}") from err

    def _read_file(self, file_path: str) -> bytes:
        """
        Reads the content of a file and returns it as bytes.

        Args:
            file_path (str): The path to the file to read.

        Returns:
            bytes: The content of the file.
        """
        try:
            with open(file_path, 'rb') as file:
                return file.read()
        except OSError as err:
            raise ValueError(
                f"Failed to read file '{file_path}': {err}") from err

    def sha256_hash(self) -> List[str]:
        """
        Calculates the SHA256 hash of the file.

        Returns a list of strings representing the hash in hexadecimal format
        for both input and output files.
        """
        hasher = hashlib.sha256()
        input_hash = ""
        output_hash = ""

        try:
            # Calculate hash for input file
            input_data = self._read_file(self.input_path)
            hasher.update(input_data)
            input_hash = hasher.hexdigest()
            # Calculate hash for output file if it exists-
            if self.output_path:
                hasher = hashlib.sha256()  # Reset the hasher
                output_data = self._read_file(self.output_path)
                hasher.update(output_data)
                output_hash = hasher.hexdigest()
        except OSError as err:
            raise ValueError(
                f"Failed to read file '{self.input_path}' or '{self.output_path}': {err}") from err

        return [input_hash, output_hash]

    def extension(self, mode: str = "encoding") -> str:
        """
        Returns the file extension.

        True if the hash is for the input file, False for the output file.
        """
        file_path = self.input_path if mode == "encoding" else self.output_path
        return os.path.splitext(file_path)[1]

    def to_dict(self) -> dict:
        """Converts the FileInfo object to a dictionary."""
        return {
            "input_path": self.input_path,
            "output_path": self.output_path,
            "size": self.size,
            "extension": self.extension(),
        }
