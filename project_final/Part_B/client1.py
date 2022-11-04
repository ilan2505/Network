import threading
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, timeout


class client:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.NikeName = ""
        self.iscon = False
        self.IP = ""
        self.file = ""
        self.start = False
        self.checksum = 0

    def connect(self, nick, ip, port=55000):
        try:
            self.IP = ip
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
                if "start download:" in mess:
                    downthrd = threading.Thread(target=self.download(self.IP, self.file))
                    downthrd.start()
                elif "continue" in mess:
                    downthrd = threading.Thread(target=self.continuedown(self.IP, self.file))
                    downthrd.start()
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
                msg = str(msg)
                self.file = msg[11:-1]
                self.sock.send(msg.encode('ascii'))

            else:
                self.sock.send(msg.encode('ascii'))

    def download(self, IP, fileName):
        counter = 0
        print('start download')
        UDP_sock = socket(AF_INET, SOCK_DGRAM)
        host = '127.0.0.1'
        IPort = (host, 9999)
        UDP_sock.bind(IPort)
        data, address = UDP_sock.recvfrom(1024)
        size = data
        file = open(f'{fileName}', 'wb')
        try:
            while data:
                counter = counter + 1
                #UDP_sock.sendto(counter, IPort)
                file.write(data)
                UDP_sock.settimeout(2)
                data, address = UDP_sock.recvfrom(1024)
                # if data1 != data:
                # UDP_sock.send(counter)
                #  data1 = data
            print('download stop')


        except timeout:
            file.close()

        UDP_sock.close()

    def continuedown(self, IP, fileName):
        counter = 0
        print('start download')
        UDP_sock = socket(AF_INET, SOCK_DGRAM)
        host = '127.0.0.1'
        IPort = (host, 9999)
        UDP_sock.bind(IPort)
        data, address = UDP_sock.recvfrom(1024)
        size = data
        file = open(f'{fileName}', 'ab')
        try:
            while data:
                counter = counter + 1
                file.write(data)
                UDP_sock.settimeout(2)
                data, address = UDP_sock.recvfrom(1024)
                # if data1 != data:
                # UDP_sock.send(counter)
                #  data1 = data
            print('download stop')
        except timeout:
            file.close()

        UDP_sock.close()


if __name__ == '__main__':
    client = client()
    write_thrd = threading.Thread(target=client.write)
    write_thrd.start()
    while not client.iscon:
        pass
    recive_thrd = threading.Thread(target=client.receive)
    recive_thrd.start()
