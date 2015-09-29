'''
Gopher server

Started with code written by Amy Csizmar Dalal.

This program implements the server side of the Gopher Protocol (RFC 1436). 
If the server receives an ill-formatted or incorrect selector string, it will return the top level links file to the client.
If white space is entered, the current links file will be displayed.
The server runs on port 50000. 
Using the socket library, we use socket.shutdown() to close the connection, but allow new connections with the same settings. 

authors:  Cody Bohlman, Joe Burson, Sahree Kasper
CS 331, Fall 2015
date:  28 September 2015
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
            print("Message received from ",clientAddr)
            # accepts connection, should not say anything
            # Get the message and echo it back
            while True:
                data = clientSock.recv(1024)
                if not len(data):
                    break
                message = self.parseMessage(data.decode("ascii"))
                # message to be sent out
                data = message.encode("ascii")
                clientSock.sendall(data)
                clientSock.shutdown(socket.SHUT_RDWR)
                
        clientSock.close()
            
    # parses the message from the client
    def parseMessage(self, clientMessage):
        message = ""
        item = clientMessage.strip()
        if clientMessage.strip() == "not valid":
            pass
        elif clientMessage == "\r\n":
            message = self.parseLinks(self.openResource(".links"))
        elif clientMessage.strip()[-1] == "/":
            message = self.parseLinks(self.openResource(item + ".links"))
        else:
            message = self.openResource(item)
                
        message += "."
        return message

    # opens and closes a give file
    def openResource(self, location):
        try:
            resource = open(location)
            content = self.parseFile(resource)
            resource.close()
            return content
        except:
            return "i    This resource cannot be located error.host  1 \r\n."
    
    # open the file and print the contents as a string
    def parseFile(self, f):
        outputString = ""
        for line in f:
            outputString += line
        return outputString
    
    # creates dictionary with a key of display string and value everything else
    def parseLinks(self, linksFile):
        d = {}
        for line in linksFile.split("\n"):
            words = line.split("\t")
            
            # This represents the display string to less than 70 characters
            key = self.lengthLimiter(words[0], 70)
            value = words[1:]
            
            # This represents the selector string, limited to less than 255 characters
            value[0] = self.lengthLimiter(value[0], 255)
            d[key] = value
        
        s = ""
        for key in d:
            s += key + "\t"
            for item in d[key]:
                s += item + "\t"
            s += "\r\n"

        return s
    
    def lengthLimiter(self, s, limit):
        if len(s) > limit:
            return s[:limit-1]
        return s

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

    server.listen()

main()