# Python CLI & OpenRouter API Integration

A Python project combining OpenRouter API integration, command-line tools, HTTP request handling, automated testing, and AI-assisted development with OpenCode.

## Features

- OpenRouter API integration using Python's `urllib.request`
- OpenRouter Python SDK integration
- Command-line interface built with `argparse`
- Interactive and CLI-based AI requests
- HTTP GET and POST operations
- JSON request and response handling
- Input validation and error handling
- HTTP 429 retry logic with exponential backoff
- API token usage monitoring
- Automated testing with pytest
- Secure API key handling through environment variables

## Technologies

- **Python 3.14**
- **OpenRouter API**
- **OpenRouter Python SDK**
- **OpenCode**
- **pytest**
- **Git**
- **argparse**
- **urllib.request**
- **JSON**

## Installation

Clone the repository:

```bash
git clone https://github.com/Fritaja/python-cli-openrouter.git
cd python-cli-openrouter
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```


## Configuration

The OpenRouter API client reads its API key from the `OPENROUTER_API_KEY` environment variable.

### Setting the API Key

On macOS or Linux, run the following commands in the terminal:

```bash
read -s "OPENROUTER_API_KEY?Paste your OpenRouter API key: "
export OPENROUTER_API_KEY
```

This allows you to enter your API key without displaying it in the terminal or saving it in shell history.

Never commit real API keys to Git.

The examples use `recursive/flint-v1.0:free`. Model availability and usage limits depend on OpenRouter.

## Usage

### Interactive AI Client

Run the application:

```bash
python ask_ai.py
```

Enter a question when prompted.

### Command-Line AI Requests

Pass a question directly from the terminal:

```bash
python ask_ai.py --question "Explain Python in one sentence."
```

Display the available commands:

```bash
python ask_ai.py --help
```

### OpenRouter SDK

Run the SDK integration example:

```bash
python sdk_example.py
```

### CLI Arguments

```bash
python cli_example.py --name Ivan
```

### HTTP Request Examples

```bash
python demo_api.py
python demo_post.py
```

## Error Handling and Retry Logic

The OpenRouter client handles HTTP errors and connection failures.

For HTTP 429 responses, it uses exponential backoff with a maximum of three total attempts:

- First retry after 1 second
- Second retry after 2 seconds
- Stop after the third failed attempt

Other HTTP errors, including 401 Unauthorized, are not automatically retried.

The client also reports model information, token usage, and response completion status.

## Automated Testing

Run the complete test suite:

```bash
python -m pytest -v
```

**48 automated tests passing.**

The test suite covers:

- Input validation and exception handling
- CLI arguments and interactive input
- HTTP request construction
- API success and failure responses
- Retry limits and exponential backoff
- Missing API keys and empty questions
- Handling incomplete or missing AI responses

API calls and retry delays are mocked during testing to avoid external requests and unnecessary waiting.

## Project Structure

| File | Description |
|---|---|
| `ask_ai.py` | OpenRouter API client with CLI support and retry handling |
| `sdk_example.py` | OpenRouter Python SDK integration |
| `cli_example.py` | CLI argument handling |
| `demo_api.py` | HTTP GET request |
| `demo_post.py` | HTTP POST request |
| `retry_example.py` | Exponential backoff implementation |
| `main.py` | Input validation and exception handling |
| `test_ask_ai.py` | API client and CLI tests |
| `test_cli_example.py` | CLI behavior tests |
| `test_retry_example.py` | Retry calculation tests |
| `test_main.py` | Input validation tests |
| `opencode.json` | OpenCode permission configuration |
| `requirements.txt` | Python dependencies |

## Development Workflow

OpenCode was used for AI-assisted code development and review.

The development workflow included:

1. Defining requirements and expected behavior.
2. Analyzing proposed implementations using OpenCode Plan mode.
3. Implementing approved changes using Build mode.
4. Reviewing source code changes with Git.
5. Running automated tests and manually validating functionality.
6. Committing verified changes to version control.

This workflow combines AI-assisted development with code review, testing, and controlled changes.

## Security

- API keys are accessed through environment variables.
- Environment files and virtual environments are excluded through `.gitignore`.
- OpenCode permissions are configured to require approval.
- API requests use timeouts and output-token limits.
- Retry attempts are limited to prevent uncontrolled repeated requests.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.