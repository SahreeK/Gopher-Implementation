'''
Gopher client

Started with code written by Amy Csizmar Dalal.
authors:  Cody Bohlman, Joe Burson, Sahree Kasper
CS 331, Fall 2015
date:  28 September 2015
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

    receivedMessage = ""
    while True:
        data = serverSock.recv(1024)
        if not len(data):
            break
        receivedMessage += data.decode("ascii")
        
    return receivedMessage

# creates dictionary with a key of display string and value everything else
def parseLinks(linksFile):
    d = {}
    for line in linksFile.split("\n"):
        words = line.split("\t")
        d[words[0]] = words[1:]
    return d

# displays the dictionary of links and distinguishes directories and files
def display(links):
    #print(links)
    for entry in links:
        if entry == "":
            # may not want this forever
            pass
        # print directory
        elif entry[0] == "0":
            print(entry[1:])
        # print file
        elif entry[0] == "1":
            print(entry[1:]+"...")
        else:
            pass

# construct the user-defined requests
def nextRequest(links):
    request = input("Select an option from the list above -> ")
    for key in links:
        if request in key:
            server = links[key][1]
            port = links[key][2]
            message = links[key][0]
            if key[0] == "0":
                messageType = "file"
            else:
                messageType = "links"
            return message, messageType, server, port

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
            input("Press enter to continue...")

        display(links)
        message, messageType, server, port = nextRequest(links)
        port = int(port)
        message += "\r\n"
        

main()
