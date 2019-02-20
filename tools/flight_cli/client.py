import json
import logging
import socket
import sys

BUFFER_SIZE = 1024


def gen_req(sock, command, **kwargs):
    message = json.dumps({"command": command, "meta": kwargs})
    sock.send(message.encode())


def main():
    if len(sys.argv) < 3:
        logging.error("Please specify a host and port")
        sys.exit(1)

    tcp_host = sys.argv[1]
    tcp_port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((tcp_host, tcp_port))

    while True:
        params = input("> ").split()
        try:
            command = params[0]
            logging.info(command)
            if command == "exit":
                gen_req(sock, command)
                sock.shutdown(socket.SHUT_WR)
                sock.close()
                return
            elif command == "land":
                gen_req(sock, command, priority=params[1])
            elif command == "hover":
                gen_req(sock, command, priority=params[2], time=params[1])
            elif command == "takeoff":
                gen_req(sock, command, altitude=params[1])
            elif command == "move":
                gen_req(
                    sock,
                    command,
                    priority=params[3],
                    direction=params[1],
                    time=params[2])
            else:
                print("Not a command. Try again.")
                logging.warning("Not a command. Try again.")

            print("Sent command")
            logging.info("Sent")
            data = sock.recv(BUFFER_SIZE)
            if not data:
                print("No data recieved")
                logging.error("No data recieved")
            elif data == b"Success":
                print(data)
                logging.info(data)
            else:
                print("Session ended:", data)
                logging.info("Session ended")
                return

        except IndexError:
            print("Bad input")
            logging.error("Malformed input, try again.")
        except Exception as err:
            print("Kill", str(err))
            logging.error("Kill " + err)
            gen_req(sock, "exit")
            sock.shutdown(socket.SHUT_WR)
            sock.close()


if __name__ == "__main__":
    main()
