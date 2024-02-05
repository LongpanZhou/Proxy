from socket import *
import sys
if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
try:
    # If in format of serverIP:Port
    serverHostName, serverPort = sys.argv[1].split(":")
except ValueError:
    # If there is not enough to unpack, set serverPort to the default value 8888
    serverHostName = sys.argv[1]
    serverPort = 8888

print("Server Host Name:", serverHostName)
print("Server Port:", serverPort)

tcpSerSock.bind((serverHostName, int(serverPort)))
tcpSerSock.listen(1)
print("The server is running...")
# Fill in end.

while 1:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    #message = tcpCliSock.recv(1024) # Fill in start. # Fill in end
    message = tcpCliSock.recv(4096).decode("utf-8")
    print(message)

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "wr")
        outputdata = f.readlines()
        fileExist = "true"

        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(bytes("HTTP/1.0 200 OK\r\n","utf-8"))
        tcpCliSock.send(bytes("Content-Type:text/html\r\n","utf-8"))
        # Fill in start.
        for i in outputdata:
            tcpCliSock.send(bytes(i, "utf-8"))
        # Fill in end.
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = None
            # Fill in start
            c = socket(AF_INET, SOCK_STREAM)
            # Fill in end.
            hostn = filename.replace("www.","",1)
            print(hostn)
            try:
                # Connect to the socket to port 80

                # Fill in start.
                c.connect((hostn, 80))
                # Fill in end.

                # Create a temporary file on this socket and ask port 80
                # for the file requested by the client
                fileobj = c.makefile('wr', 1)
                fileobj.write("GET "+"http://" + filename + "HTTP/1.0\n\n")

                # Read the response into buffer
                # Fill in start.
                buffer = fileobj.readlines()
                tmpFile = open("./" + filename,"wb")
                # Fill in end.

                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket
                # and the corresponding file in the cache

                # Fill in start.
                for line in buffer:
                    tmpFile.write(bytes(line, "utf-8"))
                    tcpCliSock.send(bytes(line, "utf-8"))
                # Fill in end.
                tmpFile.close()
            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            # Fill in start.
            tcpCliSock.send(bytes("HTTP/1.0 404 Not Found\r\n","utf-8"))
            tcpCliSock.send(bytes("Content-Type:text/html\r\n","utf-8"))
            tcpCliSock.send(bytes("\r\n","utf-8"))
            # Fill in end.
    # Close the client and the server sockets
    tcpCliSock.close()
#Unreable
tcpSerSock.close()