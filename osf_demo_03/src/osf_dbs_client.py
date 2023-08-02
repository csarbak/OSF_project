#ask server to read data base given a symbol and table
import sys
import pprint
import socket
import json

SERVER_IP = "127.0.0.1"
PORT = 5001




def app():
    print("*********** RUNNING-APP DBS-SERVER ***********")
    host = SERVER_IP  # as both code is running on same pc
    port=PORT

    # client_socket = socket.socket()  # instantiate
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Error creating socket: %s" % e)
        sys.exit(1)

    try:
        client_socket.connect((host, port))
    except socket.gaierror as e:
        print("Address-related error connecting to server: %s" % e)
        sys.exit(1)
    except socket.error as e:
        print("Connection error: %s" % e)
        sys.exit(1)


    print("\nType 'bye' to end \n")
    dic={}
    message = input(" what Exchange name? (ex : BX,nasdaq, PHLX) ")  # take input
    dic["Exchange_name"] = message
    message = input(" what Symbol? ")  # take input
    dic["Symbol"] = message
    to_server = json.dumps(dic)  # data serialized
    

    while message.lower().strip() != "bye":
        try:
            client_socket.send(to_server.encode())  # send message
        except socket.error as e:
            print("Error sending data: %s" % e)
            sys.exit(1)

        try:
            data = client_socket.recv(1024).decode()  # receive response
        except socket.error as e:
            print("Error receiving data: %s" % e)
            sys.exit(1)

        info = data
        if not data:
            info = "Wrong Data Entered"
        print("The info: \n" + str(info) + "\n")  # show in terminal

        message = input(" what Exchange name? ")  # take input
        if message.lower().strip() == "bye":
            break 
        dic["Exchange_name"] = message
        message = input(" what Symbol? ")  # take input
        if message.lower().strip() == "bye":
            break 
        dic["Symbol"] = message
        to_server = json.dumps(dic)  # data serialized


    client_socket.close()  # close the connection



def run_app():
    print ("*********** ACTIVE-MODULE-LIST ***********")
    pprint.pprint (sys.modules)
    pprint.pprint(sys.argv)
    app()



##################################

if __name__ == "__main__":
    run_app()