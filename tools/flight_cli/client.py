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
        params = input("> ").split()
        try:
            command = params[0]
            if command == "exit":
                gen_req(s, command)
                s.shutdown(socket.SHUT_WR)
                s.close()
                return
            elif command == "land":
                gen_req(s, command, priority=params[1])
            elif command == "hover":
                gen_req(s, command, priority=params[2], time=params[1])
            elif command == "takeoff":
                gen_req(s, command, altitude=params[1])
            elif command == "move":
                gen_req(
                    s,
                    command,
                    priority=params[3],
                    direction=params[1],
                    time=params[2])
            else:
                logging.warning("Not a command. Try again.")
            data = s.recv(BUFFER_SIZE)
            if not data:
                raise Exception("No data recieved")
            elif data == "Success":
                logging.info(data)
            else:
                logging.info("Session ended")
                return

        except IndexError:
            logging.error("Malformed input, try again.")
        except Exception as err:
            logging.error(err)
            gen_req(s, "exit")
            s.shutdown(socket.SHUT_WR)
            s.close()


if __name__ == "__main__":
    main()
