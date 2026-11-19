import os
from openrouter import OpenRouter


def main():
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("Error: OpenRouter API key is missing.")
        return

    with OpenRouter(api_key=api_key) as client:
        response = client.chat.send(
            model="recursive/flint-v1.0:free",
            messages=[
                {
                    "role": "user",
                    "content": "What is Python? Answer in one short sentence."
                }
            ],
            max_tokens=300,
            stream=False,
        )

        print("AI response:")
        print(response.choices[0].message.content)

        answer = response.choices[0].message.content

        print("AI response:")

        if answer is None:
            print("No text response received from the model.")
        else:
            print(answer)

        print("\n--- Request information ---")
        print("Model:", response.model)
        print("Finish reason:", response.choices[0].finish_reason)
        print("Token usage:", response.usage)


if __name__ == "__main__":
    main()
