"""Console script for tuttusa_utils."""

import fire

def help():
    print("tuttusa_utils")
    print("=" * len("tuttusa_utils"))
    print("Utils for Tuttusa")

def main():
    fire.Fire({
        "help": help
    })


if __name__ == "__main__":
    main() # pragma: no cover
