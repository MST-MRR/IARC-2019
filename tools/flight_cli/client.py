import json
import logging
import socket
import sys

import requests

TCP_PORT = 5005
BUFFER_SIZE = 1024


def gen_req(s, command, **kwargs):
    message = json.dumps({"command": command, "meta": kwargs})
    s.send(message.encode())


def main():
    if len(sys.argv) < 2:
        logging.error("Please specify a host")
        sys.exit(1)

    TCP_HOST = sys.argv[1]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_HOST, TCP_PORT))

    while True:
        PARAMS = input("> ").split()
        try:
            COMMAND = PARAMS[0]
            if COMMAND == "exit":
                gen_req(s, COMMAND)
                s.shutdown(socket.SHUT_WR)
                s.close()
                return
            elif COMMAND == "land":
                gen_req(s, COMMAND, priority=PARAMS[1])
            elif COMMAND == "hover":
                gen_req(s, COMMAND, priority=PARAMS[2], time=PARAMS[1])
            elif COMMAND == "takeoff":
                gen_req(s, COMMAND, altitude=PARAMS[1])
            elif COMMAND == "move":
                gen_req(
                    s,
                    COMMAND,
                    priority=PARAMS[3],
                    direction=PARAMS[1],
                    time=PARAMS[2])
            else:
                logging.warning("Not a command. Try again.")
            data = s.recv(BUFFER_SIZE)
            if not data:
                raise Exception
        except Exception as err:
            logging.error(err)


if __name__ == "__main__":
    main()
