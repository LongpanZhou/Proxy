from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip] : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

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


while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode("utf-8")
    print(message)

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    # Check whether the file exist in the cache
    try:
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(bytes("HTTP/1.0 200 OK\r\n","utf-8"))
        tcpCliSock.send(bytes("Content-Type:text/html\r\n","utf-8"))

        for line in outputdata:
            tcpCliSock.send(bytes(line,"utf-8"))

        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)

            hostn = filename.replace("www.","",1)
            print(hostn)
            try:
                # Connect to the socket to port 80
                c.connect((hostn,80))

                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('rb', 0)
                fileobj.write(bytes(f"GET / HTTP/1.0\r\nHost: {hostn}\r\n\r\n", "utf-8"))

                # Read the response into buffer
                buffer = fileobj.readlines()

                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")

                for line in buffer:
                    tmpFile.write(line)
                    tcpCliSock.send(line)

            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found

            tcpCliSock.send(bytes("HTTP/1.0 404 Not Found\r\n","utf-8"))
            tcpCliSock.send(bytes("Content-Type:text/html\r\n","utf-8"))
            tcpCliSock.send(bytes("\r\n","utf-8"))

    # Close the client and the server sockets
    tcpCliSock.close()

# Unreachable
tcpSerSock.close()