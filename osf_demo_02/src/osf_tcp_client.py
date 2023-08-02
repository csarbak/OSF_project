#client for txt symbol
import sys
import pprint
import socket
import json

PORT =  5000
SERVER_IP = "127.0.0.1"
EXCHANGE="CME" #either "NASDAQ", "CME", "NYSE", "BX"
OUTPUT = "json" #either txt or json



def app():
    print("*********** RUNNING-APP TCP-CLIENT TXT ***********")
    host = SERVER_IP  # as both code is running on same pc
    port=PORT
    exchange = EXCHANGE
    outPut=OUTPUT

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

    client_socket.send(exchange.encode())  # send message
    data = None
    while not data:
        data = client_socket.recv(1024).decode()

    client_socket.send(outPut.encode())  # send message
    data = None
    while not data:
        data = client_socket.recv(1024).decode()

    print("\nType 'bye' to end \n")

    message = input(" what Symbol? ")  # take input

    while message.lower().strip() != "bye":
        try:
            client_socket.send(message.encode())  # send message
        except socket.error as e:
            print("Error sending data: %s" % e)
            sys.exit(1)

        try:
            data = client_socket.recv(1024).decode()  # receive response
            if outPut == "json":
                data = json.loads(data)  # data loaded
        except socket.error as e:
            print("Error receiving data: %s" % e)
            sys.exit(1)

        info = ""
        if outPut == "json":
            print("The info: \n" + str(data) + "\n")
            i = 0
            for k, v in data.items():
                if str(v).isspace() or v == "":
                    v = "EMPTY"
                adding = f"{k} =  {v}\n"
                info = info + adding
                i += 1
        else:
            info = data
        if not data:
            info = "Wrong Data Entered"
        print("The info: \n" + str(info) + "\n")  # show in terminal

        message = input(" Symbol again: ?\n ")  # again take input

    client_socket.close()  # close the connection
    



def run_app():
    print ("*********** ACTIVE-MODULE-LIST ***********")
    pprint.pprint (sys.modules)
    pprint.pprint(sys.argv)
    app()



##################################

if __name__ == "__main__":
    run_app()