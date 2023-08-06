"""Console script for tuttusa_proxy."""

import fire

def help():
    print("tuttusa_proxy")
    print("=" * len("tuttusa_proxy"))
    print("package for determining the protected based on a non protected attribute to help detect discrimination in decision systems")

def main():
    fire.Fire({
        "help": help
    })


if __name__ == "__main__":
    main() # pragma: no cover
