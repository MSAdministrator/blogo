"""Command-line interface."""
import fire

from .blogo import Blogo


def main():
    fire.Fire(Blogo)


if __name__ == "__main__":
    main()
