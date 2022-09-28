# Copyright: (c) 2022, MSAdministrator <rickardja@live.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

"""Command-line interface."""

import fire

from .blogo import Blogo


def main():
    """Main entry point for the command line interface of blogo."""
    fire.Fire(Blogo)


if __name__ == "__main__":
    main()
