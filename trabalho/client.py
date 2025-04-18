import socket
import threading

HOST = 'localhost'
PORT = 5555

def receive(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if data:
                print(data)
        except:
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        print(s.recv(1024).decode())
        name = input("> ")
        s.sendall(name.encode())

        threading.Thread(target=receive, args=(s,), daemon=True).start()

        while True:
            msg = input()
            if msg.lower() == "sair":
                break
            s.sendall(msg.encode())

if __name__ == "__main__":
    main()
