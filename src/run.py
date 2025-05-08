# pylint: disable=W0201
import argparse
from rich.prompt import Prompt

from amy.utils import Logger, ConfigNamespace
from amy.encoding import Base64FileEncoder
from amy.decoding import Base64FileDecoder


def parse_arguments() -> ConfigNamespace:
    """
    Parse command line arguments.
    """

    parser = argparse.ArgumentParser(
        description="Base64 File Encoder/Decoder CLI Tool")

    # Group for encoding and decoding
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--encode", "-e",
        action="store_true",
        help="Encode a file to Base64"
    )

    group.add_argument(
        "--decode", "-d",
        action="store_true",
        help="Decode a Base64 file"
    )

    parser.add_argument(
        "--file", "-f",
        type=str,
        help="Path to the file to be encoded or decoded"
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Path to save the output file (optional)"
    )

    args = parser.parse_args()

    env = ConfigNamespace()

    env.mode = "encode" if args.encode else "decode"
    env.file = args.file
    env.output = args.output

    return env


def preprocess(env: ConfigNamespace) -> None:
    """
    Preprocess the environment variables.
    """

    if not env.file:
        print(
            "File path is required. "
            "Please provide a valid file path."
        )
        env.file = Prompt.ask(
            "[bold yellow] QUESTION\n[/bold yellow] "
            "Please enter the file path"
        )


def main():
    """
    Main function to run the Base64 encoding/decoding process.
    """
    display = Logger()
    display.info(
        "Starting Base64 File Encoder/Decoder CLI Tool",
    )
    env = parse_arguments()

    preprocess(env)

    if env.mode == "encode":
        encoder = Base64FileEncoder()
        encoder.set_environment(env)
        encoder.encode()
    if env.mode == "decode":
        decoder = Base64FileDecoder()
        decoder.set_environment(env)
        decoder.decode()


if __name__ == "__main__":
    main()
