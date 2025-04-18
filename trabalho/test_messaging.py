import unittest
from unittest.mock import MagicMock
from messaging import MsgQMgr, Proxy

class TestMessageQueueManager(unittest.TestCase):

    def setUp(self):
        self.msg_mgr = MsgQMgr()
        
        self.client1 = Proxy(conn=MagicMock(), addr=('127.0.0.1', 5000), name="Alice")
        self.client2 = Proxy(conn=MagicMock(), addr=('127.0.0.2', 5001), name="Bob")
        self.client3 = Proxy(conn=MagicMock(), addr=('127.0.0.3', 5002), name="Charlie")

        self.msg_mgr.add_client(self.client1)
        self.msg_mgr.add_client(self.client2)
        self.msg_mgr.add_client(self.client3)

    def test_add_and_remove_client(self):
        self.assertEqual(len(self.msg_mgr.clients), 3)
        self.msg_mgr.remove_client(self.client2)
        self.assertEqual(len(self.msg_mgr.clients), 2)

    def test_send_to_specific_client(self):
        self.client2.send = MagicMock()
        self.msg_mgr.send_to("Bob", "Mensagem privada")
        self.client2.send.assert_called_once_with("Mensagem privada")

    def test_broadcast(self):
        for client in [self.client1, self.client2, self.client3]:
            client.send = MagicMock()

        self.msg_mgr.broadcast("Mensagem geral", exclude=self.client1)
        self.client1.send.assert_not_called()
        self.client2.send.assert_called_once()
        self.client3.send.assert_called_once()

    def test_group_message(self):
        self.client1.group = "grupoA"
        self.client3.group = "grupoA"
        self.client1.send = MagicMock()
        self.client3.send = MagicMock()

        self.msg_mgr.send_to_group("grupoA", "Olá grupo!")
        self.client1.send.assert_called_once_with("Olá grupo!")
        self.client3.send.assert_called_once_with("Olá grupo!")

if __name__ == '__main__':
    unittest.main()
