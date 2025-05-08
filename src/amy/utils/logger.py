from rich.console import Console
from rich.table import Table

from .file_info import FileInfo


class Logger:
    """Handles logging functionality using Rich."""

    def __init__(self, display: Console = Console()):
        self.console = display

    def log_summary(self, original_file: FileInfo, b64_file: FileInfo) -> None:
        """Logs encoding summary using a table."""
        try:
            table = Table(title="File Encoding Summary")
            table.add_column(
                "File", justify="left",
                style="cyan", no_wrap=True
            )
            table.add_column("Size (bytes)", justify="right", style="magenta")
            table.add_column("SHA256 Hash", justify="left", style="green")

            table.add_row(original_file.path, str(
                original_file.size), original_file.sha256_hash)
            table.add_row(b64_file.path, str(
                b64_file.size), b64_file.sha256_hash)

            self.console.print(table)
            self.console.print(
                f"[bold green]File '{original_file.path}' has been successfully "
                f"encoded to '{b64_file.path}'.[/bold green]"
            )
        except Exception as err:  # pylint: disable=broad-except
            self.console.print(f"[red]Logging Error:[/red] {err}")

    def __str__(self) -> str:
        return "Logger"

    def __repr__(self) -> str:
        return self.__str__()
