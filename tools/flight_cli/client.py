import json
import logging
import socket
import sys

BUFFER_SIZE = 1024


def set_keepalive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)


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
    set_keepalive_linux(sock, max_fails=2)
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
