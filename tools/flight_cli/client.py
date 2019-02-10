import logging
import sys

import requests

if len(sys.argv) < 2:
    logging.error("Please specify a host")
    sys.exit(1)

URL = 'http://{}/commands/'.format(sys.argv[1])


def gen_req(command, **kwargs):
    resp = requests.post(URL, data={"command": command, "meta": kwargs})
    if resp.status_code != requests.codes.ok:
        logging.error(resp.text)


while True:
    PARAMS = input("> ").split()
    try:
        COMMAND = PARAMS[0]
        if COMMAND == "exit":
            gen_req(COMMAND)
        elif COMMAND == "land":
            gen_req(COMMAND, priority=PARAMS[1])
        elif COMMAND == "hover":
            gen_req(COMMAND, priority=PARAMS[2], time=PARAMS[1])
        elif COMMAND == "takeoff":
            gen_req(COMMAND, altitude=PARAMS[1])
        elif COMMAND == "move":
            gen_req(
                COMMAND,
                priority=PARAMS[3],
                direction=PARAMS[1],
                time=PARAMS[2])
        else:
            logging.warning("Not a command. Try again.")
    except Exception as err:
        logging.error(err)
