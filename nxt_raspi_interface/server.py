#!/usr/bin/env python
import socket
import interface

PORT = 15555

bot = Interface()
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', PORT))

while True:
    socket.listen(5)
    client, address = socket.accept()
    print "{} connected".format( address )

    response = client.recv(255)
    if response == "0":
        bot.forward()
    elif response == "1":
        bot.back()
    elif response == "2":
        bot.left()
    elif response == "3":
        bot.right()
    elif response == "4":
        bot.take_pic()
    else:
        print "error"

print "Close"
client.close()
stock.close()
