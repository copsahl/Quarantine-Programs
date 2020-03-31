import socket
import random
from datetime import datetime

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('',1337))

with open("phrases.txt","r") as fobj:
    phrases = fobj.readlines()

log = open("log.txt", "a+")
done = 0
used = []
now = datetime.now()

while not done:
    sock.listen(2)

    client, addr = sock.accept()

    print("Connection: {}\t{}".format(addr, now.strftime("%d/%m/%y %H:%M:%S")))
    log.write("Connection: {}\t{}".format(addr, now.strftime("%d/%m/%y %H:%M:%S")))

    phrase = random.choice(phrases)
    while phrase in used:
        phrase = random.choice(phrases)

        if len(used) == len(phrases):
            phrase = "Sorry. I am all out of phrases :(\nTher will be more!"
            done = 1

    used.append(phrase)
    client.send(phrase.encode())
    client.close()
