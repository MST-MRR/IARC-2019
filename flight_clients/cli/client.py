import logging
import sys

import requests

if len(sys.argv) < 2:
    logging.error("Please specify a host")
    sys.exit(1)

url = 'http://{}:8000/commands/'.format(sys.argv[1])


def gen_req(command, **kwargs):
    r = requests.post(url, data={"command": command, "meta": kwargs})
    if not (r.status_code == requests.codes.ok):
        logging.error(r.text)


while True:
    params = input("> ").split()
    try:
        command = params[0]
        if command == "exit":
            gen_req(command)
        elif command == "land":
            gen_req(command, priority=params[1])
        elif command == "hover":
            gen_req(command, priority=params[2], time=params[1])
        elif command == "takeoff":
            gen_req(command, altitude=params[1])
        elif command == "move":
            gen_req(
                command,
                priority=params[3],
                direction=params[1],
                time=params[2])
        else:
            logging.warning("Not a command. Try again.", e)
    except Exception as e:
        logging.error(e)
