from os import close
import socket
import threading
import time
import os
import sys

SERVERADDRESS = ("0.0.0.0", 9000)


# SERVERADDRESS = ("localhost", 4444)


def file_transfer(ip_port, serversocket):
    print("connected ", ip_port)
    filename = '/mnt/mirror/1.mp4'
    # filename = '1.mov'
    filedata = filename.encode("utf-8")
    if os.path.exists(filedata):
        filesize = os.path.getsize(filedata)
        filemg = filesize / float(1024 * 1024)
        data = "name:{},size:{:.2f}".format(filedata, filemg)
        serversocket.send(data.encode("utf-8"))

        options = serversocket.recv(1024)
        if options.decode("utf-8") == "y":
            with open(filedata, "rb") as f:
                packetnum = filesize / 1024
                counter = 0

                while True:
                    # try:
                    opt = serversocket.recv(1024)
                    if opt.decode("utf-8") == "p":
                        print("client paused")
                    elif opt.decode("utf-8") == "r":
                        for i in range(0, 100):
                            file_data = f.read(1024)
                            counter = counter + 1
                            process = counter / packetnum * 100
                            if file_data:
                                serversocket.send(file_data)
                            else:
                                print("file transferred successfully")
                                break
                        print("resumed from: {:.2f}{}".format(process, "%"))
                    elif opt.decode("utf-8") == "w":
                        run = True
                        while run:
                            file_data = f.read(1024)
                            counter = counter + 1
                            process = counter / packetnum * 100
                            if file_data:
                                serversocket.send(file_data)
                            else:
                                print("download completed : {:.2f}{}".format(process, "%"))
                                print("file transferred successfully ")
                                run = False
                        if not run:
                            break

                # except:
                #     serversocket.close()


        else:
            print("abort")
    else:
        print("file does not exist")

    serversocket.close()

def receive_message(connection, client_address):
    while True:
        message = connection.recv(1024)
        print("from: ", client_address, "message: ", message)
        connection.send(message)

        if message == b'terminate':
            connection.close()
            break


def main():
    s = socket.socket()

    s.bind(SERVERADDRESS)

    s.listen(5)

    while True:
        print("Waiting for a connection ...")

        connection, client_addr = s.accept()

        print("connection received from: ", client_addr)

        th = thread = threading.Thread(target=file_transfer, args=[client_addr, connection])
        th.start()


if __name__ == "__main__":
    main()
