#like txt symbol for udp

import sys
import pprint
import socket
import json




SERVER_IP = "127.0.0.1"
EXCHANGE="CME" #either "NASDAQ", "CME", "NYSE", "BX"
OUTPUT = "json" #either txt or json
FOREIGN_PORT = 5000
def app():
    print("***********RUNNING-APP UDP CLIENT-TXT ***********")
    # client_socket = socket.socket()  # instantiate
    outPut= OUTPUT
    exchange = EXCHANGE
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print("Error creating socket: %s" % e)
        sys.exit(1)

    # foregn_port = int(input("foregn_port? "))
    # local_port = int(input("local port? "))
    server_addr = (SERVER_IP, FOREIGN_PORT)
    # client_socket.bind(("", local_port))

    client_socket.sendto(exchange.encode("utf-8"), server_addr)
    data = None
    while not data:
        data = client_socket.recvfrom(1024)

    client_socket.sendto(outPut.encode("utf-8"), server_addr)
    data = None
    while not data:
        data = client_socket.recv(1024).decode()

    print("\nType 'bye' to end \n")

    message = input(" what Symbol? ")  # take input

    while message.lower().strip() != "bye":
        try:
            client_socket.sendto(message.encode("utf-8"), server_addr)  # send message
        except socket.error as e:
            print("Error sending data: %s" % e)
            sys.exit(1)

        try:
            bytesAddressPair = client_socket.recvfrom(1024)  # receive response
        except socket.error as e:
            print("Error receiving data: %s" % e)
            sys.exit(1)

        data = bytesAddressPair[0].decode("utf-8")
        if outPut != "txt":
            data = json.loads(data)  # data loaded

            info = ""
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

    try:
        client_socket.sendto(message.encode("utf-8"), server_addr)  # send message
    except socket.error as e:
        print("Error sending data: %s" % e)
        sys.exit(1)



def run_app():
    print ("*********** ACTIVE-MODULE-LIST ***********")
    pprint.pprint (sys.modules)
    pprint.pprint(sys.argv)
    app()



##################################

if __name__ == "__main__":
    run_app()