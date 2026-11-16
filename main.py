def greet(name):
    if not isinstance(name, str):
        raise TypeError("Name must be a string")
    clean_name = name.strip()

    if not clean_name:
        raise ValueError("Name cannot be empty")

    return f"Hello, {clean_name}!"


def main():
    user_name = input("What is your name? ")

    try:
        message = greet(user_name)
        print(message)

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()