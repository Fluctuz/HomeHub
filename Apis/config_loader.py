import os
import json


def load_config():
    config_filename = "config.json"
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, config_filename), 'r') as f:
        return json.load(f)


