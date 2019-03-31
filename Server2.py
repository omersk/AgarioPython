import socket
import select
import random
import pygame as pg
from settings import *
vec = pg.math.Vector2
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 24))
server_socket.listen(5)
open_client_sockets = []
messages_to_send = []
there_is = []
x = 0
y = 0
arr = []
index_addition = 0


def send_waiting_messages(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        if client_socket in wlist:
            print data
            client_socket.send(data)
            messages_to_send.remove(message)

while True:
    try:
        rlist, wlist, xlist = select.select([server_socket] +
                                            open_client_sockets,
                                            open_client_sockets, [])
        x = random.randint(FROM_X, TO_X)
        y = random.randint(FROM_Y, TO_Y)
        arr.append(vec(x, y))
        for current_socket in rlist:
            if current_socket is server_socket:
                (new_socket, adresss) = server_socket.accept()
                open_client_sockets.append(new_socket)
            else:
                try:
                    data = current_socket.recv(1024)
                    if data == "":
                        open_client_sockets.remove(current_socket)
                        print "connection with client closed"
                    else:
                        messages_to_send.append((current_socket,
                                                 str(arr[int(data) +
                                                         index_addition].x) +
                                                 "," +
                                                 str(arr[int(data) +
                                                         index_addition].y)))
                except:
                    open_client_sockets.remove(current_socket)
                    print "connection with client closed"
        send_waiting_messages(wlist)
    except MemoryError:
        arr = arr[len(arr)/2:len(arr)]
        index_addition += len(arr)/2
