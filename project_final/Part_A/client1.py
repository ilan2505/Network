import threading
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM


class client:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.NikeName = ""
        self.iscon = False
        self.IP = ""

    def connect(self, nick, ip, port=55000):
        try:
            self.IP = ip
            print(nick)
            self.sock.connect((ip, port))
            self.NikeName = nick
            self.sock.send(self.NikeName.encode('ascii'))
            self.iscon = True
        except:
            print("Error")
            self.iscon = False

    def receive(self):
        while True:
            try:
                mess = self.sock.recv(1024).decode("ascii")
                if mess != '':
                    print(mess)
            except:
                self.sock.close()
                break

    def write(self):
        while True:
            msg = input("")
            if '<connect>' in msg and self.iscon == False:
                Nick = msg[10:-1]
                self.connect(Nick, '127.0.0.1')
            elif '<disconnect>' in msg and self.iscon == True:
                self.sock.send(msg.encode('ascii'))
                self.sock.close()
                self.iscon = False
                break
            elif '<download>' in msg:
                self.download(self.IP, msg[12:-2])
            else:
                self.sock.send(msg.encode('ascii'))

    def download(self, IP, fileName):
        UDP_sock = socket(AF_INET, SOCK_DGRAM)
        IPort = IP, 55001
        UDP_sock.bind(IPort)
        data, address = UDP_sock.recvfrom(1024)
        file = open(f'{fileName}', 'w')
        data.strip()


if __name__ == '__main__':
    client = client()
    write_thrd = threading.Thread(target=client.write)
    write_thrd.start()
    while not client.iscon:
        pass
    print(123)
    recive_thrd = threading.Thread(target=client.receive)
    recive_thrd.start()
