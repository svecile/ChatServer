from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
import time


def connect():

    def reconnect():
        # Destroy the chat window
        chatWindow.destroy()

    def on_closing(event=None):
        if sendToServer:
            """This function is to be called when the window is closed."""
            # Send message to the server indication the client has quit
            sendMessage.set("dsnfjnd")
            send()
            time.sleep(1)
            clientSocket.close()
        chatWindow.destroy()

    def receive():
        """Handles receiving of messages."""
        while True:
            try:
                # Get the message from the server
                recvMessage = clientSocket.recv(4096).decode("utf8")
                # If the server responds with the closing message, write to the interface and break the loop
                if recvMessage == "dsnfjnd":
                    messageList.insert(END, "Server has disconnected!")
                    break
                messageList.insert(END, recvMessage)
                messageList.yview_moveto(1)
            # Client may have left the chat and handles closing the thread when the chat window exits
            except OSError: 
                break
        

    def send(event=None):  
        # Get the message from the input field
        msg = sendMessage.get()
        # Clear the input field.
        sendMessage.set("")  
        try:
            #  Send the message to the server
            clientSocket.send(msg.encode())
        except:
            # Notify the user in the update frame
            updateSendText.set("Message not sent. Connection may have lost")
            reconnectButton.config(state="normal")

    sendToServer = 1
    # Lines 56 to 69 is just GUI stuff
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

    messagesFrame = Frame(chatWindow)
    # Holder for the entered message
    sendMessage = StringVar()  
    scrollbar = Scrollbar(messagesFrame) 
    # List to contain the messages and display them to the user
    messageList = Listbox(messagesFrame, height=15, width=120, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    messageList.pack(side=LEFT, fill=BOTH)
    messageList.pack()
    messagesFrame.pack()

    inputFrame = Frame(chatWindow)
    inputFrame.pack(pady=5)
    entryField = Entry(inputFrame, textvariable=sendMessage, width = 65)
    # Allows the user to send to the server by clicking the enter (return) key
    entryField.bind("<Return>", send)
    entryField.grid(column=0, row=0, padx=5)
    send_button = Button(inputFrame, text="Send", command=send, relief=GROOVE)
    send_button.grid(column=1, row=0)

    reconnectButton = Button(chatWindow, text="Redirect to Home Page", command=reconnect, fg="green", state=DISABLED, relief=GROOVE)
    reconnectButton.pack(pady=20)

    chatWindow.protocol("WM_DELETE_WINDOW", on_closing)
    ADDR = ("3.83.189.76", 3000)

    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.connect(ADDR)
    except:
        # Don't allow sending to the server
        sendToServer = 0
        updateText.set(
            "Cannot connect to the server. Make sure it is running OR make sure the info you have entered is correct!")
        send_button.config(state = "disabled" )
        reconnectButton.config(state = "normal")
    # Create thread
    recvThread = Thread(target=receive)
    recvThread.start()
    
    

# Shut down the program
def closeMain():
    root.quit()

# Define the GUI root and set the title
root = Tk()
root.title("Configure Connection")
# Set the dimensions 
width = 500
height = 400
root.minsize(width=width, height=height)

welcomeFrame = Frame(root)
welcomeLabel = Label(welcomeFrame, text="Welcome to the chat app!")
welcomeLabel.pack()
welcomeFrame.pack(pady=20)

connectButton = Button(root, text="Connect", command=connect, relief=GROOVE, width="15", height="1", fg="green")
connectButton.pack(pady=10)

exitButton = Button(root, text="Exit", command=closeMain, relief=GROOVE, width="15", height="1", fg="red")
exitButton.pack(pady=10)

# Launch the GUI
root.mainloop()
