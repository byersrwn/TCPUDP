import socket
import sys

def main():
    # grab the inputs and store them in variables
    hostname = sys.argv[1]
    port = sys.argv[2];
    socketType = sys.argv[3]
    mode = sys.argv[4]
    if(sys.argv.__len__() == 6): #if there is a file path, store it in a variable
        filePath = sys.argv[5]

    if(socketType == "TCP"): #if the socket type is TCP, follow the TCP steps
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a TCP socket
        client_socket.connect((hostname, int(port))) #connect to the server
        if(mode == "send"): #if the mode is send, open the file and send the contents to the server
            fileToSend = open(filePath, "r")
            client_socket.send(fileToSend.read().encode('utf-8')) #send the contents of the file to the server
            fileToSend.close() #close the file
            client_socket.close() #close the socket
        elif(mode == "receive"): #if the mode is receive, send the word "receive" to the server and receive the message from the server
            client_socket.send(mode.encode('utf-8'))
            messageFromServer = client_socket.recv(3000).decode('utf-8') #receive 3000 bytes (each char is 1 byte) of message from the server
            print("Message received from server:")
            print(messageFromServer) #print the message received from the server
            client_socket.close() #close the socket
    elif(socketType == "UDP"):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create a UDP socket
        if(mode == "send"): #if the mode is send, open the file and send the contents to the server
            fileToSend = open(filePath, "r")
            client_socket.sendto(fileToSend.read().encode('utf-8'), (hostname, int(port))) #send the contents of the file to the server
            fileToSend.close() #close the file
            client_socket.close() #close the socket
        elif(mode == "receive"):
            client_socket.sendto(mode.encode('utf-8'), (hostname, int(port))) #if the mode is receive, send the word "receive" to the server. "mode" happens to be "receive" in this case
            messageFromServer, serverAddress = client_socket.recvfrom(3000) #receive 3000 bytes of message from the server
            print("Message received from server:")
            print(messageFromServer.decode('utf-8')) #print the message received from the server
            client_socket.close()

if __name__ == "__main__":
    main()