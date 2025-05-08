import base64
from dataclasses import dataclass

from amy.utils import Logger, FileInfo, FileValidator


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


@dataclass
class Base64FileEncoder:
    """Main class to orchestrate the Base64 file encoding process."""
    file_path: str
    output_path: str = None
    logger: Logger = Logger()

    @classmethod
    def from_file(cls, file_path: str, output_path: str = None) -> 'Base64FileEncoder':
        """Factory method to create an encoder instance."""
        FileValidator.validate_file(file_path)
        return cls(file_path, output_path)

    def encode(self) -> None:
        """Main method to encode the file to Base64."""
        try:
            # Prepare file information objects
            original_file = FileInfo(self.file_path)
            b64_file_path = self.output_path if self.output_path else self._get_b64_file_path()
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
