import socket 
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

IP='0.0.0.0'
port=3000

endFlag= False

#enter number of chat rooms the server should support
print("How many chat rooms would you like?")
numRooms = int(input())

#list to hold all client threads so we can join them to the main thread when the server shuts down
clientThreads = []

#make a 2D room list where the rows are the different chat rooms and each spot in a row is a client connection
roomList=[]
for x in range(0, numRooms):
    roomList.append([])
    

#binds the server to the entered ip and port number, client needs to know these to connect
server.bind((IP, port)) 
  
#server listens for up to 100 connections
server.listen(100)

#set server socket timeout to 3 so it doesnt block forever when waiting to accept connections (this is so server thread can terminate gracegully)
server.settimeout(3)

#client thread that is created each time a client connects
def clientthread(conn, addr): 
    
    #set client connection timeout so when it blocks on recv() it will eventually timeout (this is so client thread can terminate gracegully)
    conn.settimeout(3)
    
    room=""
    #flag for main loop when client is chatting in the chatroom different from end flag so it only closes the current client
    flag = True
    
    #Let client know they are connected
    m="Connected successfully! What is your name?"
    conn.send(m.encode())
    
    #recv() will eventually timeout and cause an acception which will be caught and allow it to continue waiting for input
    #but if the server has started to shutdown the endFlag will become true and will break the loop
    name=""
    while not(endFlag):
            try:
                #wait for client to send a message
                name = conn.recv(2048).decode()
            except:
                #this string is sent by the client when it closes the connection from its side so the client thread can terminate on the server
                if name=='dsnfjnd':
                    flag=False
                    break
                #this is so when the client supplies a name it will break this loop and move on to the next part of the code
                elif name!= "":
                    break
                #if client hasnt given a name and also hasnt closed the connection continue waiting for a message
                continue
    
    #this is so if the client has closed its connection or the server has started to shutdown before the room number is entered it will skip this section
    if not(name=='dsnfjnd') and not(endFlag):
        
        #ask which chat room the client would like to join
        m = "Hello " +name+ "! There are currently "+str(len(roomList))+" rooms which room would you like to join?"
        conn.send(m.encode())
        
        #same logic as first recv loop
        room=""
        while not(endFlag):
                try:
                    room = conn.recv(2048).decode()
                except:
                    if room=='dsnfjnd':
                        flag=False
                        break
                    elif room!= "":
                        break
                    continue
        
        #make sure a valid room number is entered
        while(not(isNumber(room)) or int(room)>numRooms or int(room)<0):
            
            #if the server is shutting down or client has exited break this loop and set flag for main receiving loop to false
            if endFlag or room =='dsnfjnd':
                flag=False
                break
            
            #give them a chance to enter a valid room number
            m="Error you did not enter a number or the number is not valid, Please enter a valid room number: "
            conn.send(m.encode())
            
            room=""
            while not(endFlag):
                    try:
                        room = conn.recv(2048).decode()
                    except:
                        if room=='dsnfjnd':
                            flag=False
                            break
                        elif room!= "":
                            break
                        continue

        #if room is a number add client connection to room of their choice
        if isNumber(room):
            room = int(room)
            roomList[room-1].append(conn)
            
            #tell client they are connected
            m="You are now connected to chat room "+str(room)+"!"
            conn.send(m.encode())
    
    #if the client has exited at any point dont enter main message receiving loop  
    if name=='dsnfjnd' or room=='dsnfjnd':
        flag=False

    conn.settimeout(5)
    
    #main while loop for receiving client messages and sending them to everyone in the chat room
    while flag:
        
        #check if server is shutting down
        if endFlag:
            break
        
        try: 
            message = conn.recv(4096).decode()
            
            #if the client has disconnected break loop
            if message=='dsnfjnd':
                msg= name+' has left the chat!'
                sendAll(msg.encode(), conn, room)
                removeClient(conn, room)
                break
            
            #if a message has been received from client send it to everyone in the chat room
            if message: 
                #prints the name and msg that was just sent to the server
                print("From: " + name +" Message:" + message) 
                
                # Calls sendAll function to send a message to all clients in the room
                msg = "From: " + name +" Message: " + message 
                sendAll(msg.encode(), conn, room) 
            else:
                #If the message has no content there may be a connection error so remove the client
                removeClient(conn, room)
                break
                
        except:
            continue
    
    #remove client from room because thread is exiting          
    if not(room=="") and isNumber(room):
        removeClient(conn, room)
    
    #if server is shutting down tell client so it can close properly 
    if endFlag:
        m="dsnfjnd"
        conn.send(m.encode())
    
    #close the connection  
    conn.close()
    print(addr[0]+" has disconnected!")
    

#sends a message to all clients in the chat
def sendAll(msg, connection, roomNum): 
    for client in roomList[roomNum-1]: 
        try: 
            client.send(msg) 
        except:
            client.close()
            # if the link is broken, we remove the client 
            removeClient(client, roomNum) 
            
  

#removes a client from the room list if the connection is closed
def removeClient(connection, room):
    if connection in roomList[room-1]: 
        roomList[room-1].remove(connection)
        
#check if a value is a number      
def isNumber(s):
    try:
        #attempt cast to int if it throws an exception return false otherwise return true
        int(s)
        return True
    except ValueError:
        return False
        
#server control thread that waits for incoming client connections 
def serverThread():
    
    #while the end flag is false keep waiting for client connections
    while not(endFlag): 
    
        try: 
            #accepts a connection request and sores the client socket object and ip address
            #timeout was set for accept() blocking call so that if the server shuts down it can exit
            #when timeout happens an exception is thrown which is caught
            conn, addr = server.accept()
            
            # prints the address of the user that just connected 
            print (addr[0] + " connected")
            
            # creates and individual client thread for every user that connects 
            thread = threading.Thread(target=clientthread, args=(conn,addr))
            thread.start()
            
            #adds new client thread to the list
            clientThreads.append(thread)
            
        except:
            continue

#start server control thread
serverT = threading.Thread(target=serverThread)
serverT.start()

print("Server up and running on IP " +IP+ " and port "+str(port) +"\n")

#wait for enter to be pressed to close the server
input("Press Enter to close server...\n")

#set end flag so client threads can break while loop and close properly
endFlag=True

#join any client threads that havent exited yet to the main thread so they can finish their execution before main thread exits
for client in clientThreads:
    client.join()
    print(str(client.getName())+" closed")

#wait for server thread to finish if it hasnt already
if serverT.is_alive():
    serverT.join()

#close server socket
server.close()

print('Server closed gracefully')









