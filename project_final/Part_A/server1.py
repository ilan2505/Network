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
        self.clients = {}
        self.UsersName = {}
        
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
                    	 self.sendToEveryone(f'{nick} is disconnected')
                    elif '<set_msg>' in mes:
                        self.sendTo = mes[12:-2]
                        print(self.sendTo)
                        self.action = "msg"
                    elif '<set_msg_all>' in mes:
                        self.action = "msg_all"
                        self.ounmes("Enter your message: ", client)
                    elif '<get_list_file>' in mes:
                        self.ounmes(self.filesName, client)
                    elif '<download> < test.txt >' in mes:
                        filename = mes[22:-2]
                        self.sendfiles(filename, client)
                    elif '<proceed>' in mes:
                        pass
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
                print(self.clients)
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
        count = 0
        s = socket(AF_INET, SOCK_DGRAM)
        port = 55000
        buf = 1024
        addr = (client, port)
        f = open(file_name, "rb")
        data = f.read(buf)

        s.sendto(file_name, addr)
        s.sendto(data, addr)
        while data:
            if (s.sendto(data, addr)):
                print("sending ...")
                data = f.read(buf)
        s.close()
        f.close()


if __name__ == '__main__':
    my_server = server()
    my_server.resetServer()
    print("server open")
    my_server.receive()
