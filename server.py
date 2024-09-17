import sys
import socket
from queue import Queue
import threading
import os

def main():
    port = sys.argv[1]
    socketType = sys.argv[2]
    # hostname = 'localhost'
    hostname = socket.gethostbyname(socket.gethostname())
    print(f"Hostname: {hostname}")
    global messageQueue #Single Global Queue to store all messages
    messageQueue = Queue()

    #Depending on the socket type, call the appropriate function
    if(socketType == "TCP"):
        TCP(hostname, port)
    elif(socketType == "UDP"):
        UDP(hostname, port)


def TCP(hostname, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create TCP socket
    server_socket.bind((hostname, int(port))) #bind on the hostname and port
    server_socket.listen(128) #Listen for incoming connections and queue up to 128 connections
    lock = threading.Lock() #Create thread lock to be used in critical section
    print(f"TCP server listening with hostname: {hostname} on port: {port}") #print statement to show server is online
    while True: #Infinite loop to keep server running
        client_socket, addr = server_socket.accept() #Accept incoming connection
        print(f"Connection established with {addr}") #Print statement to show connection established
        data = client_socket.recv(3000).decode('utf-8') #Receive 3000 bytes of data from client (3000 char data types)
        thread = threading.Thread(target=TCPThread, args=(client_socket, data)) #Create a thread to run critical code section (TCP Thread function)
        lock.acquire() # Before running thread, acquire lock to ensure that only 1 thread runs the TCPThread function at a time
        thread.start() # Start the thread
        thread.join() # Wait for the thread to finish to ensure that the global messageQueue has the addition or subtraction of messages completed. Only 1 thread can add or delete messages from the queue at once.
        lock.release() # Release the lock to allow other threads to run the critical section

#Critical code section which modifies the global shared messageQueue
def TCPThread(client_socket, data):
    if(data == "receive"): #if the client send the message "receive", then send the first message in the queue to the client and return
        if(messageQueue.empty()): #if the queue is empty, send an error message to the client and return
            client_socket.send("Error: No Messages".encode('utf-8'))
            return
        message = messageQueue.get() #queue is not empty and the client is asking for a message, grab the next message in the queue and send back
        client_socket.send(message.encode('utf-8')) #send the message to the client
        return
    messageQueue.put(data) #if the client is not asking for a message, then add the message to the queue and send nothing back to the client

def UDP(hostname, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Create UDP socket
    server_socket.bind((hostname, int(port))) #Bind the socket to the hostname and port
    lock = threading.Lock() #Create a lock to be used in the critical section
    print(f"UDP server online with hostname: {hostname} on port: {port}") #Print statement to show server is online
    while True:
        data, cli_addr = server_socket.recvfrom(3000) #Receive 3000 bytes of data from the client (char data types are 1 byte)
        thread = threading.Thread(target=UDPThread, args=(data, cli_addr, server_socket)) #Create a thread to run the critical code section (UDPThread function)
        lock.acquire() #Acquire the lock to ensure only 1 thread runs the critical section at a time
        thread.start() #Start the thread
        thread.join() #Wait for the thread to finish to ensure the global messageQueue has the addition or subtraction of messages completed. Only 1 thread can add or delete messages from the queue at once.
        lock.release() #Release the lock to allow other threads to run the critical section
        
def UDPThread(data, cli_addr, server_socket):
    if(data.decode('utf-8') == "receive"): #if the client sends the message "receive", then send the first message in the queue to the client and return
        if(messageQueue.empty()):  #if the queue is empty, send an error message to the client and return
            server_socket.sendto("Error: No Messages".encode('utf-8'), cli_addr ) #Send back the error message to the client
            return
        message = messageQueue.get() #queue is not empty and the client is asking for a message, grab the next message in the queue to send back
        server_socket.sendto(message.encode('utf-8'), cli_addr) #send the message to the client
        return
    messageQueue.put(data.decode('utf-8')) #if the client is not asking for a message, then add the message to the queue and send nothing back to the client

if __name__ == "__main__":
    main()

        
    
    # Define the IP address and the port number the server will listen on
# host = 'localhost'  # Localhost
# port = 12345

# # Bind the socket to the address and port
# server_socket.bind((host, port))

# # Listen for incoming connections (allow up to 5 connections to queue)
# server_socket.listen(5)
# print(f"Server listening on {host}:{port}")

# while True:
#     # Accept a connection
#     client_socket, addr = server_socket.accept()
#     print(f"Connection established with {addr}")
    
#     # Receive data from the client (maximum 1024 bytes)
#     data = client_socket.recv(1024).decode('utf-8')
#     print(f"Received from client: {data}")
    
#     # Send a response back to the client
#     response = f"Server received: {data}"
#     client_socket.send(response.encode('utf-8'))
    
#     # Close the connection with the client
#     client_socket.close()

