import socket
from threading import Thread, Lock
import sys
import time

class NetUpdate:
    def __init__(self, port=8080, interval=5, callback=None):
        self._port_number = port
        self.interval = interval
        self.callback = callback
        self._listen_thread = None
        self._socket = None
        self._host = socket.gethostname()
        self._is_active = False
        self._max_connections = 10

    def start(self):
        self._init_socket()
        print("Connect to {}:{}".format(self._host, self._port_number))
        self._is_active = True
        self._listen_thread = Thread(target=self._listener, daemon=True)
        self._listen_thread.start()

    def end(self):
        if not self._listen_thread:
            return
        self._is_active = False
        while self._listen_thread.isAlive:
            continue
        self._socket.close()
        self._listen_thread = None
    
    def _init_socket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self._host, self._port_number))
    
    def _listener(self):
        self._socket.listen(self._max_connections)
        while self._is_active:
            connection, addr = self._socket.accept()
            print('New client')
            a_thread = Thread(target=self._handle_client, args=(connection, addr), daemon=True)
            a_thread.start()
            
    def _handle_client(self, connection, addr):
        while self._is_active:
            data = connection.recv(2000)
            print('req reveived')
            val = str(self.callback())
            msg = "HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: {}\n\n{}".format(len(val), val)
            connection.send(msg.encode())

#TODO: when I end, it needs to stop listening
    #as of now it is stuck in the recv part
#TODO: same with the handle client part
