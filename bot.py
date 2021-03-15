import argparse

DEFAULT_CHROME_VERSION = 89

def main(*args):
    parser = argparse.ArgumentParser(description='Book time slots for grr in accordance to schedule.')
    parser.add_argument(
        '--chrome-version', '-v',
        metavar='V',
        type=int,
        help='Version of chrome being used, defaults to 89.'
    )
    args = parser.parse_args()
    if args.chrome_version is None:
        args.chrome_version = DEFAULT_CHROME_VERSION

if __name__ == '__main__':
    main()