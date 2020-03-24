from socket import * 
import sys
import _thread as thread

activeUsers = []

def main(): 
    host = '127.0.0.1'
    port = validPort(sys.argv)
    sock = getAndBindSocket(host, port)
    while True: 
        conn, addr = sock.accept()
        user = conn.recv(1024).decode()
        if user in activeUsers: 
            print('here')
            conn.sendall("False".encode())
        else:
            conn.sendall("True".encode())
            activeUsers.append(user)
            thread.start_new_thread(newClient, (conn,))

def newClient(conn):
    while True:
        print('newClient')
        data = conn.recv(1024).decode()
        conn.sendall(data.enconde())
def validPort(args): 
    try: 
        port = int(args[1])
        if port >= 1024 and port <= 65535: 
            return port
    except: 
        sys.exit()

#helper to get a socket to interact with 
def getAndBindSocket(host, port):
    sock = socket(AF_INET, SOCK_STREAM)
    try: 
        sock.bind((host, port))
        sock.listen(1)
    except:
        print("UNABLE TO BIND TO SELECTED PORT")
        sys.exit()
    return sock

main()




main()