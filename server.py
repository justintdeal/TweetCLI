from socket import * 
import sys
import _thread as thread
import pickle

activeUsers = []
userToPort = dict()
userSubs = dict()
userTweets = dict()

######################################
#          Driver Method             #
# Determines if a user can login     #
# creates threads for new clients    #
######################################
def main(): 
    host = '127.0.0.1'
    port = validPort(sys.argv)
    sock = getAndBindSocket(host, port)

    while True: 
        conn, addr = sock.accept()
        user = conn.recv(1024).decode()
        if user in activeUsers: 
            ### Deny connection
            conn.sendall("False".encode())
        else:
            ### Allows connection, add user to active users, create client thread
            conn.sendall("True".encode())
            activeUsers.append(user)
            thread.start_new_thread(newClient, (conn,user))
        
#####################################
#        New Client Thread          #
# recieves data from client and     #
# delegates to preformAction func   #
#####################################
def newClient(conn, user):
    ### Initialize new client info and store connection 
    userSubs[user] = []
    userTweets[user] = []
    userToPort[user] = conn
    print('newClient')

    ### Listens for services requests 
    while True:
        data = conn.recv(1024).decode().split()
        print(data)
        preformAction(data)

#####################################
#   Handles Requests from Clients   #
#####################################
def preformAction(data):
    request = data[0]
    ### Handles subscibe functionality
    if (request == "sub"): 
        user = data[1]
        tag = data[2]
        subscribeToTag(user, tag) 
    ### Handles tweet functionality
    if (data[0] == "tweet"):
        user = data[3]
        message = data[1]
        tag = data[2]
        userTweets[user].append(message) # add tweet to user tweet history 
        for use in activeUsers:          # loop through all active users and broadcast tweets
            if "#ALL" in userSubs[use] or tag in userSubs[use]: #check if tag or ALL is in their set of subscriptions
                userToPort[use].sendall(("rep " + str(user)+" "+ str(message)+ " " + str(tag)).encode())
    ### Handles unsubscribing from a hashtag
    if (data[0] == "unsub"):
        user = data[1]
        tag = data[2]
        unsubFromTag(user, tag)
    ### Handles the get user features
    if data[0] == 'users':
        user = data[1]
        users = ["user"] + activeUsers
        print("WE MADE IT")
        onlineUsers = pickle.dumps(users)
        userToPort[user].send((onlineUsers))
    ### Handles getTweets, sends client all of it's previous tweets
    if data[0] == "getTweets":
        user = data[1]
        requestedUser = data[2]
        t = ["tweets"] + userTweets[requestedUser]
        tweets = pickle.dumps(t)
        userToPort[user].send(tweets)
    
#########################################
# Helpers for Subscirbe and Unsubscribe #
#########################################
def unsubFromTag(user, tag):
    ### if unsub from all
    if (tag == "#ALL"):     
        userSubs[user] = []
    ### removes sub
    userSubs[user].remove(tag)

### helper to handle subscriptions to a given hashtag
def subscribeToTag(user, tag):
    if (tag not in userSubs[user]): #add tag to user key
        userSubs[user].append(tag)
        userToPort[user].sendall(("good").encode())

#######################################
# helper to validate port selection   #
#######################################
def validPort(args): 
    try: 
        port = int(args[1])
        if port >= 1024 and port <= 65535: 
            return port
    except: 
        sys.exit()

###########################################
# helper to get a socket to interact with #
###########################################
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



