import random
import socket
import time
import re
import threading

changeColor = True
newColor = 000000
    
user = ""
channel = ""


oauth = "oauth:"
# get your oauth token here: https://twitchapps.com/tmi/

s = socket.socket()
channels = []

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

s.connect(("irc.chat.twitch.tv", 6667))
s.send(bytes("PASS " + oauth + "\r\n", "UTF-8")) # joins twitch chat
s.send(bytes("NICK " + user + "\r\n", "UTF-8"))
#for channel in channels:
    #s.send(bytes("JOIN #" + channel + "\r\n", "UTF-8"))
    #uncomment this if you want it to be in more than one channel
s.send(bytes("JOIN #" + channel + "\r\n", "UTF-8"))

def chat(msg):
    blab = "PRIVMSG #" + user + " :"  + msg + "\r\n"
    s.send(bytes(str(blab), 'utf-8'))

def randomColor():
   return ''.join([random.choice('0123456789ABCDEF') for x in range(6)])

while True:
    response = s.recv(1027).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", response).group(0)
        message = CHAT_MSG.sub("", response)
        msg = message.lower()
        
        if username == user or username == channel:
            if msg.startswith("off"):
                if changeColor == True:
                    changeColor = False
                    chat('/color #' + defaultColor)
                    print("No longer changing colors!")
                else:
                    print("Not changing colors!")

            elif msg.startswith("on"):
                if changeColor == False:
                    changeColor = True
                    print("Now changing colors!")
                else:
                    print("Already changing colors!")
            elif changeColor == True and username == user:
                newColor = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])

                chat("/color #" + newColor)
                print(newColor)

        print(channel + "> " + username + ": " + message)
