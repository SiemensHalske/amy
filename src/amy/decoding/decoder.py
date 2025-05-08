import base64
from dataclasses import dataclass

from amy.utils import Logger, FileInfo, FileValidator, ConfigNamespace


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
    _instance: 'Base64FileDecoder' = None
    environment: ConfigNamespace = None

    file: FileInfo = None
    logger: Logger = Logger()

    def __new__(cls):
        """
        Singleton pattern to ensure only one instance exists.

        Must **NOT** use _init
        """

        if not cls._instance:
            cls._instance = super(Base64FileDecoder, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def set_environment(self, environment: ConfigNamespace) -> None:
        """Sets the environment variables."""
        self.environment = environment
        self.startup()

    def __init__(self) -> None:
        pass

    def startup(self) -> None:
        """Initializes the decoder with file paths. NOT used in __new__."""
        if not self.environment:
            raise ValueError("Environment variables are not set.")

        b64_file_path = self.environment.file

        output_path = self.environment.output
        output_path = output_path if output_path else self._get_original_file_path(
            b64_file_path)

        FileValidator.validate_file(b64_file_path)
        FileValidator.validate_file(output_path)

        self.file = FileInfo(b64_file_path, output_path)

    def _get_original_file_path(self, b64_file_path: str) -> str:
        """Generates the output file path by removing the .b64 extension."""
        if b64_file_path.endswith('.b64'):
            return b64_file_path[:-4]
        raise ValueError(
            f"File '{b64_file_path}' does not have a valid '.b64' extension.")

    def decode(self) -> None:
        """Main method to decode the Base64 file."""

        if not self.file:
            raise ValueError("File paths are not set.")

        try:
            # Perform decoding
            data = self._read_file(self.file.input_path)
            original_data = Base64Decoder.decode(data)
            self._write_file(self.file.output_path, original_data)

            self.logger.log_summary(file=self.file, mode="decoded")
        except Exception as err:  # pylint: disable=broad-except
            self.logger.error(f"Error: {err}", stacklevel=2)

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
