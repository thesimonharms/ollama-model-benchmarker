import re
from .base import BaseEvaluator

class RegexEvaluator(BaseEvaluator):
    def evaluate(self, response: str, expected: str) -> bool:
        """Checks if the response matches the regex pattern."""
        # Clean response of common markdown wrappers for better matching
        clean_response = response.strip()
        if clean_response.startswith("```"):
            # Extract content inside block
            lines = clean_response.splitlines()
            content = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
            clean_response = content.strip()

        return bool(re.search(expected, clean_response, re.MULTILINE | re.DOTALL))
