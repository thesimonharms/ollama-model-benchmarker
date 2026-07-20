import subprocess
import os
from .base import BaseEvaluator

class UnitTestEvaluator(BaseEvaluator):
    def evaluate(self, response: str, test_script_name: str) -> bool:
        """Executes the model's code against a provided test script."""
        # Extract code from markdown
        clean_response = response.strip()
        if clean_response.startswith("```"):
            lines = clean_response.splitlines()
            content = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
            clean_response = content.strip()

        # Save model code to a temp file (model_solution.py)
        sol_path = "tests_output/model_solution.py"
        os.makedirs("tests_output", exist_ok=True)
        with open(sol_path, "w") as f:
            f.write(clean_response)

        # The test script is expected to be in the 'suite' or specialized folder
        test_path = os.path.join("tests_output", test_script_name)
        # We need to copy the predefined test script to tests_output so it can import model_solution
        with open(f"suite/{test_script_name}", "r") as f:
            test_content = f.read()
        
        with open(test_path, "w") as f:
            f.write(test_content)

        # Run the test script
        try:
            result = subprocess.run(
                ["python", test_path], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Test execution error: {e}")
            return False
