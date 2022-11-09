import socket
import time
import random
import os
import sys

SERVERADDRESS = ("192.168.10.2", 9000)
# SERVERADDRESS = ("localhost", 4444)


def main():
    s = socket.socket()
    print("connect to server: ", SERVERADDRESS)

    s.connect(SERVERADDRESS)

    received_file = s.recv(1024)
    file_data = received_file.decode("utf-8")
    print(file_data)
    file_name = "3.mp4"
    filesize = float(file_data.split(',')[1].split('size:')[1])
    filesize2 = filesize * 1024
    opts = input("Do you want to download the file? press y(yes) or q(quit)")
    if opts == 'q':
        print("abort")
    else:
        print("download started")
        s.send(b'y')

    with open("./" + file_name, "wb") as file:
        counter = 0
        precentage = 0
        while True:
            opt = input("press r to resume or p to pause or w to download all: ")
            if opt == 'p':
                print("paused from: {:.2f}{}".format(precentage, "%"))
                s.send(b'p')
            elif opt == 'r':
                s.send(b'r')
                for i in range(0, 100):
                    file_data = s.recv(1024)
                    if file_data:
                        file.write(file_data)
                        counter = counter + 1
                        precentage = counter / filesize2 * 100
                print("resumed from: {:.2f}{}".format(precentage, "%"))
            elif opt == 'w':
                s.send(b'w')
                run = True
                while run:
                    file_data = s.recv(1024)
                    counter = counter + 1
                    precentage = counter / filesize2 * 100
                    if file_data:
                        file.write(file_data)
                    else:
                        print("download completed : {:.2f}{}".format(precentage, "%"))
                        s.close()
                        run = False
                if not run:
                    break
    s.close()


if __name__ == "__main__":
    main()
