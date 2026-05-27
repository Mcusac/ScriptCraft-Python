import re

from typing import Dict, List, Optional, Tuple


class PrivacyClassifier:
    def __init__(self, healthcare_patterns: Dict):
        self.healthcare_patterns = healthcare_patterns

    def classify(self, col_name: str) -> Tuple[str, Optional[str], List[str], List[str]]:
        col_lower = col_name.lower().replace("_", " ").replace("-", " ")

        for pattern_name, info in self.healthcare_patterns.items():
            for pattern in info["patterns"]:
                if re.search(pattern, col_lower, re.IGNORECASE):
                    return (
                        info["privacy"],
                        pattern_name,
                        info["constraints"].copy(),
                        info["indexes"].copy(),
                    )

        if any(term in col_lower for term in ["id", "key", "number"]):
            return "internal", None, [], ["INDEX"]

        if any(term in col_lower for term in ["name", "address", "phone", "email"]):
            return "sensitive", None, [], []

        return "public", None, [], []