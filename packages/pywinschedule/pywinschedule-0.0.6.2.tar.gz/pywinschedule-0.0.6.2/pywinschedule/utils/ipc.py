import socket

class IPC:
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 22222
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channels={}
    def subscribe(self,channel,handler):
        self.channels[channel]=handler
    def dispatch(self,channel,payload):
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.HOST,self.PORT))
        data=channel+":"+payload
        sock.sendall(data.encode())

    def listen(self):
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(10)
        while True:
            coon, addr = self.sock.accept()
            print('Connected:', addr)
            while True:
                data = coon.recv(1024).decode()
                if not data:
                    break
                channel,payload=data.split(':',maxsplit=1)
                if channel in self.channels.keys():
                    self.channels[channel](payload)




