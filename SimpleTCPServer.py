'''
A simple TCP "echo" server written in Python.

author:  Amy Csizmar Dalal and [YOUR NAMES HERE]
CS 331, Fall 2015
date:  21 September 2015
'''
import sys, socket

class TCPServer:
    def __init__(self, port=50000):
        self.port = port
        self.host = ""
        self.startServer()

    def startServer(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #In case server crashes
        self.sock.bind((self.host, self.port))        

    def listen(self):
        self.sock.listen(5)

        while True:
            clientSock, clientAddr = self.sock.accept()
            # accepts connection, should not say anything
            print ("Connection received from ",  clientSock.getpeername())
            # Get the message and echo it back
            message = ""
            while True:
                data = clientSock.recv(1024)
                if not len(data):
                    break
                print ("Received message:  " + data.decode("ascii"))
                clientMessage = data.decode("ascii")
                if clientMessage == "\r\n":
                    print("cats")
                    linksFile = open(".links")
                    message = self.parseFile(linksFile)
                    linksFile.close()
                elif clientMessage.strip()[-1] == "/":
                    print("cats1")
                    try:
                        print("trying to open: " + clientMessage +".links")
                        linksFile = open(clientMessage.strip() +".links")
                        message = self.parseFile(linksFile)
                        linksFile.close()
                    except:
                        message = "i    This resource cannot be located error.host  1 \r\n."
                    
                else:
                    print("cats2")
                    try:
                        print("trying to open: " + clientMessage)
                        linksFile = open(clientMessage.strip())
                        message = self.parseFile(linksFile)
                        linksFile.close()
                    except:
                        message = "i    This resource cannot be located error.host  1 \r\n."
                # message to be sent out\
                print(message)
                if message == "":
                    message = "\r\n."
                data = message.encode("ascii")
                clientSock.sendall(data)
                clientSock.shutdown(socket.SHUT_RDWR)
            
    def parseLinks(self, linksFile):
        pass
    
    # open the file and print the contents as a string
    def parseFile(self, f):
        outputString = ""
        for line in f:
            outputString += line
        outputString += "\r\n."
        return outputString
    
    def findFile(self, selectorString):
        pass
    

def main():
    # Create a server
    if len(sys.argv) > 1:
        try:
            server = TCPServer(int(sys.argv[1]))
        except ValueError:
            print ("Please specify port as an integer.  Creating server on default port.")
            server = TCPServer()
    else:
        server = TCPServer()

    # Listen forever
    print ("Listening on port " + str(server.port))
    server.listen()

main()
