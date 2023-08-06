from qpi.main import QPI
import sys
import os


class ARWatchdog:
    def __init__(self, port, ar_systemd_name='runcore'):
        self.sudo_pass = sys.argv[0]
        self.ar_systemd_name = ar_systemd_name
        self.api = QPI('0.0.0.0', port, without_auth=True,
                       mark_disconnect=False)

    def get_api_support_methods(self):
        methods = {'restart_ar': {'method': self.restart_ar}}
        return methods

    def restart_ar(self, **kwargs):
        """ Перезапустить systemd unit, работающий с AR """
        command = 'systemctl restart {}'.format(self.ar_systemd_name)
        command = "echo {}|sudo -S {}".format(self.sudo_pass, command)
        os.system(command)
