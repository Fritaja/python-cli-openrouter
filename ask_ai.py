import argparse
import json
import os
import time
import urllib.error
import urllib.request

from retry_example import calculate_delay


def is_response_incomplete(finish_reason):
    return finish_reason == "length"


def ask_model(question, api_key):
    url = "https://openrouter.ai/api/v1/chat/completions"

    data = {
        "model": "recursive/flint-v1.0:free",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "max_completion_tokens": 300
    }

    max_attempts = 3

    json_data = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=json_data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    for attempt in range(max_attempts):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))

        except urllib.error.HTTPError as error:
            print("HTTP Error:", error.code)
            if error.code != 429 or attempt == max_attempts - 1:
                return None

            delay = calculate_delay(attempt)
            print(f"Retrying after {delay}s...")
            time.sleep(delay)

        except urllib.error.URLError as error:
            print("Connection Error:", error.reason)
            return None

    return None


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Ask an AI model a question using OpenRouter."
    )
    parser.add_argument(
        "--question",
        help="Question to ask. If omitted, the program asks interactively."
    )
    args = parser.parse_args(argv)

    question = None
    if args.question is not None:
        question = args.question.strip()
        if not question:
            raise SystemExit("Error: Question cannot be empty")

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise SystemExit("Error: API key is missing")

    if question is None:
        question = input("Ask AI: ").strip()

    if not question:
        raise SystemExit("Error: Question cannot be empty")

    result = ask_model(question, api_key)

    if result is None:
        return

    answer = result["choices"][0]["message"].get("content")

    model = result.get("model", "Unknown")
    usage = result.get("usage") or {}
    finish_reason = result["choices"][0].get("finish_reason")
    token_details = usage.get("completion_tokens_details") or {}

    print("AI response:")
    if answer is None:
        print("(No answer)")
    else:
        print(answer)

    print("\n--- Request information ---")
    print("Model:", model)
    print("Input tokens:", usage.get("prompt_tokens", "N/A"))
    print("Output tokens:", usage.get("completion_tokens", "N/A"))
    print("Total tokens:", usage.get("total_tokens", "N/A"))
    print("Finish reason:", finish_reason)
    print("Reasoning tokens:", token_details.get("reasoning_tokens", "N/A"))

    if is_response_incomplete(finish_reason):
        print("\nWARNING: AI response was cut off.")
        print("The model reached the token limit.")


if __name__ == "__main__":
    main()
