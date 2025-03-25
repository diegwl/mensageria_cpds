import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if data:
                print("\n" + data)
        except:
            print("Erro ao receber mensagens.")
            break

def main():
    host = '127.0.0.1'
    port = 12345

    name = input("Digite seu nome: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # Envia o nome do usuário ao servidor
    sock.send(name.encode('utf-8'))

    # Thread para receber mensagens
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    print("\nComandos disponíveis:")
    print("/msg [usuario] [mensagem] - enviar mensagem privada")
    print("/all [mensagem] - enviar para todos")
    print("/grupo entrar - entrar no grupo 1")
    print("/grupo msg [mensagem] - enviar mensagem ao grupo")
    print("/sair - sair do chat")

    while True:
        msg = input("> ")
        if msg == "/sair":
            break
        sock.send(msg.encode('utf-8'))

    sock.close()

if __name__ == "__main__":
    main()
