from typing import Optional

class CatSessionError(Exception):
    pass

class CatExplorerError(Exception):
    pass

class OpenDataSoftExplorerError(Exception):
    """
    Custom exception class for OpenDataSoft Explorer errors with colored output using ANSI codes.
    """
    # ANSI escape codes for colors
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        self.message = message
        self.original_error = original_error

        # Build the error message with color
        error_msg = (
            f"{self.RED}OpenDataSoftExplorer Error: {message}{self.RESET}"
        )

        if original_error:
            error_msg += (
                f"\n{self.YELLOW}Original error: "
                f"{str(original_error)}{self.RESET}"
            )

        super().__init__(error_msg)

    def __str__(self) -> str:
        return self.args[0]
