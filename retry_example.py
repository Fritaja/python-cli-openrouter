def calculate_delay(attempt):
    return 2 ** attempt


def main():
    max_attempts = 3

    for attempt in range(max_attempts):
        print(f"Attempt {attempt + 1} of {max_attempts}")

        print("API Error: 429 Too Many Requests")

        if attempt == max_attempts - 1:
            print("Maximum attempts reached. Stopping.")
            break

        delay = calculate_delay(attempt)
        print(f"Wait {delay} seconds before retrying.")


if __name__ == "__main__":
    main()

