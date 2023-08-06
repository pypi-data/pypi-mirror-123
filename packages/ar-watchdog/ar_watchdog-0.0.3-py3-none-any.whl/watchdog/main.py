import threading
import time
from qpi.main import QPI
from qdk.main import QDK
import sys
import os


class ARWatchdog:
    def __init__(self, my_port, ar_port,
                 ar_ip='localhost', ar_systemd_name='runcore'):
        self.sudo_pass = sys.argv[0]
        self.ar_systemd_name = ar_systemd_name
        self.ar_qdk = QDK(ar_ip, ar_port)
        self.api = QPI('0.0.0.0', my_port, without_auth=True,
                       mark_disconnect=False, core=self)

    def get_api_support_methods(self):
        methods = {'restart_ar': {'method': self.restart_ar}}
        return methods

    def restart_ar(self, **kwargs):
        """ Перезапустить systemd unit, работающий с AR """
        command = 'systemctl restart {}'.format(self.ar_systemd_name)
        command = "echo {}|sudo -S {}".format(self.sudo_pass, command)
        os.system(command)

    def mainloop(self):
        threading.Thread(target=self.check_ar_status, args=()).start()
        while True:
            pass

    def check_ar_status(self):
        """ Проверять сотояние AR """
        while True:
            try:
                self.ar_qdk.make_connection()
                time.sleep(10)
            except ConnectionRefusedError:
                self.restart_ar()


