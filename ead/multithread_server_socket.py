import socket
import threading
from deitel_comm import User, Group, Message

clients = {}
grupo_1 = Group("grupo 1")

def handle_client(client_sock):
    try:
        name = client_sock.recv(1024).decode('utf-8')
        user = User(name, client_sock)
        clients[name] = user

        print(f"{name} entrou no chat.")
        broadcast(f"{name} entrou no chat.", user)

        while True:
            msg = client_sock.recv(1024).decode('utf-8')
            if not msg:
                break

            if msg.startswith("/msg"):
                parts = msg.split(" ", 2)
                if len(parts) < 3:
                    user.receive_message(Message("Sistema", "Formato: /msg [usuario] [mensagem]"))
                    continue
                recipient_name, message = parts[1], parts[2]
                if recipient_name in clients:
                    user.send_message(clients[recipient_name], message)
                else:
                    user.receive_message(Message("Sistema", "Usuário não encontrado."))

            elif msg.startswith("/all"):
                content = msg[5:]
                broadcast(f"{user.name}: {content}", user)

            elif msg == "/grupo entrar":
                grupo_1.add_user(user)
                user.receive_message(Message("Sistema", "Você entrou no grupo 1."))

            elif msg.startswith("/grupo msg"):
                if user in grupo_1.users:
                    group_message = msg[11:]
                    grupo_1.broadcast_message(user.name, group_message)
                else:
                    user.receive_message(Message("Sistema", "Você precisa entrar no grupo primeiro (/grupo entrar)."))

            else:
                user.receive_message(Message("Sistema", "Comando não reconhecido."))

    except:
        pass

    print(f"{user.name} saiu do chat.")
    broadcast(f"{user.name} saiu do chat.", user)
    del clients[user.name]
    grupo_1.users = [u for u in grupo_1.users if u.name != user.name]
    client_sock.close()

def broadcast(message, sender=None):
    for user in clients.values():
        if user != sender:
            user.receive_message(Message("Sistema", message))

def main():
    host = ''
    port = 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print("Servidor iniciado em", port)

    while True:
        client_sock, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    main()
