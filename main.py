import logging
import logging.config
import os
from time import perf_counter
import argparse
from flask import Flask
from flask import request, jsonify

ADDRESS_ARG = 'address'


def parse_args():
    parser = argparse.ArgumentParser(description='Python Service to accept addresses and return the states they reside in.')
    parser.add_argument('api_key', type=str, help='Google API key necessary to use their geocoding API')
    return parser.parse_args()


def start_flask(command_args):
    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_object('config')
    flask_app.config['api_key'] = command_args.api_key

    @flask_app.route('/search_address', methods=['GET'])
    def geocode_address():
        if ADDRESS_ARG in request.args:
            address = request.args[ADDRESS_ARG]
        else:
            return "ERROR: Address not found. Please provide an address"

        return "Nothing has been implemented!"
    return flask_app


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
    print(args.api_key)
    app = start_flask(args)
    app.run()
    print("app running")

