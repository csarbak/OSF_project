import socket
import json
from os import environ, path
from dotenv import load_dotenv

# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, ".env"))
load_dotenv("/Users/conradscomputer/Desktop/Fintech/osfutils_dev/osf_demo_01/.env")

TEXT_FILE = environ.get("TEXT_FILE")
SERVER_IP = environ.get("SERVER_IP")
PORT = int(environ.get("PORT"))


def load_server_program( port, ccfile):
    # get the hostname
    host = SERVER_IP

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
    outputType = "txt"
    dic = load_dic(ccfile)
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


def load_dic(fileObject):
    for aline in fileObject:
        values = aline.split("|")
        keys = values
        dic = dict(zip(keys, [None] * len(keys)))
        break

    return dic


if __name__ == "__main__":
    ccfile = open(TEXT_FILE, "r")
    # port = int(input("enter port: "))
    load_server_program( PORT, ccfile)
    ccfile.close
