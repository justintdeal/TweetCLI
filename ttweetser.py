from socket import * 
import sys
import _thread as thread
import pickle
import time

activeUsers = [] #list of all active users
userToPort = dict() #dict of key: users, value: their port number 
userSubs = dict() #dict of key: user, value: their hashtag subscriptions
userTweets = dict() #dict of key: user, value: their tweets


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
        # print("Recieved data: " + str(data))
        preformAction(data, conn, user)

#####################################
#   Handles Requests from Clients   #
#####################################
def preformAction(data, conn, user):
    print("data: " + str(data))
    request = data[0]
    ### Handles subscibe functionality
    if (request == "sub"): 
        user = data[1]
        tags = data[2].split('#')[1:]
        print("tags: " + str(tags))
        for tag in tags: 
            subscribeToTag(user, "#" + tag) 

    ### Handles tweet functionality
    if (data[0] == "tweet"):
        print("data dealing with 1: " + str(data))
        if (data[1] == '"' and data[2] == '"'): #for if empty message
            data.pop(1) #gets rid of '"'
            data.pop(1) #gets rid of '"'
            data.insert(1, '" "')
            # print("special space: " + str(data))

        # print("data dealing with 2: " + str(data))
        # print("data[1][0]: " + str(data[1][0]))
        # print("data[1][len(data[1])-1]: " + str(data[1][len(data[1])-1]))
        if (data[1][0] == '"' and data[1][len(data[1])-1] != '"'):
            # print("hey")
            index = 1
            stop = True
            newString = ""
            while index < len(data) and stop:
                # print("hey2")
                # print("data[index][len(data[index])-1]: " + str(data[index][len(data[index])-1]))
                newString += data[index]
                # print("newString: " + str(newString))
                if (data[index][len(data[index])-1] == '"'):
                    stop = False  
                if stop: 
                    newString += " " 
                index = index + 1    
            # print("index: " + str(index))
            
            count = 0
            # print("pre pop data: " + str(data))
            while count < index - 1:
                # print("hey3")
                data.pop(1)
                # print("popped data: " + str(data))
                count = count + 1
            data.insert(1, str(newString))
            # print("post insert data: " + str(data))
        
        #this data coming from what was passed from client
        user = data[3]
        message = data[1]
        print(message)
        tags = data[2].split("#")[1:]
        for tag in tags: 
            tag = "#" + tag
        print("tags: " + str(tags))
        userTweets[user].append(message + " " + str(data[2])) # add tweet to user tweet history 

        for use in activeUsers:          # loop through all active users and broadcast tweets
            for sub in userSubs[use]: #loop through the dicts key: hashtag, value: frequency
                for tag in tags: #going three all hashtags in tweet
                    if ("#" + tag) in sub.keys(): #check if tag is in set of subscriptions
                        userToPort[use].sendall(("rep " + str(user)+" "+ str(message)+ " " + str(data[2]) + " " + str(sub["#" + tag])).encode())
                        # time.sleep(.1)
                if "#ALL" in sub.keys():
                    userToPort[use].sendall(("rep " + str(user)+" "+ str(message)+ " " + str(data[2]) + " " + str(1)).encode())
                    # time.sleep(.1)
   
    ### Handles unsubscribing from a hashtag
    if (data[0] == "unsub"):
        user = data[1]
        tag = data[2]
        unsubFromTag(user, tag)
    ### Handles the get user features
    if data[0] == "users":
        toSend = ""
        for person in activeUsers:
            toSend += str(person)
            toSend += " "

        userToPort[user].sendall(("incoming " + toSend).encode())

    ### Handles getTweets, sends client all of it's previous tweets
    if data[0] == "getTweets":
        user = data[1]
        requestedUser = data[2]
        if requestedUser not in activeUsers:
            # userToPort[user].sendall(("notIn").encode()) 
            index = 0
        else:
            toSend = ""
            for twit in userTweets[requestedUser]:
                toSend += str(requestedUser + ": " + twit)
                userToPort[user].sendall(("tweets " + toSend).encode()) 
                # time.sleep(.25)   
                toSend = ""
    if data[0] == "exit":
        user = data[1]
        activeUsers.remove(user)
        del userSubs[user]
        del userTweets[user]
        userToPort[user].sendall(("ended ".encode()))
        del userToPort[user]
        conn.close()
        thread.exit()
    
#########################################
# Helpers for Subscirbe and Unsubscribe #
#########################################
def unsubFromTag(user, tag):
    ### if unsub from all
    if (tag == "#ALL"):     
        userSubs[user] = []
    ### removes sub
    else: 
        print("userSubs[user]: " + str(userSubs[user]))
        for subs in userSubs[user]:
            print("subs: " + str(subs))
            if tag in subs.keys():
                del subs[tag]
        print("userSubs[user]: " + str(userSubs[user]))
        userToPort[user].sendall(("good").encode())

### helper to handle subscriptions to a given hashtag
def subscribeToTag(user, tag):
    hashUsers[tag] = []
    if (len(tag) > 1):
        if (len(userSubs[user]) < 3): #add tag to user key
            added = False
            hashUsers[tag].append(user)
            print("hashUser: " + str(hashUsers[tag]))
            for subs in userSubs[user]:
                if tag in subs.keys():
                    # subs[tag] += 1
                    userToPort[user].sendall(("good").encode())
                    added = True
            
            if not added:
                userSubs[user].append({tag : 1})
                userToPort[user].sendall(("good").encode())
        else:
            userToPort[user].sendall(("tooMany").encode())           

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



