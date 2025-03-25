class Message:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content

class User:
    def __init__(self, name, connection):
        self.name = name
        self.connection = connection

    def send_message(self, recipient, content):
        message = Message(self.name, content)
        recipient.receive_message(message)

    def receive_message(self, message):
        try:
            self.connection.send(f"{message.sender}: {message.content}".encode('utf-8'))
        except:
            pass

class Group:
    def __init__(self, name):
        self.name = name
        self.users = []

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)

    def broadcast_message(self, sender, content):
        message = Message(sender, content)
        for user in self.users:
            if user.name != sender:
                user.receive_message(message)
