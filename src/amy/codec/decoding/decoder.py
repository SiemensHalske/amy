from dataclasses import dataclass

from amy.codec.base import FileCodec


@dataclass
class Base64FileDecoder(FileCodec):
    """Main class to orchestrate the Base64 file decoding process."""

    def __post_init__(cls):
        pass
