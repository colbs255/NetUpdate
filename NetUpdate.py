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
        while self._listen_thread.isAlive():
            continue
        self._socket.close()
        self._listen_thread = None
        self._socket = None
    
    def _init_socket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self._host, self._port_number))
        self._socket.setblocking(0)
    
    def _listener(self):
        self._socket.listen(self._max_connections)
        while True:
            connection = None
            addr = None
            while self._is_active and not connection:
                try:
                    c, a = self._socket.accept()
                    connection = c
                    addr = a   
                except BlockingIOError:
                    pass        
            if not self._is_active:
                return
            print('New client')
            a_thread = Thread(target=self._handle_client, args=(connection, addr), daemon=True)
            a_thread.start()
            
    def _handle_client(self, connection, addr):
        while True:
            data = None
            while self._is_active and not data:
                try:
                    data = connection.recv(2000)
                except BlockingIOError:
                    pass
            if not self._is_active:
                return
            print('req reveived')
            val = str(self.callback())
            msg = "HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: {}\n\n{}".format(len(val), val)
            connection.send(msg.encode())

#TODO: need a timeout functionality so i dont have a ton of threads
#TODO: need to make sure the portnumber is not being used again before i restart
