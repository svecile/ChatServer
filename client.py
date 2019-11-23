import socket 
import select 
import sys 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#input server ip
print("Enter server IP address: ")
IP = str(input()) 
#input port number for the server
print("Enter server port number: ")
port = int(input())
#connects to server using IP and Port
server.connect((IP, port))

while True: 
# maintains a list of possible input streams 
    sockets_list = [sys.stdin, server] 
#below code: if retrieving from server, go to "if" statement
#if sending to server go to "else" statement
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048).decode() 
            print (message) 
        else:
           
            message = str(input()) 
            server.send(message.encode())
            sys.stdout.write("\n<You>") 
            sys.stdout.flush() 
server.close() 
