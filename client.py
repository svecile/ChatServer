"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *


def connect():

    def reconnect():
        chatWindow.destroy()

    def on_closing(event=None):
        if sendToServer:
            """This function is to be called when the window is closed."""
            my_msg.set("dsnfjnd")
            send()
            client_socket.close()
        chatWindow.destroy()

    def receive():
        """Handles receiving of messages."""
        while True:
            try:
                recvMessage = client_socket.recv(4096).decode("utf8")
                if recvMessage == "dsnfjnd":
                    break
                msg_list.insert(END, recvMessage)
                msg_list.yview_moveto(1)
            except OSError:  # Client may have left the chat and handles closing the thread when the chat window exits
                break
        print("Test")

    def send(event=None):  # event is passed by binders.

        """Handles sending of messages."""
        msg = my_msg.get()
        my_msg.set("")  # Clears input field.
        try:
            client_socket.send(bytes(msg, "utf8"))
        except:
            updateSendText.set("Message not sent. Connection may have lost")
            reconnectButton.config(state="normal")

    sendToServer = 1
    chatWindow = Toplevel(root)
    chatWindow.title("Chat Away!")
    chatWindow.grab_set()
    width = 800
    height = 400
    chatWindow.minsize(width=width, height=height)

    updateText = StringVar()
    updateShow = Label(chatWindow, textvariable=updateText, width="100", fg="red")
    updateShow.pack()

    updateSendText = StringVar()
    updateSendShow = Label(chatWindow, textvariable=updateSendText, width="100", fg="red")
    updateSendShow.pack()

    messages_frame = Frame(chatWindow)
    my_msg = StringVar()  # For the messages to be sent.
    scrollbar = Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = Listbox(messages_frame, height=15, width=120, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    msg_list.pack(side=LEFT, fill=BOTH)
    msg_list.pack()
    messages_frame.pack()

    inputFrame = Frame(chatWindow)
    inputFrame.pack(pady=5)
    entry_field = Entry(inputFrame, textvariable=my_msg, width = 65)
    entry_field.bind("<Return>", send)
    entry_field.grid(column=0, row=0, padx=5)
    send_button = Button(inputFrame, text="Send", command=send, relief=GROOVE)
    send_button.grid(column=1, row=0)

    reconnectButton = Button(chatWindow, text="Reconnect To Server", command=reconnect, fg="green", state=DISABLED, relief=GROOVE)
    reconnectButton.pack(pady=20)

    chatWindow.protocol("WM_DELETE_WINDOW", on_closing)
    ADDR = ("3.83.189.76", 3000)

    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect(ADDR)
    except:
        sendToServer = 0
        updateText.set(
            "Cannot connect to the server. Make sure it is running OR make sure the info you have entered is correct!")
        print("Server not found")
        send_button.config(state = "disabled" )
        reconnectButton.config(state = "normal")
    receive_thread = Thread(target=receive)
    receive_thread.start()

    print("DOne")
   


def closeMain():
    root.quit()


root = Tk()
root.title("Configure Connection")

width = 500
height = 400
root.minsize(width=width, height=height)

welcomeFrame = Frame(root)
welcomeLabel = Label(welcomeFrame, text="Welcome to the chat app!")
welcomeLabel.pack()
welcomeFrame.pack(pady=20)

connect_button = Button(root, text="Connect", command=connect, relief=GROOVE, width="15", height="1", fg="green")
connect_button.pack(pady=10)

exit_button = Button(root, text="Exit", command=closeMain, relief=GROOVE, width="15", height="1", fg="red")
exit_button.pack(pady=10)


# ----Now comes the sockets part----

root.mainloop()  # Starts GUI execution.
