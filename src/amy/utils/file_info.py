import hashlib
import os
from dataclasses import dataclass


@dataclass
class FileInfo:
    """Data class to store file information."""
    path: str

    @property
    def size(self) -> int:
        """Returns the file size in bytes."""
        try:
            return os.path.getsize(self.path)
        except OSError as err:
            raise ValueError(
                f"Unable to determine size of file '{self.path}': {err}") from err

    @property
    def sha256_hash(self) -> str:
        """Calculates the SHA256 hash of the file."""
        try:
            with open(self.path, 'rb') as file:
                return hashlib.sha256(file.read()).hexdigest()
        except OSError as err:
            raise ValueError(
                f"Unable to calculate SHA256 hash for file '{self.path}': {err}") from err
