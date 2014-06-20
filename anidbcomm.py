from lib.py3utils import Config
import socket
from threading import Thread

class AnidbComm(Thread):

    def __init__(self):
        config = Config()
        self._hostname = config.get('anidb', 'anidbhost')
        self._port = int(config.get('anidb', 'anidbport'))
        self._localport = int(config.get('anidb', 'anidblocalport'))
        self._timeout = int(config.get('anidb', 'anidbtimeout'))
        self._delay = int(config.get('anidb', 'anidbdelay'))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self._localport))
        self.sock.settimeout(self._timeout)

    def run(self):
#        while True:
            data, addr = self.sock.recvfrom(8192)
            print("Received: ", data, addr)

    def send(self):
        self.sock.sendto(b"PING nat=1", (self._hostname, self._port))
