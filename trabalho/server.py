import socket
import threading
from messaging import Proxy, MsgQMgr

HOST = 'localhost'
PORT = 5555

msg_mgr = MsgQMgr()

def handle_client(conn, addr):
    try:
        conn.sendall("Digite seu nome: ".encode())
        name = conn.recv(1024).decode().strip()
        proxy = Proxy(conn, addr, name)
        msg_mgr.add_client(proxy)

        print(f"[+] {name} conectado de {addr}")
        msg_mgr.broadcast(proxy, f"{name} entrou no chat.")

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            if data.startswith("/msg"):
                _, target_name, msg = data.split(" ", 2)
                msg_mgr.send_to(proxy, target_name, msg)
                
            elif data.startswith("/canal_msg"):
                _, msg = data.split(" ", 1)
                msg_mgr.send_to_channel(proxy, msg)

            elif data.startswith("/canal"):
                _, channel = data.split(" ", 1)
                proxy.channel = channel
                proxy.send(f"[Sistema] Você entrou no canal {channel}")
            
            else:
                msg_mgr.broadcast(proxy, data)
    except:
        pass
    finally:
        msg_mgr.remove_client(proxy)
        msg_mgr.broadcast(proxy, f"{proxy.name} saiu.")
        conn.close()
        print(f"[-] {proxy.name} desconectado de {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor iniciado em {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()
