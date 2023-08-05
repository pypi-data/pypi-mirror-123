import argparse
from collections import namedtuple
from getpass import getpass
import json
from pathlib import Path

import appdirs
import requests


DEFAULT_ENDPOINT_URL = "https://strutern.raek.se/api/run-command"


Config = namedtuple("Config", "endpoint_url, api_token")


class RunError(Exception):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("script", help="Script to run, given as a single argument. Example: \"echo hello\"")
    args = parser.parse_args()
    config_path = Path(appdirs.user_config_dir()) / "pladder-client" / "config.json"
    config = read_config(config_path)
    print(run_script(args.script, config))


def read_config(path):
    if not path.exists():
        setup_config(path)
    with path.open(encoding="utf-8") as f:
        json_config = json.load(f)
    return Config(**json_config)


def setup_config(path):
    print(f'A configuration file does not exist at "{path}". Starting setup wizard.')
    while True:
        print()
        print(f"Endpoint URL [{DEFAULT_ENDPOINT_URL}]: ", end="")
        endpoint_url = input() or DEFAULT_ENDPOINT_URL
        print("API Token (16 character string): ", end="")
        api_token = input()
        config = Config(endpoint_url, api_token)
        print("Testing credentials... ", end="")
        try:
            run_script("echo test", config)
            print("OK!")
            break
        except RunError as e:
            print(f"Failed: {e}")
            print("Check credentials and try again.")
    write_config(config, path)
    print(f'Wrote config to "{path}".')
    print()


def write_config(config, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(config._asdict(), f)


def run_script(script, config):
    headers = {
        "X-Pladder-Token": config.api_token,
        "Content-Type": "text/plain; charset=utf-8",
    }
    try:
        response = requests.post(config.endpoint_url, data=script.encode("utf-8"), headers=headers)
    except Exception as e:
        raise RunError(str(e)) from None
    if response.status_code == 200:
        return(response.text)
    else:
        raise RunError(response.text)
