import logging
import socket
import sys

from commands import COMMANDS, MAPPINGS, HEX

BUFFER_SIZE = 1024


'''def set_keepalive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)
'''

def main():
    if len(sys.argv) < 3:
        logging.error("Please specify a host and port")
        sys.exit(1)

    tcp_host = sys.argv[1]
    tcp_port = int(sys.argv[2])

    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #set_keepalive_linux(sock, max_fails=2)
    # sock.connect((tcp_host, tcp_port))

    while True:
        params = input("> ").split()
        #try:
        query = ""
        command = params[0]
        count = 1
        logging.info(command)
        for index, com in enumerate(COMMANDS):
            com = com()
            print(command.upper(), com.name)
            if command.upper() == com.name:
                query += str(index)
                req_params = com.required_params
                print(req_params)
                for param in req_params:
                    if param in MAPPINGS:
                        print(MAPPINGS, params, count)
                        query += MAPPINGS[param][params[count].upper()]
                    else:
                        query += HEX[params[count]]
                    count += 1
                    print(query)
                return
        """
                exit
                sock.shutdown(socket.SHUT_WR)
                sock.close()
                return
            print("Sent command")
            logging.info("Sent")
            # data = sock.recv(BUFFER_SIZE)
        except Exception as err:
            print("Kill", str(err))
            logging.error("Kill " + str(err))
            # sock.shutdown(socket.SHUT_WR)
            # sock.close()
        """


if __name__ == "__main__":
    main()
