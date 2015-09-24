'''
A simple "echo" client written in Python.

author:  Amy Csizmar Dalal and [YOUR NAMES HERE]
CS 331, Fall 2015
date:  21 September 2015
'''
import re, sys, socket

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
    # creates dictionary with a key of display string and value everything else
    d = {}
    for line in linksFile.split("\n"):
        words = line.split("\t")
        d[words[0]] = words[1:]
    return d

def main():
    # Process command line args (server, port)
    if len(sys.argv) == 3:
        try:
            server = sys.argv[1]
            port = int(sys.argv[2])
            message = "\r\n"
            messageType = "links"
            links = {}

        except ValueError:
            usage()

    else:
        usage()
        
    while True:
        response = connectToServer(server, port, message)
        if messageType == "links":
            #print(response)
            # response will be a string
            links = parseLinks(response)
            
        else:
            print(response)
            input("Press any key to continue...")
            print()
            print()
            print()
        print(links)
        for entry in links:
            if entry == "":
                # may not want this forever
                pass
            elif entry[0] == "0":
                print(entry[1:])
            else:
                print(entry[1:]+"...")
                
        nextRequest = input("Select an option from the list above -> ")
        for key in links:
            if nextRequest in key:
                server = links[key][1]
                port = links[key][2]
                message = links[key][0]
                if key[0] == "0":
                    messageType = "file"
                else:
                    messageType = "links"
                    
    


main()
