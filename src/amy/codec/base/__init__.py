import base64
from dataclasses import dataclass

from amy.utils import Logger, FileInfo, FileValidator, ConfigNamespace


class Codec:
    """Base class for all encoders."""

    @staticmethod
    def encode(data: bytes) -> bytes:
        """Encode the given data."""
        try:
            return base64.b64encode(data)
        except Exception as e:
            raise ValueError("Encoding failed") from e

    @staticmethod
    def decode(data: bytes) -> bytes:
        """Decode the given data."""
        try:
            return base64.b64decode(data)
        except Exception as e:
            raise ValueError("Decoding failed") from e

    def __str__(self):
        raise NotImplementedError("Subclasses must implement __str__ method.")

    def __repr__(self):
        return self.__str__()


class Base64Decoder(Codec):
    """Handles Base64 decoding logic."""

    def __str__(self) -> str:
        return "Base64Decoder"


class Base64Encoder(Codec):
    """Handles Base64 encoding logic."""

    def __str__(self) -> str:
        return "Base64Encoder"


class FileCodec:
    """Base class for all file encoders."""

    _instances = {}
    environment: ConfigNamespace = None

    file: FileInfo = None
    logger: Logger = Logger()
    mode: str = None

    def __new__(cls):
        instance = cls._instances.setdefault(cls, super().__new__(cls))
        instance.__init__()
        return instance

    @classmethod
    def set_environment(cls, environment: ConfigNamespace) -> None:
        """Sets the environment variables."""
        cls.environment = environment
        cls.startup()

    @classmethod
    def startup(cls) -> None:
        """Initializes the codec environment."""

        if not cls.environment:
            raise ValueError("Environment variables are not set.")

        cls.mode = cls.environment.mode

        input_file = cls.environment.file
        output_file = cls.environment.file

        output_file = output_file if output_file else cls._get_file_path(
            file=input_file, mode=cls.mode)

        FileValidator.validate_file(input_file)
        FileValidator.validate_file(output_file)

        cls.file = FileInfo(
            input_path=input_file,
            output_path=output_file
        )

    @classmethod
    def _get_file_path(cls, file: str, mode=""):
        """tbe"""

        if mode != "b64":
            return f"{file}.b64"

        if file.endswith('.b64'):
            return file[:-4]

        raise NotImplementedError(
            f"Mode {mode} not supported.")

    @classmethod
    def decode(cls) -> None:
        """Main method to decode the Base64 file."""

        if not cls.file:
            raise ValueError("File paths are not set.")

        try:
            # Perform decoding
            data = cls._read_file(cls.file.input_path)
            original_data = Base64Decoder.decode(data)
            cls._write_file(cls.file.output_path, original_data)

            cls.logger.log_summary(file=cls.file, mode="decoded")
        except Exception as err:  # pylint: disable=broad-except
            cls.logger.error(f"Error: {err}", stacklevel=2)

    @classmethod
    def encode(cls) -> None:
        """Main method to encode the file to Base64."""
        try:
            # Perform encoding
            file_data = cls._read_file(cls.file.input_path)
            b64_data = Base64Encoder.encode(file_data)
            cls._write_file(cls.file.output_path, b64_data)

            # Log success
            cls.logger.log_summary(file=cls.file, mode="encoded")
        except Exception as err:  # pylint: disable=broad-except
            cls.logger.error(f"Error: {err}")

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


__all__ = [
    "Codec",
    "FileCodec",
    "Base64Decoder",
    "Base64Encoder",
]
