"""
Main module for fa.
"""
import argparse as ap
import logging


def parse_args():
    """"What it says on the can"""
    parser = ap.ArgumentParser(formatter_class=ap.ArgumentDefaultsHelpFormatter)

    log_levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    parser.add_argument(
        "--log_level", choices=log_levels, default="INFO", help="Possible log levels"
    )

    return parser.parse_args()


def main():
    """
    Main entry point for fa. This is responsible for setting up scaffolding like
    logging and command-line argument parsing. It generally doesn't contain significant
    application logic but rather redirects flow elsewhere after the basics of the program
    are set up and ready-to-go.
    """
    args = parse_args()
    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s %(levelname)8s: (%(threadName)s) %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    print("Hello, FlightAware!")


if __name__ == "__main__":
    main()
