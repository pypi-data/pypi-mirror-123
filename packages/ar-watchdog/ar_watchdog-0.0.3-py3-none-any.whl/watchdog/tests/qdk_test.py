from qdk.main import QDK
import unittest


class QDKTets(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.qdk = QDK('192.168.100.118', 9889)
        self.qdk.make_connection()

    def test_restart_ar(self):
        self.qdk.execute_method('restart_ar')
        print(self.qdk.get_data())

