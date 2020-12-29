import socket
import re
import winsound
import tkinter
import threading
import getpass
import os
import traceback
import io

from tkinter.simpledialog import askstring
from tkinter.messagebox import showerror

path = r"C:\Users\{}\AppData\Local\Temp\twitch_sound_chat.txt"
path = path.format(getpass.getuser())

root = tkinter.Tk()


def new_nickname_token():
    nickname = askstring("Channel name", "Channel name",).lower()
    token = askstring(
        "Token",
        "Write your token. Get one acessing https://twitchapps.com/tmi/",
        show="*")

    with open(path, 'w', encoding="utf-8") as fp:
        fp.write('\n'.join([nickname, token]))

    return nickname, token


if not os.path.exists(path):
    nickname, token = new_nickname_token()
else:
    with open(path, encoding="utf-8") as fp:
        nickname, token = fp.readlines()

muted = tkinter.IntVar()


tkinter.Button(root, text="Reset", command=new_nickname_token).grid(column=1,
                                                                    row=1)
tkinter.Checkbutton(root, text="Muted", variable=muted).grid(column=2, row=1)


def main():
    string_io = io.StringIO()
    try:
        sock = socket.socket()
        sock.connect(('irc.chat.twitch.tv', 6667))

        sock.send(f"PASS {token}\n".encode('utf-8'))
        sock.send(f"NICK {nickname}\n".encode('utf-8'))
        sock.send(f"JOIN #{nickname}\n".encode('utf-8'))

        while True:
            resp = sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))

            resp = re.search(
                r':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', resp)
            if resp and not muted.get():
                winsound.Beep(500, 100)
    except Exception:
        traceback.print_exc(file=string_io)
        showerror("Error", string_io.getvalue())
        root.quit()


thread = threading.Thread(target=main, daemon=True)
thread.start()

root.mainloop()
