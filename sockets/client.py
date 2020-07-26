import socket
import sys


def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8000
    try:
        soc.connect((host, port))
    except:
        print("Connection Error")
        sys.exit()
    print("Please enter 'quit' to exit")
    message = input(" -> ")
    while message != 'QUIT':
        soc.sendall(message.encode("utf8"))
        data = soc.recv(5120).decode("utf8")
        if data == "-":
            pass  # null operation
        else:
            print(data)
        message = input(" -> ")
    soc.send(b'--quit--')


if __name__ == "__main__":
    main()
