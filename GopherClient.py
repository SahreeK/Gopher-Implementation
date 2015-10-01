'''
Gopher client revision

Started with code written by Amy Csizmar Dalal.

Implements the client side of the Gopher Protocol (RFC 1436).
Directories are indicated with a trailing ellipses. Files are indicated as their display string. This adheres to the RFC guidelines.



authors:  Cody Bohlman, Joe Burson, Sahree Kasper
CS 331, Fall 2015
date:  2 October 2015
'''
import re, sys, socket

HOSTNAME = socket.gethostname()

def usage():
    print ("Usage:  python3 GopherClient.py <server IP> <port number>")
    sys.exit(0)

def connectToServer(server, port, message):
    try:
        #print(message, server, port)
        serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSock.connect((server, port))
        serverSock.send(message.encode("ascii"))
    
    except:
        print("No connection to server available.")
        sys.exit(0)

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
def nextRequest(links, server, port):
    request = input("\nSelect an option from the list above -> ")
    print()
    badLine = ""
    # nothing
    if request == "": 
        return "not valid", "none", server, port
    try:
        for key in links:
            badLine = links[key]
            if request.lower() in key.lower():
                server = links[key][1]
                port = links[key][2]
                message = links[key][0]
                if key[0] == "0":
                    messageType = "file"
                elif key[0] == "1":
                    messageType = "links"
                else:
                    messageType = "not valid"
                return message, messageType, server, port
    except TypeError:
        print("There was an error in your input.")
        
    except IndexError:
        print("Invalid .links file from server. Line is:",badLine)
    return "", "links", server, port 

def showUsability():
    print("Welcome to our Gopher Client!\n\nBelow you will see the contents of the root level directory.\nFolder names are followed by"\
          +" an ellipsis (...), and files have no special marking. This adheres to the guidelines in RFC 1436.\n\nWhen selecting a file or directory, you may type either part of or the entire display string. Use the entire display string if two files/directories have similar names.\n")

def main():
    # Process command line args (server, port)
    if len(sys.argv) >= 3:
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
        
    showUsability()
    while True:
        response = connectToServer(server, port, message)
        if messageType == "links":

            # response will be a string
            links = parseLinks(response)
            
        elif messageType == "file":
            print(response)
            input("Press enter to continue...")
            print()
            message = ""
        else:
            pass

        display(links)
        
        message, messageType, server, port = nextRequest(links, server, port)
        port = int(port)
        message += "\r\n"
        

main()
