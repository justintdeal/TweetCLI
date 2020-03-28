from socket import * 
import sys
import _thread as thread

activeUsers = []
userToPort = dict()
hashToUser = dict()
userToHash = dict()

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
            if (user not in userToHash.keys()):
                userToHash[user] = []
            userToPort[user] = conn
            thread.start_new_thread(newClient, (conn,))
        

def newClient(conn):

    while True:
        print('newClient')
        data = conn.recv(1024).decode().split()
        if (data[0] == "sub"): #putting hashtags away
            user = data[1] #saving data
            tag = data[2]
            print(tag) #get rid of later
            if (tag not in hashToUser.keys()): # add hashtag to keys if not already saved 
                hashToUser[tag] = []
            
            if (len(userToHash[user]) >= 3): #lenght check for subscriptions
                print("sub <hashtag> failed, already exists or exceeds 3 limitation")
                # sys.exit()
            if (user not in hashToUser[tag]): #add user to tag key
                hashToUser[tag].append(user)
            if (tag not in userToHash[user]): #add tag to user key
                userToHash[user].append(tag)
            conn.sendall(("good").encode())

    
        if (data[0] == "tweet"): #if tweet is called
            message = data[1] #saving data
            tag = data[2]
            for use in activeUsers: #loop through all active users
                if "#ALL" in userToHash[use] or tag in userToHash[use]: #check if tag or ALL is in their set of subscriptions
                    userToPort[use].sendall(("rep " + str(use)+" "+ str(message)+ " " + str(tag)).encode()) #send to client to display

            
        # conn.sendall(data.enconde())

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