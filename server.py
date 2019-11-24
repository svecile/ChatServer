import socket 
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

IP='0.0.0.0'
port=3000

print("How many chat rooms would you like?")
numRooms = int(input())

clientThreads = []
#make a room list with a lists embedded in it to hold the clients in each room
roomList=[]
for x in range(0, numRooms):
    roomList.append([])
    

#binds the server to the entered ip and port number, client needs to know these to connect
server.bind((IP, port)) 
  
#server listens for up to 100 connections
server.listen(100)


def clientthread(conn,addr): 
    
    flag= True
    
    #Let client know they are connected
    m="Connected successfully! What is your name?"
    conn.send(m.encode())
    name = conn.recv(2048).decode()
    
    if not(name=='dsnfjnd'):
        
        m = "Hello " +name+ "! There are currently "+str(len(roomList))+" rooms which room would you like to join?"
        conn.send(m.encode())
        room = conn.recv(2048).decode()
        
        #make sure a valid room number is entered
        while(not(isNumber(room)) or int(room)>numRooms or int(room)<0):
            
            if room =='dsnfjnd':
                flag=False
                break
            
            m="Error you did not enter a number or the number is not valid, Please enter a valid room number: "
            conn.send(m.encode())
            room = conn.recv(2048).decode()
            
    
        if isNumber(room):
            room = int(room)
            roomList[room-1].append(conn)
        
            m="You are now connected to chat room "+str(room)+"!"
            conn.send(m.encode())
       
    if name =='dsnfjnd':
        flag=False
                
    while flag: 
            try: 
                message = conn.recv(4096).decode()
                
                if message=='dsnfjnd':
                    msg= name+' has left the chat!'
                    sendAll(msg.encode(), conn, room)
                    removeClient(conn, room)
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
            
    conn.close()
    print(addr[0]+" has disconnected!")
    

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
        
def isNumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def serverThread():
    
    flag=True
    
    while flag: 
    
        #accepts a connection request and sores the client socket object and ip address
        conn, addr = server.accept()
        
        # prints the address of the user that just connected 
        print (addr[0] + " connected")
      
        # creates and individual thread for every user  
        # that connects 
        thread = threading.Thread(target=clientthread, args=(conn,addr))
        thread.start()
        
        #adds new client thread to the list
        clientThreads.append(thread) 
    

    
    conn.close()

#start server thread
serverT = threading.Thread(target=serverThread)
serverT.start()

print("Server up and running on IP " +IP+ " and port "+str(port) +"\n")

input("Press Enter to close server...")

#close all client connections
for r in roomList:
    for c in r:
        c.close()
        
#set clag for all client threads       
for client in clientThreads:
    client.flag=False
    print(str(client)+" closed")

server.close()

print('Server closed gracefully')









