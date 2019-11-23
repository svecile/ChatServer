import socket 
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

IP='0.0.0.0'
port=3000

print("How many chat rooms would you like?")
numRooms = int(input())

#make a room list with a lists embedded in it to hold the clients in each room
roomList=[]
for x in range(0, numRooms):
    roomList.append([])
    

#binds the server to the entered ip and port number, client needs to know these to connect
server.bind((IP, port)) 
  
#server listens for up to 100 connections
server.listen(100)


clientThreads = []

print("Server up and running on IP " +IP+ " and port "+str(port))

def clientthread(conn, addr): 
  
    #Let client know they are connected
    m="Connected successfully! What is your name?"
    conn.send(m.encode())
    name = conn.recv(2048).decode()
    
    m = "Hello " +name+ "! There are currently "+str(len(roomList))+" rooms which room would you like to join?"
    conn.send(m.encode())
    room = int(conn.recv(2048).decode())
    roomList[room-1].append(conn)
    
    m="You are now in chat room "+str(room)
       
    
    while True: 
            try: 
                message = conn.recv(4096).decode()
                
                if message=='done':
                    msg= name+' has left the chat!'
                    sendAll(msg.encode(), conn, room)
                    removeClient(conn, room) 
                    conn.close()
                    break
                
                if message: 
  
                    #prints the name and msg that was just sent to the server
                    print("From: " + name +" Message:" + message) 
  
                    # Calls sendAll function to send a message to all clients in the room
                    msg = "From: " + name +" Message: " + message 
                    sendAll(msg.encode(), conn, room) 
  
                else: 
                    #If the message has no content there may be a connection error so remove the client
                    removeClient(conn, room) 
  
            except: 
                continue
  

#sends a message to all clients in the chat except yourself
def sendAll(msg, connection, roomNum): 
    for client in roomList[roomNum-1]: 
        try: 
            client.send(msg) 
        except: 
            client.close() 

            # if the link is broken, we remove the client 
            removeClient(client, roomNum) 
  

#removes a client from the client list if the connection is closed
def removeClient(connection, room): 
    if connection in roomList[room-1]: 
        roomList[room-1].remove(connection) 


while True: 

    #accepts a connection request and sores the client socket object and ip address
    conn, addr = server.accept() 
  
    # prints the address of the user that just connected 
    print (addr[0] + " connected")
  
    # creates and individual thread for every user  
    # that connects 
    thread = threading.Thread(target=clientthread, args=(conn, addr))
    thread.start()
    
    #adds new client thread to the list
    clientThreads.append(thread) 


conn.close() 
server.close()










