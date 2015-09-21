'''
A simple "echo" client written in Python.

author:  Amy Csizmar Dalal and [YOUR NAMES HERE]
CS 331, Fall 2015
date:  21 September 2015
'''
import sys, socket

HOSTNAME = socket.gethostname()

def usage():
    print ("Usage:  python SimpleTCPClient <server IP> <port number>")

def connectToServer(server, port, message):
    serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSock.connect((server, port))
    print ("Connected to server; sending message")

    serverSock.send(message.encode("ascii"))
    print ("Sent message; waiting for reply")

    returned = serverSock.recv(1024)
    print ("Received reply: "+ returned.decode("ascii"))

    #serverSock.close() #do with server

    return returned.decode("ascii")

def parseLinks(linksFile):
    f = open(linksFile)

def main():
    # Process command line args (server, port)
    if len(sys.argv) == 3:
        try:
            server = sys.argv[1]
            port = int(sys.argv[2])
            message = "\r\n"

        except ValueError:
            usage()

    else:
        usage()
        
    while True:
        response = connectToServer(server, port, message)
        if message == "\r\n": #or dir
            links = parseLinks(response)
        else:
            #file


main()
