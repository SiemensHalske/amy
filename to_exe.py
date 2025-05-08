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
    def validate_file(file_path: str, required_extension: str = '.b64') -> None:
        """Validates the file existence and extension."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")
        if not file_path.endswith(required_extension):
            raise ValueError(
                f"File '{file_path}' must have a '{required_extension}' extension.")

    def __str__(self) -> str:
        return "FileValidator"

    def __repr__(self) -> str:
        return self.__str__()


class Base64Decoder:
    """Handles Base64 decoding logic."""
    @staticmethod
    def decode(b64_data: bytes) -> bytes:
        """Decodes Base64 content into binary data."""
        try:
            return base64.b64decode(b64_data)
        except base64.binascii.Error as err:
            raise ValueError(f"Failed to decode Base64 data: {err}") from err

    def __str__(self) -> str:
        return "Base64Decoder"

    def __repr__(self) -> str:
        return self.__str__()


class Logger:
    """Handles logging functionality using Rich."""

    def __init__(self, display: Console = Console()):
        self.console = display

    def log_summary(self, b64_file: FileInfo, original_file: FileInfo) -> None:
        """Logs decoding summary using a table."""
        try:
            table = Table(title="File Decoding Summary")
            table.add_column("File", justify="left",
                             style="cyan", no_wrap=True)
            table.add_column("Size (bytes)", justify="right", style="magenta")
            table.add_column("SHA256 Hash", justify="left", style="green")

            table.add_row(b64_file.path, str(
                b64_file.size), b64_file.sha256_hash)
            table.add_row(original_file.path, str(
                original_file.size), original_file.sha256_hash)

            self.console.print(table)
            self.console.print(
                f"[bold green]File '{b64_file.path}' has been successfully "
                f"decoded to '{original_file.path}'.[/bold green]"
            )
        except Exception as err:  # pylint: disable=broad-except
            self.console.print(f"[red]Logging error:[/red] {err}")

    def __str__(self) -> str:
        return "Logger"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class Base64FileDecoder:
    """Main class to orchestrate the Base64 file decoding process."""
    b64_file_path: str
    logger: Logger = Logger()

    @classmethod
    def from_file(cls, b64_file_path: str) -> 'Base64FileDecoder':
        """Factory method to create a decoder instance."""
        FileValidator.validate_file(b64_file_path)
        return cls(b64_file_path)

    def decode(self) -> None:
        """Main method to decode the Base64 file."""
        try:
            # Prepare file information objects
            b64_file = FileInfo(self.b64_file_path)
            original_file_path = self._get_original_file_path()
            original_file = FileInfo(original_file_path)

            # Perform decoding
            b64_data = self._read_file(b64_file.path)
            original_data = Base64Decoder.decode(b64_data)
            self._write_file(original_file.path, original_data)

            # Log success
            self.logger.log_summary(b64_file, original_file)
        except Exception as err:  # pylint: disable=broad-except
            self.logger.console.print(f"[red]Error:[/red] {err}")

    def _get_original_file_path(self) -> str:
        """Generates the output file path by removing the .b64 extension."""
        if not self.b64_file_path.endswith('.b64'):
            raise ValueError(
                f"File '{self.b64_file_path}' does not have a valid '.b64' extension.")
        return self.b64_file_path[:-4]

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
    # Replace 'plugin.VSIXPackage.b64' with the path to your Base64 file
    INPUT_FILE = 'plugin.VSIXPackage.b64'
    try:
        decoder = Base64FileDecoder.from_file(INPUT_FILE)
        decoder.decode()
    except Exception as err:  # pylint: disable=broad-except
        console = Console()
        console.print(f"[red]Critical Error:[/red] {err}")
