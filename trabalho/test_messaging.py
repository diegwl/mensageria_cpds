import unittest
from unittest.mock import MagicMock, patch
from messaging import MsgQMgr, Proxy, Message
from lamport import LamportClock

class TestMensageriaDistribuida(unittest.TestCase):

    def setUp(self):
        self.msg_mgr = MsgQMgr()
        self.client1 = Proxy(conn=MagicMock(), addr=("127.0.0.1", 5000), name="Alice")
        self.client2 = Proxy(conn=MagicMock(), addr=("127.0.0.2", 5001), name="Bob")
        self.client3 = Proxy(conn=MagicMock(), addr=("127.0.0.3", 5002), name="Charlie")

        self.msg_mgr.add_client(self.client1)
        self.msg_mgr.add_client(self.client2)
        self.msg_mgr.add_client(self.client3)

    def test_lamport_clock_tick(self):
        clock = LamportClock()
        self.assertEqual(clock.tick(), 1)
        self.assertEqual(clock.tick(), 2)

    def test_lamport_clock_update(self):
        clock = LamportClock()
        clock.tick()  # 1
        updated = clock.update(5)
        self.assertEqual(updated, 6)

    @patch("messaging.log_event")
    def test_buffer_message_and_log(self, mock_log):
        msg = Message("Alice", "Oi!", 1)
        self.msg_mgr.buffer_message(msg)
        self.assertEqual(len(self.msg_mgr.buffer), 1)
        mock_log.assert_called_once()

    @patch("messaging.log_event")
    def test_send_to(self, mock_log):
        self.client2.send = MagicMock()
        self.msg_mgr.send_to(self.client1, "Bob", "Mensagem privada")
        self.client2.send.assert_called_once()
        self.assertTrue("Mensagem privada" in self.client2.send.call_args[0][0])
        self.assertEqual(len(self.msg_mgr.buffer), 1)

    @patch("messaging.log_event")
    def test_broadcast(self, mock_log):
        for c in [self.client2, self.client3]:
            c.send = MagicMock()
        self.msg_mgr.broadcast(self.client1, "Mensagem geral")
        self.client2.send.assert_called_once()
        self.client3.send.assert_called_once()

    @patch("messaging.log_event")
    def test_send_to_channel(self, mock_log):
        self.client2.channel = "dev"
        self.client3.channel = "dev"
        self.client2.send = MagicMock()
        self.client3.send = MagicMock()

        self.client1.channel = "dev"
        self.msg_mgr.send_to_channel(self.client1, "Mensagem no canal")
        self.client2.send.assert_called_once()
        self.client3.send.assert_called_once()

if __name__ == "__main__":
    unittest.main()
