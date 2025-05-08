import base64
from dataclasses import dataclass

from amy.utils import Logger, FileInfo, FileValidator, ConfigNamespace


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
    _instance = None
    environment: ConfigNamespace = None

    file: FileInfo = None
    logger: Logger = Logger()

    def __new__(cls):
        """
        Singleton pattern to ensure only one instance exists
        using the __init__ method once with both file paths.
        """
        if cls._instance is None:
            cls._instance = super(Base64FileEncoder, cls).__new__(cls)
        return cls._instance

    def set_environment(self, environment: ConfigNamespace) -> None:
        """Sets the environment variables."""
        self.environment = environment
        self.startup()

    def startup(self) -> None:
        """Initializes the encoder with file paths."""
        if not self.environment:
            raise ValueError("Environment variables are not set.")

        file_path = self.environment.file

        output_path = self.environment.output
        output_path = output_path if output_path else self._get_b64_file_path(
            file_path)

        self.logger.info(f"Encoding file: {file_path}")
        self.logger.info(f"Output file: {output_path}")

        FileValidator.validate_file(file_path)
        FileValidator.validate_file(output_path)

        self.file = FileInfo(file_path, output_path)

        # print the content of the file
        self.logger.debug(f"File: {self.file.to_dict()}")

    def encode(self) -> None:
        """Main method to encode the file to Base64."""
        try:
            # Perform encoding
            file_data = self._read_file(self.file.input_path)
            b64_data = Base64Encoder.encode(file_data)
            self._write_file(self.file.output_path, b64_data)

            # Log success
            self.logger.log_summary(file=self.file, mode="encoded")
        except Exception as err:  # pylint: disable=broad-except
            self.logger.error(f"Error: {err}")

    def _get_b64_file_path(self, file_path: str) -> str:
        """Generates the output file path with a .b64 extension."""
        return f"{file_path}.b64"

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
