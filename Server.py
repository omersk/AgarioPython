import socket
import select
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 23))
server_socket.listen(5)
open_client_sockets = []
messages_to_send = []
there_is = []
count = 0


def send_waiting_messages(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        try:
            float(data.split(",")[0])
            float(data.split(",")[1])
            if client_socket in wlist:
                for socket in wlist:
                    if socket != client_socket:
                        socket.send(data.split(",")[0] + "," +
                                    data.split(",")[1])
                messages_to_send.remove(message)
        except:
            messages_to_send.remove(message)

while True:
    rlist, wlist, xlist = select.select([server_socket] + open_client_sockets,
                                        open_client_sockets, [])
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
                    count += 1
                    messages_to_send.append((current_socket, data))
            except:
                    open_client_sockets.remove(current_socket)
                    print "connection with client closed"

    send_waiting_messages(wlist)
