import logging
from typing import Any

from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from rich.traceback import install

from .file_info import FileInfo

# Install rich traceback for better debugging
install(extra_lines=5)


class Logger:
    """Handles logging functionality using RichHandler and Console."""

    _instance: "Logger" = None
    logger: logging.Logger = None
    handler: RichHandler = None
    console: Console = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure only one instance of Logger exists."""
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self, level: int = logging.INFO):
        # Configure the logger
        self.logger = logging.getLogger("rich_logger")
        self.logger.setLevel(level)

        # Define the log format to include line numbers
        log_format = "%(levelname)s: %(message)s (%(pathname)s:%(lineno)d)"
        self.handler = RichHandler(rich_tracebacks=True, console=Console())
        self.handler.setFormatter(logging.Formatter(log_format))

        self.logger.addHandler(self.handler)

        # Create a Console instance for direct styled output
        self.console = Console()

    def log_summary(self, file: FileInfo, mode: str = "encoded") -> None:
        """Logs encoding summary using RichHandler."""
        try:
            input_hash, output_hash = file.sha256_hash()

            # Create the summary table
            table = Table(title="File Encoding Summary")
            table.add_column("File", justify="left",
                             style="cyan", no_wrap=True)
            table.add_column("Size (bytes)", justify="right", style="magenta")
            table.add_column("SHA256 Hash", justify="left", style="green")

            table.add_row(file.input_path, str(file.size), input_hash)
            table.add_row(file.output_path, str(file.size), output_hash)

            # Print the summary table directly to the console
            self.console.print(table)

            # Log the success message
            self.info(
                f"File '{file.input_path}' has been successfully "
                f"{mode} to '{file.output_path}'",
                style="bold green",
            )
        except Exception as err:  # pylint: disable=broad-except
            self.error(f"Logging Error from summary: {err}")

    def log(self, message: Any = "", style: str = "") -> None:
        """Logs a message to the console with optional styling."""
        try:
            if style:
                self.console.print(f"[{style}]{message}[/{style}]")
            else:
                self.console.print(message)
        except Exception as err:  # pylint: disable=broad-except
            self.error(f"Logging Error: {err}")

    def debug(self, message: Any = "", style: str = "bold yellow") -> None:
        """Logs a debug message to the console with optional styling."""
        try:
            if style:
                self.console.print(f"[{style}]DEBUG: {message}[/{style}]")
            else:
                self.logger.debug(message)
        except Exception as err:  # pylint: disable=broad-except
            self.error(f"Logging Error: {err}")

    def info(self, message: Any = "", style: str = "bold blue") -> None:
        """Logs an info message to the console with optional styling."""
        try:
            if style:
                self.console.print(f"[{style}]INFO: {message}[/{style}]")
            else:
                self.logger.info(message)
        except Exception as err:  # pylint: disable=broad-except
            self.error(f"Logging Error: {err}")

    def warning(self, message: Any = "", style: str = "bold yellow", stacklevel: int = 2) -> None:
        """Logs a warning message to the console with optional styling."""
        try:
            if style:
                self.console.print(f"[{style}]WARNING: {message}[/{style}]")
            else:
                self.logger.warning(message, stacklevel=stacklevel)
        except Exception as err:  # pylint: disable=broad-except
            self.error(f"Logging Error: {err}")

    def error(self, message: Any = "", style: str = "bold red", stacklevel: int = 2) -> None:
        """Logs an error message to the console with optional styling."""
        try:
            if style:
                self.console.print(f"[{style}]ERROR: {message}[/{style}]")
            else:
                self.logger.error(message, stacklevel=stacklevel)
        except Exception as err:  # pylint: disable=broad-except
            self.logger.error(f"Logging Error: {err}")

    def __str__(self) -> str:
        return "Logger"

    def __repr__(self) -> str:
        return self.__str__()
