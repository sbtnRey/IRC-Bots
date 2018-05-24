#!/usr/bin/python3
import random
import socket, string, time, ssl
import urllib, re
import time
from random import shuffle
import random


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "" # Server
channel = "" # Channel
keys = "" # Keys
botnick = "homestuckbot" # Your bots nick
adminname = "" #IRC nickname
exitcode = "begone " + botnick

socket.connect((server, 9999)) # Here we connect to the server using the port 6667

ircsock = ssl.wrap_socket(socket)

ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) #We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # assign the nick to the bot


def joinchan(chan): # join channel(s).

    ircsock.send(bytes("JOIN "+ chan + keys + "\r\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

def ping(): # respond to server Pings.
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

def sendmsg(msg, target=channel): # sends messages to the target.
    ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))

def main():


    cList = open("corn.txt").read().splitlines()


    joinchan(channel)
    while 1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]

            if len(name) < 25:


                if message.find('!corn') != -1:
                    randIndex = random.randint(1, 403)
                    ranko = re.split(':\\b',cList[randIndex])[-1]
                    corn = re.split(':\\b',cList[randIndex])[0]

                    sendmsg(str(corn) + ", Rank: " + str(ranko))
                    if float(ranko) == 1:
                        sendmsg("Best numba ONE corn of all time, the triple S black diamond tier corn. This is the real corn god")
                    if float(ranko) >= 2 and float(ranko) <= 40:
                        sendmsg("Black diamond tier, cream of the crop when it comes to quality. Immeasurable rank, well kinda.")
                    if float(ranko) >= 41 and float(ranko) <= 68:
                        sendmsg("Top double S tier corn, not many stand this high and most fall to this corn king")
                    if float(ranko) == 69:
                        sendmsg("The S E X Y Tier. This corn takes the corn as the sexiest most desirable corn. Praise dem kernals")
                    if float(ranko) >= 70 and float(ranko) <= 120:
                        sendmsg("Premo corn S tier, a valient corn of corns that must be both trusted and respected to the Absolute")
                    if float(ranko) >= 121 and float(ranko) <= 160:
                        sendmsg("Upper semi mid tier (Otherwise known as A tier). Prestige runs within the veins of this beautiful corn")
                    if float(ranko) >= 161 and float(ranko) <= 200:
                        sendmsg("Mid B tier, nothin too much to brag about this corn. It's good, not great")
                    if float(ranko) >= 201 and float(ranko) <= 220:
                        sendmsg("Dingus B- tier. Many question this tier rank as poor, but a dingus corn is the corn I want to be")
                    if float(ranko) >= 221 and float(ranko) <= 240:
                        sendmsg("C tier. The corn is corn")
                    if float(ranko) >= 241 and float(ranko) <= 280:
                        sendmsg("bungo tier (C-). This corn doesn't deserve to live, but exists none the less")
                    if float(ranko) >= 281 and float(ranko) <= 320:
                        sendmsg("double bungo D tier. This is a garbage corn. Don't ever keep this corn around, or else.")
                    if float(ranko) >= 321 and float(ranko) <= 360:
                        sendmsg("Dirty bronze tier. This corn doesn't have a future and never will. Sorry bud")
                    if float(ranko) >= 361 and float(ranko) <= 402:
                        sendmsg("Sludge tier. This is corn is dark and heavily tainted. Stay away from this corn")
                    if float(ranko) == 403:
                        sendmsg("Worthless tier. This corn has earned the title of the worst corn ever. #notevencorn #ignore")
                    time.sleep(3)

                if message.find(botnick + ': help') != -1:
                    sendmsg("corn = corn")

                if message[:5].find('.tell') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                    else:
                        target = name
                        message = "Could not parse. The message should be in the format of '.tell [target] [message]' to work properly."
                    sendmsg(message, target)

                if name.lower() == adminname.lower() and message.rstrip() == exitcode:
                    sendmsg("lol bye ;-;")
                    ircsock.send(bytes("QUIT \n", "UTF-8"))
                    return
        else:
            if ircmsg.find("PING :") != -1:
                ping()

main()
