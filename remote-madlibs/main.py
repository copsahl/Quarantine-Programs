#!/usr/bin/python3
import socket
import random
import re

def getWord(wordType, sock):
    ask = "Please give me a {}: ".format(wordType)
    sock.send(ask.encode())
    word = sock.recv(256)
    return word.decode()

def getWordTypes(madlib):
    regex = re.compile(r'[A-Z_]{2,}')
    try:
        x = regex.findall(madlib)
    except:
        return -1
        
    return x

def getMadLib(madlibs, used):
    
    choice = random.choice(madlibs)
    return choice

def assembleMadLib(words, wordTypes, madlib):
    counter = 0
    new = madlib
    for x in wordTypes:
        madlib = new
        new = re.sub(x, words[counter], madlib, 1)
        counter += 1

    return new


def main():
    
    used = []
    clientWords = []
    
    final = ""

    with open("madlibs.txt", "r") as fobj:
        data = fobj.readlines()
    
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('',1337))
    sock.listen(2)
    client, addr = sock.accept()
    
    currMadLib = getMadLib(data, used)
    if currMadLib == -1:
        client.send("All out of madlibs! Oh No!")
        client.close()
        exit()
    
    wordTypes = getWordTypes(currMadLib)
    for wordType in wordTypes:
        clientWord = getWord(wordType, client)
        clientWords.append(clientWord)
        
    for x in range(0, len(clientWords)):
        clientWords[x].rstrip()

    final = assembleMadLib(clientWords, wordTypes, currMadLib)
    final = final.split(" ")
    final.pop(0)
    
    ml = " ".join(final)
    client.send("Your MADLIB is done! Enjoy!\n\n".encode())
    client.send(ml.encode())
    client.close()

    with open("results.txt", "a+") as fobj:
        fobj.write(ml + "\n\n")


if __name__ == "__main__":
    while True:
        main()
