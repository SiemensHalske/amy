import base64
from dataclasses import dataclass

from amy.utils import Logger, FileInfo, FileValidator


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
            self.logger.log_summary(original_file, b64_file)
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
