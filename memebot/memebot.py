#!/usr/bin/python3
import random
import socket, string, time, ssl
import urllib, re
import time
import json, requests
import os
import string

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "" # Server
channel = "" # Channel
keys = "" # Keys
botnick = "memebot" # Your bots nick
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

def memegather(subreddit):
    r = requests.get(
        'http://www.reddit.com/r/{}.json?=100'.format(subreddit),
        headers={'user-agent': 'Mozilla/5.0'})

    memes = []

    for post in r.json()['data']['children']:
        memes.append(post['data']['url'])

    del memes[0]

    meme = random.choice(memes)
    return meme


def main():


    joinchan(channel)
    while 1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]

            if len(name) < 25:

                if message.find('!dankmeme') != -1:
                    sendmsg(str(memegather('dankmemes')))

                if message.find('!meme') != -1:
                    sendmsg(str(memegather('memes')))

                if message.find('!irlmeme') != -1:
                    sendmsg(str(memegather('memesirl')))

                if message.find('!surrealmeme') != -1:
                    sendmsg(str(memegather('surrealmemes')))

                if message.find('!nukedmeme') != -1:
                    sendmsg(str(memegather('nukedmemes')))

                if message.find('!wholememe') != -1:
                    sendmsg(str(memegather('wholesomememes')))

                if message.find('!friedmeme') != -1:
                    sendmsg(str(memegather('deepfriedmemes')))


                if message.find(botnick + ': help') != -1:
                    sendmsg("-----------meme menu--------------")
                    sendmsg("!meme")
                    sendmsg("!dankmeme")
                    sendmsg("!irlmeme")
                    sendmsg("!surrealmeme")
                    sendmsg("!nukedmeme")
                    sendmsg("!wholememe")
                    sendmsg("!friedmeme")


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
