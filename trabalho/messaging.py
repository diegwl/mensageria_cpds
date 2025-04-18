import threading

class Proxy:
    def __init__(self, conn, addr, name):
        self.conn = conn
        self.addr = addr
        self.name = name
        self.group = None

    def send(self, message):
        try:
            self.conn.sendall(message.encode())
        except:
            pass

class MsgQMgr:
    def __init__(self):
        self.clients = []
        self.lock = threading.Lock()

    def add_client(self, proxy):
        with self.lock:
            self.clients.append(proxy)

    def remove_client(self, proxy):
        with self.lock:
            self.clients.remove(proxy)

    def get_client_by_name(self, name):
        for client in self.clients:
            if client.name == name:
                return client
        return None

    def broadcast(self, message, exclude=None):
        with self.lock:
            for client in self.clients:
                if client != exclude:
                    client.send(message)

    def send_to(self, name, message):
        client = self.get_client_by_name(name)
        if client:
            client.send(message)

    def send_to_group(self, group_name, message):
        with self.lock:
            for client in self.clients:
                if client.group == group_name:
                    client.send(message)
