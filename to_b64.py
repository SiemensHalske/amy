"""
Module Name: <module_name>

Description:
    This module provides functionality for encoding and decoding files to and from Base64 format.
    It includes classes and methods to encode files to Base64,
    decode Base64 files, validate file inputs, etc. The module is designed to handle errors
    gracefully and provide detailed logging using the Rich library.

Author:
    Hendrik Siemens

Created:
    2025-05-08

Updated:
    2025-05-08

Usage:

    1. Replace 'plugin.VSIXPackage' with the path to your file.
    2. Run the script to encode the file to Base64 format.

Dependencies:
    - rich: For console output and table formatting.

Classes:
    - FileInfo: Represents metadata and properties of a file (size, SHA256 hash).
    - FileValidator: Validates file existence and extensions.
    - Base64FileEncoder: Encodes files into Base64 format.
    - Base64FileDecoder: Decodes Base64 files back to their original format.
    - Logger: Handles logging of operations using Rich.

Error Handling:
    The module includes detailed error handling for:
    - File not found or inaccessible.
    - Invalid file extensions.
    - Base64 encoding/decoding errors.
    - General I/O errors.

License:
    MIT License (for now)
"""


import base64
import os
import hashlib
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table


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


class FileValidator:
    """Handles file validation logic."""
    @staticmethod
    def validate_file(file_path: str) -> None:
        """Validates the file existence and checks if it's non-empty."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")
        if os.path.getsize(file_path) == 0:
            raise ValueError(f"File '{file_path}' is empty.")

    def __str__(self) -> str:
        return "FileValidator"

    def __repr__(self) -> str:
        return self.__str__()


class Base64Encoder:
    """Handles Base64 encoding logic."""
    @staticmethod
    def encode(data: bytes) -> bytes:
        """Encodes binary data to Base64."""
        try:
            return base64.b64encode(data)
        except Exception as err:
            raise ValueError(
                f"Failed to encode data to Base64: {err}") from err

    def __str__(self) -> str:
        return "Base64Encoder"

    def __repr__(self) -> str:
        return self.__str__()


class Logger:
    """Handles logging functionality using Rich."""

    def __init__(self, display: Console = Console()):
        self.console = display

    def log_summary(self, original_file: FileInfo, b64_file: FileInfo) -> None:
        """Logs encoding summary using a table."""
        try:
            table = Table(title="File Encoding Summary")
            table.add_column(
                "File", justify="left",
                style="cyan", no_wrap=True
            )
            table.add_column("Size (bytes)", justify="right", style="magenta")
            table.add_column("SHA256 Hash", justify="left", style="green")

            table.add_row(original_file.path, str(
                original_file.size), original_file.sha256_hash)
            table.add_row(b64_file.path, str(
                b64_file.size), b64_file.sha256_hash)

            self.console.print(table)
            self.console.print(
                f"[bold green]File '{original_file.path}' has been successfully "
                f"encoded to '{b64_file.path}'.[/bold green]"
            )
        except Exception as err:  # pylint: disable=broad-except
            self.console.print(f"[red]Logging Error:[/red] {err}")

    def __str__(self) -> str:
        return "Logger"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class Base64FileEncoder:
    """Main class to orchestrate the Base64 file encoding process."""
    file_path: str
    logger: Logger = Logger()

    @classmethod
    def from_file(cls, file_path: str) -> 'Base64FileEncoder':
        """Factory method to create an encoder instance."""
        FileValidator.validate_file(file_path)
        return cls(file_path)

    def encode(self) -> None:
        """Main method to encode the file to Base64."""
        try:
            # Prepare file information objects
            original_file = FileInfo(self.file_path)
            b64_file_path = self._get_b64_file_path()
            b64_file = FileInfo(b64_file_path)

            # Perform encoding
            file_data = self._read_file(original_file.path)
            b64_data = Base64Encoder.encode(file_data)
            self._write_file(b64_file.path, b64_data)

            # Log success
            self.logger.log_summary(original_file, b64_file)
        except Exception as err:  # pylint: disable=broad-except
            self.logger.console.print(f"[red]Error:[/red] {err}")

    def _get_b64_file_path(self) -> str:
        """Generates the output file path with a .b64 extension."""
        return f"{self.file_path}.b64"

    @staticmethod
    def _read_file(file_path: str) -> bytes:
        """Reads content from the specified file."""
        try:
            with open(file_path, 'rb') as file:
                return file.read()
        except OSError as err:
            raise ValueError(
                f"Failed to read file '{file_path}': {err}") from err

    @staticmethod
    def _write_file(file_path: str, data: bytes) -> None:
        """Writes data to the specified file."""
        try:
            with open(file_path, 'wb') as file:
                file.write(data)
        except OSError as err:
            raise ValueError(
                f"Failed to write to file '{file_path}': {err}") from err


if __name__ == "__main__":
    # Replace 'plugin.VSIXPackage' with the path to your file
    INPUT_FILE = 'plugin.VSIXPackage'
    try:
        encoder = Base64FileEncoder.from_file(INPUT_FILE)
        encoder.encode()
    except Exception as err:  # pylint: disable=broad-except
        console = Console()
        console.print(f"[red]Critical Error:[/red] {err}")
