"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            recvMessage = client_socket.recv(4096).decode("utf8")
            msg_list.insert(END, recvMessage)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        root.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

root = Tk()
root.title("Chat Client Connection")

messages_frame = Frame(root)
my_msg = StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = Entry(root, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = Button(root, text="Send", command=send)
send_button.pack()

root.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----

ADDR = ("127.0.0.1", 3000)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
root.mainloop()  # Starts GUI execution.
