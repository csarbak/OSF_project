#server for txt symbol
import sys
import pprint
import socket
import json


TEXT_FILE = "../data/bxtraded.txt"  #Change to your exchange preference
SERVER_IP = "127.0.0.1"
PORT = 5000


def app():
    print("*********** RUNNING-APP TCP SERVER-TXT ***********")
    # get the hostname
    host = SERVER_IP
    port = PORT
    ccfile = open(TEXT_FILE, "r")


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(4)
    conn, address = server_socket.accept()  # accept new connection

    fileData=[]
    for aline in ccfile:
            values = aline.split("|")
            fileData.append(values)


    print("Connection from: " + str(address))
    outputType = "json"
    dic = {}
    for values in fileData:
        for v in values:
            dic[v] = ""
        break

    while True:
        
        # receive data stream. it won't accept data packet greater than 1024 bytes

        data_recv = conn.recv(1024).decode()
        print(f"data_recv: {data_recv}")

        if not data_recv or data_recv == "bye":
            break
        data_recv = str(data_recv)

        if data_recv == "CME" or data_recv == "NASDAQ" or data_recv == "NYSE":
            ex_name = str(data_recv)
            conn.send(ex_name.encode())  # send data to the client

            continue

        if data_recv == "txt" or data_recv == "json":
            outputType = str(data_recv)
            conn.send(outputType.encode())  # send data to the client
            continue

        notFound = True
        for values in fileData:
            if values[1] == str(data_recv):
                notFound = False
                i = 0
                for k, v in dic.items():
                    dic[k] = values[i]
                    i += 1
                break

        if outputType == "json":
            if notFound == False:
                info = json.dumps(dic)  # data serialized
            else:
                info = json.dumps({})
        else:
            if notFound == False:
                info = str(dic)  # data serialized
            else:
                info = "Empty please try again"

        conn.send(info.encode())  # send data to the client

    conn.close()  # close the connection



def run_app():
    print ("*********** ACTIVE-MODULE-LIST ***********")
    pprint.pprint (sys.modules)
    pprint.pprint(sys.argv)
    app()



##################################

if __name__ == "__main__":
    run_app()