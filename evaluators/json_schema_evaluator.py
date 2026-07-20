import json
from typing import Any
from .base import BaseEvaluator

class JsonSchemaEvaluator(BaseEvaluator):
    def evaluate(self, response: str, schema: dict) -> bool:
        """Validates that the response is valid JSON and conforms to a simple schema."""
        try:
            # Extract JSON from markdown if present
            clean_response = response.strip()
            if clean_response.startswith("```"):
                lines = clean_response.splitlines()
                content = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
                clean_response = content.strip()

            data = json.loads(clean_response)
        except Exception:
            return False

        return self._validate(data, schema)

    def _validate(self, data: Any, schema: dict) -> bool:
        # Check type
        expected_type = schema.get("type")
        if expected_type == "object":
            if not isinstance(data, dict): return False
            
            # Check required properties
            for req in schema.get("required", []):
                if req not in data: return False
            
            # Check properties
            props = schema.get("properties", {})
            for key, value in data.items():
                if key in props:
                    if not self._validate(value, props[key]):
                        return False
                # If property is not in schema, we allow it (non-strict)

        elif expected_type == "array":
            if not isinstance(data, list): return False
            item_schema = schema.get("items")
            if item_schema:
                for item in data:
                    if not self._validate(item, item_schema):
                        return False

        elif expected_type == "string":
            if not isinstance(data, str): return False

        elif expected_type == "integer":
            if not isinstance(data, int): return False

        # Check constant value
        if "const" in schema:
            if data != schema["const"]:
                return False

        return True
