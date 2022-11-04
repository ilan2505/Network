import os
import threading
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM


class server:
    def __init__(self):
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        SERVER_ADDRESS = ('127.0.0.1', 55000)
        self.serverSocket.bind(SERVER_ADDRESS)
        self.serverSocket.listen()
        self.Number_Of_Users = 0
        self.checksum = {}
        self.download = {}
        self.clients = {}
        self.UsersName = {}
        self.filesName = os.listdir("./ServerFiles")
        self.action = ""
        self.sendTo = ""

    def resetServer(self):
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        SERVER_ADDRESS = ('127.0.0.1', 55000)
        self.serverSocket.bind(SERVER_ADDRESS)
        self.serverSocket.listen()
        self.Number_Of_Users = 0

    def receive(self):
        while True:
            client, addr = self.serverSocket.accept()
            nick = client.recv(1024).decode('ascii')
            print(f'{nick} join\n')
            self.clients[client] = nick
            self.UsersName[nick] = client
            self.Number_Of_Users = len(self.UsersName)
            self.sendToEveryone(f'{nick} is connected')
            thrd = threading.Thread(target=self.checkIfCon, args=(client,))
            thrd.start()

    def sendToEveryone(self, message):
        for client in self.clients:
            client.send(str(message).encode('ascii'))

    def sendPrivate(self, message, client1):
        thisClient = self.clients[client1]
        print(f'{message}!!{client1}')
        client1.send(str(message).encode('ascii'))

    def checkIfCon(self, client):
        while True:
            try:
                mes = client.recv(1024)
                mes = str(mes)

                if self.action == "":
                    if '<connect>' in mes:
                        pass
                    elif '<get_users>' in mes:
                        self.ounmes(tuple(self.UsersName.keys()), client)
                    elif '<disconnect>' in mes:
                        pass
                    elif '<set_msg>' in mes:
                        self.sendTo = mes[12:-2]
                        self.action = "msg"
                    elif 'set_msg_all' in mes:
                        self.action = "msg_all"
                        self.ounmes("Enter your message: ", client)
                    elif '<get_list_file>' in mes:
                        self.ounmes(self.filesName, client)
                    elif '<checksum>' in mes:
                        check =mes[13:-2]
                        self.checksum[client] = int(mes)

                    elif '<download>' in mes:
                        filename = mes[13:-2]
                        self.download[client] = filename
                        self.sendfiles(filename, client)
                    elif '<proceed>' in mes:
                        if self.download[client]:
                            self.continuesend(self.download[client], client)
                            del self.download[client]
                        else:
                            self.ounmes("you dont have a download", client)

                elif mes != "" and self.action == 'msg_all':
                    self.sendToEveryone(mes)
                    self.action = ""
                    Nick = self.clients[client]
                    mes = mes[1:]
                    mes = f'{Nick}: {mes}'
                    self.sendToEveryone(mes)
                elif mes != "" and self.action == 'msg':
                    try:
                        client2 = self.UsersName[self.sendTo]
                        Nick = self.clients[client]
                        mes = mes[1:]
                        mes = f'{Nick}: {mes}'
                        self.sendPrivate(mes, client2)
                    except:
                        self.ounmes("there are no NickName", client)

                    self.action = ""

            except:
                name = self.clients[client]
                del self.clients[client]
                del self.UsersName[name]
                msg = f'{name} is disconnected'
                print(msg)
                self.sendToEveryone(msg)
                client.close()
                break

    def ounmes(self, msg, client):
        client.send(str(msg).encode('ascii'))

    def sendfiles(self, file_name, client):
        count=0
        send = 0
        s = socket(AF_INET, SOCK_DGRAM)
        port = 9999
        buf = 128
        addr = ('localhost', port)
        file = f'./ServerFiles/{file_name}'
        size = (int)(os.path.getsize(file) / buf)
        halfSize = size / 2
        size = (str)(size).encode()
        s.sendto(size, addr)
        timeout=False
        try:
            f = open(file, "rb")
            data = f.read(buf)
            # s.sendto(file, addr)
            self.ounmes("start download:", client)
            while data and send < halfSize:

                if s.sendto(data, addr):
                    print("sending..")
                    data = f.read(buf)
                    send = send + 1
            self.ounmes("download stop", client)

            f.close()
        except:
            self.ounmes("file dont exists", client)
        s.close()

    def continuesend(self, file_name, client):
        send = 0
        s = socket(AF_INET, SOCK_DGRAM)
        port = 9999
        buf = 1024
        addr = ('localhost', port)
        file = f'./ServerFiles/{file_name}'
        size = (int)(os.path.getsize(file) / 1024)
        halfSize = size / 2
        size = (str)(size).encode()
        s.sendto(size, addr)
        try:
            f = open(file, "rb")
            data = f.read(buf)
            # s.sendto(file, addr)
            self.ounmes("continue:", client)
            while data:
                if send < halfSize:
                    data = f.read(buf)
                    send = send + 1
                else:

                    if s.sendto(data, addr):
                        print("sending..")
                        data = f.read(buf)
                        send = send + 1
            self.ounmes("download stop", client)

            f.close()
        except:
            self.ounmes("file dont exists", client)
        s.close()


if __name__ == '__main__':
    my_server = server()
    my_server.resetServer()
    print("server open")
    my_server.receive()
