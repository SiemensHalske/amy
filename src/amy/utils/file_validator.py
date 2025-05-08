import os


class FileValidator:
    """Handles file validation logic."""
    @staticmethod
    def validate_file(file_path: str) -> None:
        """Validates the file existence and checks if it's non-empty."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")
        if os.path.getsize(file_path) == 0:
            raise ValueError(f"File '{file_path}' is empty.")

    def __str__(self) -> str:
        return "FileValidator"

    def __repr__(self) -> str:
        return self.__str__()
