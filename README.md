# Ollama Code Benchmarker

Ollama Code Benchmarker is a tool designed to evaluate the coding capabilities of Large Language Models (LLMs) served via [Ollama](https://ollama.com/).

## Overview

The benchmarker runs a predefined suite of tests across various categories (e.g., refactoring, bug fixing, algorithmic implementation). Each test consists of:
- A **prompt** for the model.
- An **expected output**.
- An **evaluator** (Regex, JSON Schema, or Unit Test) that determines if the model's response is correct.

The tool provides a final score and a breakdown by category to help identify strengths and weaknesses in specific coding tasks.

## Getting Started

### Prerequisites

- [Ollama](https://ollama.com/) installed and running on your machine.
- Python 3.11+

### Installation

Clone the repository:

```bash
git clone <repository-url>
cd ollama-code-benchmarker
```

Install dependencies (if any, typically `requests` or similar for the Ollama API):

```bash
pip install -r requirements.txt
```
*(Note: If there is no requirements.txt, check the imports in `ollama_client.py`)*

### Usage

Run the benchmarker by specifying the model you want to test:

```bash
python main.py --model <model-name>
```

Example:

```bash
python main.py --model llama3
```

## Project Structure

- `main.py`: The entry point that manages the test loop and scoring.
- `ollama_client.py`: Wrapper for interacting with the Ollama API.
- `evaluators/`: Contains different evaluation strategies:
    - `BaseEvaluator`: Abstract base class.
    - `RegexEvaluator`: Matches output against a regular expression.
    - `JsonSchemaEvaluator`: Validates output against a JSON schema.
    - `UnitTestEvaluator`: Executes code to verify correctness via unit tests.
- `suite/tests.json`: The benchmark dataset containing prompts and expected results.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
