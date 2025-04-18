import threading
from lamport import LamportClock
from log_utils import log_event

class Message:
    def __init__(self, producer, content, timestamp):
        self.producer = producer
        self.content = content
        self.timestamp = timestamp

class Proxy:
    def __init__(self, conn, addr, name):
        self.conn = conn
        self.addr = addr
        self.name = name
        self.channel = None
        self.clock = LamportClock()

    def send(self, message):
        try:
            self.conn.sendall(message.encode())
        except:
            pass

class MsgQMgr:
    def __init__(self):
        self.clients = []
        self.buffer = []
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

    def get_clients_by_channel(self, channel):
        return [c for c in self.clients if c.channel == channel]

    def buffer_message(self, message):
        self.buffer.append(message)
        log_event("mensageria.log", f"[PRODUZIDA] {message.timestamp} | {message.producer} -> {message.content}")

    def broadcast(self, sender, content):
        timestamp = sender.clock.tick()
        msg = Message(sender.name, content, timestamp)
        self.buffer_message(msg)
        for client in self.clients:
            if client != sender:
                client.clock.update(timestamp)
                client.send(f"{msg.timestamp} | {sender.name}: {msg.content}")
                log_event("mensageria.log", f"[CONSUMIDA] {client.clock.time} | {client.name} <- {msg.content}")

    def send_to(self, sender, target_name, content):
        target = self.get_client_by_name(target_name)
        if target:
            timestamp = sender.clock.tick()
            msg = Message(sender.name, content, timestamp)
            self.buffer_message(msg)
            target.clock.update(timestamp)
            target.send(f"{msg.timestamp} | {sender.name} (privado): {msg.content}")
            log_event("mensageria.log", f"[CONSUMIDA] {target.clock.time} | {target.name} <- {msg.content}")

    def send_to_channel(self, sender, content):
        timestamp = sender.clock.tick()
        msg = Message(sender.name, content, timestamp)
        self.buffer_message(msg)
        for client in self.get_clients_by_channel(sender.channel):
            if client != sender:
                client.clock.update(timestamp)
                client.send(f"{msg.timestamp} | {sender.name} (canal {sender.channel}): {msg.content}")
                log_event("mensageria.log", f"[CONSUMIDA] {client.clock.time} | {client.name} <- {msg.content}")
