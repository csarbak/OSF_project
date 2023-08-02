import sys
import pprint
import socket
import json



TEXT_FILE = "../data/bxtraded.txt"
SERVER_IP = "127.0.0.1"
RECV_PORT = 5000

def app():
    print("*********** RUNNING-APP UDP SERVER-TXT ***********")
     # get the hostname
    host = SERVER_IP
    ccfile = open(TEXT_FILE, "r")

    print("host name: " + str(host))
    # recv_port = int(input("recv_port: "))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # get instance
    server_socket.bind(("", RECV_PORT))

    fileData=[]
    for aline in ccfile:
            values = aline.split("|")
            fileData.append(values)

    dic = {}
    for values in fileData:
        for v in values:
            dic[v] = ""
        break

    while True:
        info = ""
        # receive data stream. it won't accept data packet greater than 1024 bytes
        bytesAddressPair = server_socket.recvfrom(1024)
        symbol = bytesAddressPair[0].decode("utf-8")

        if not symbol or symbol == "bye":
            break

        if symbol == "CME" or symbol == "NASDAQ" or symbol == "NYSE":
            ex_name = str(symbol)
            server_socket.sendto(ex_name.encode("utf-8"), bytesAddressPair[1])

            continue

        if symbol == "txt" or symbol == "json":
            outputType = str(symbol)
            server_socket.sendto(outputType.encode("utf-8"), bytesAddressPair[1])
            continue

        notFound = True
        for values in fileData:
            if values[1] == str(symbol):
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

        server_socket.sendto(
            info.encode("utf-8"), bytesAddressPair[1]
        )  # send data to the client


def run_app():
    print ("*********** ACTIVE-MODULE-LIST ***********")
    pprint.pprint (sys.modules)
    pprint.pprint(sys.argv)
    app()



##################################

if __name__ == "__main__":
    run_app()