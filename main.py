import logging
import logging.config
import os
from time import perf_counter
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Python Service to accept addresses and return the states they reside in.')
    parser.add_argument('api-key', type=str, help='Google API key necessary to use their geocoding API')
    return parser.parse_args()


if __name__ == "__main__":
    # Create Logs
    logfile = os.path.join('logs', 'logging_file.log')
    print(logfile)
    if not os.path.isdir('logs'):
        os.makedirs('logs')
    logging.config.fileConfig('logging.conf', defaults={'logfile': logfile})
    logging.debug("Starting main")
    # Get args
    args = parse_args()


