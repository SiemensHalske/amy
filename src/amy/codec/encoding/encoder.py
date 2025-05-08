from dataclasses import dataclass

from amy.codec.base import FileCodec


@dataclass
class Base64FileEncoder(FileCodec):
    """Main class to orchestrate the Base64 file encoding process."""

    def __post_init__(cls):
        pass
