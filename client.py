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
            flag = 1
            client_socket.close()
        chatWindow.destroy()

    def receive():
        """Handles receiving of messages."""
        while True:
            if flag:
                break
            try:
                recvMessage = client_socket.recv(4096).decode("utf8")
                msg_list.insert(END, recvMessage)
                msg_list.yview_moveto(1)
            except OSError:  # Possibly client has left the chat.
                break

    def send(event=None):  # event is passed by binders.

        """Handles sending of messages."""
        msg = my_msg.get()
        my_msg.set("")  # Clears input field.
        try:
            client_socket.send(bytes(msg, "utf8"))
        except:
            updateSendText.set("Message not sent. Connection may have lost")
            reconnectButton.config(state="normal")

    flag = 0
    sendToServer = 1
    chatWindow = Toplevel(root)
    chatWindow.title("Chat Away!")
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
    msg_list = Listbox(messages_frame, height=15, width=80,
                       yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    msg_list.pack(side=LEFT, fill=BOTH)
    msg_list.pack()
    messages_frame.pack()
    entry_field = Entry(chatWindow, textvariable=my_msg, width = 65)
    entry_field.bind("<Return>", send)
    entry_field.pack(pady=5)
    send_button = Button(chatWindow, text="Send", command=send)
    send_button.pack()

    reconnectButton = Button(chatWindow, text="Reconnect To Server", command=reconnect, fg="green", state=DISABLED)
    reconnectButton.pack()

    chatWindow.protocol("WM_DELETE_WINDOW", on_closing)
    ADDR = ("54.162.255.141", 3000)

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
   


def closeMain():
    root.quit()


root = Tk()
root.title("Configure Connection")

width = 500
height = 400
root.minsize(width=width, height=height)

containingFrame = Frame(root)
containingFrame.pack(pady=30)

ipFrame = Frame(root)
ipFrame.pack(pady=10)
# input server ip
ipLabel = Label(ipFrame, text="Enter server IP address: ")
ipLabel.config(font=("Helvetica", 12))
ipLabel.pack()
ip_entry = StringVar()
ip_entry_field = Entry(ipFrame, textvariable=ip_entry, width="60")
ip_entry_field.pack()

# print("Enter server IP address: ")
# IP = str(input())

portFrame = Frame(root)
portFrame.pack(pady=10)
# input port number for the server
portLabel = Label(portFrame, text="Enter server port number: ")
portLabel.config(font=("Helvetica", 12))
portLabel.pack()
port_entry = StringVar()
port_entry_field = Entry(portFrame, textvariable=port_entry, width="60")
port_entry_field.pack()

nameFrame = Frame(root)
nameFrame.pack(pady=10)
# input for user's name
nameLabel = Label(nameFrame, text="Enter your name: ")
nameLabel.config(font=("Helvetica", 12))
nameLabel.pack()
name_entry = StringVar()
name_entry_field = Entry(nameFrame, textvariable=name_entry, width="60")
name_entry_field.pack()

connect_button = Button(root, text="Connect", command=connect,
                        relief=GROOVE, width="15", height="1", fg="green")
connect_button.pack(pady=10)

exit_button = Button(root, text="Exit", command=closeMain,
                     relief=GROOVE, width="15", height="1", fg="red")
exit_button.pack(pady=10)


# ----Now comes the sockets part----

root.mainloop()  # Starts GUI execution.
