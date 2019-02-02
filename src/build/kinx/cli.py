"""Kinx CLI
Usage:
    kinx build [-D|--dev] <path>
    kinx clean <path>
    kinx -H|--help
    kinx -V|--version
Options:
    <path>  Optional name argument.
    -H --help  Show this screen.
    -V --version  Show version.
    -D --dev  Development Mode
"""

from os import getcwd
from os.path import abspath

from docopt import docopt

from .main import Builder


def main():
    options = docopt(__doc__, version="1.0.0")
    # print(options)

    if not options["<path>"]:
        options["<path>"] = getcwd()

    options["<path>"] = abspath(options["<path>"])

    if options["build"]:
        Builder(options["<path>"], bool(options["--dev"])).build()

    if options["clean"]:
        pass
        # clean(options["<path>"])


if __name__ == "__main__":
    main()
