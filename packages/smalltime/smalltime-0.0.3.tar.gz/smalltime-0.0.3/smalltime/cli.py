import argparse
import subprocess
import sys

import smalltime


class UsageError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def main() -> None:
    parser = argparse.ArgumentParser(description="Time a program")
    parser.add_argument("--name", type=str, required=False, help="An identifier for the timer.")
    args = parser.parse_args()
    if not len(sys.argv) > 1:
        parser.print_usage()
        raise UsageError(
            "You must provide the name (and optionally arguments of a program to time.)"
        )
    timer = smalltime.Timer(name=args.name if args.name else None)
    timer.start()
    subprocess.call(sys.argv[1:])
    timer.stop()
