from pathlib import Path
from typing import List, Optional, Union


class ValidationMixin:
    """Handles input validation."""

    supported_formats: List[str]

    def validate_input_files(
        self,
        input_paths: List[Union[str, Path]],
        required_count: Optional[int] = None,
    ) -> bool:
        if not input_paths:
            self.log_error("No input paths provided")
            return False

        if required_count and len(input_paths) < required_count:
            self.log_error(f"Need {required_count}, got {len(input_paths)}")
            return False

        for path in input_paths:
            path = Path(path)

            if not path.exists():
                self.log_error(f"Missing file: {path}")
                return False

            if path.suffix.lower() not in self.supported_formats:
                self.log_error(f"Unsupported type: {path.suffix}")
                return False

        return True