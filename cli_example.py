import argparse


def main():
    parser = argparse.ArgumentParser(
        description="A simple greeting CLI program"
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Name of the person to greet"
    )

    args = parser.parse_args()

    print(f"Hello, {args.name}!")


if __name__ == "__main__":
    main()
