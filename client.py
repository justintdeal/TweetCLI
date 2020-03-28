from socket import * 
import sys
import re
import _thread as thread

def main():
    host, port, user = validateArgs(sys.argv)
    print(sys.argv)
    csock = connect(host, port, user)
    while True:
        thread.start_new_thread(listening, (csock,))
        raw = input("Options: tweet, subscribe, unsubscribe, timeline, users, tweets, exit\n").split()
        print(raw)
        if (len(raw) == 2 and raw[0] == "subscribe" and validateTag(raw[1])):
            subscribe(user, raw[1], csock)
        if (len(raw) == 3 and raw[0] == "tweet"): 
            valid = True
            if (len(raw[1]) <= 2): 
                valid = False
                print("message format illegal.")
            if (len(raw[1]) >= 150):
                valid = False 
                print("message length illegal, connection refused.")
            if (valid):
                tweet((raw[1] +" "+ raw[2]), csock)

def tweet(message, conn):
    code = "tweet " + str(message)
    conn.sendall(code.encode())

def subscribe(user, tag, conn): 
    code = "sub " + str(user) + " " + str(tag)
    conn.sendall(code.encode())

# def unsubscribe():

# def timeline():

# def getUsers():

# def getTweets():

def connect(host, port, user): 
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((host, port))
    except:
        print("error: server ip invalid, connection refused.")
        sock = None
        sys.exit()
    sock.sendall(user.encode())
    loggedIn = sock.recv(1024).decode()
    if loggedIn == 'True': 
        print('username legal, connection established')
        return sock
    else: 
        print('username illegal, connection refused')
        sys.exit()

def listening(conn):
    while True:
        data = conn.recv(1024).decode().split()
        if data[0] == "rep":
            print(str(data[1]) + " " + str(data[2]) + " " +str(data[3]))
        if data [0] == "good":
            print("operation success")

def validateArgs(args):
    regexIP = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''
    regexUser = "^[a-zA-Z0-9_]*$"

    if len(args) != 4: 
        print('error: args should contain <ServerIP> <Server Port> <Username>')
        sys.exit()
    host, port, user = args[1], int(args[2]), args[3]
    if port < 1024 or port > 65535: 
        print('error: server port invalid, connection refused')
        sys.exit()
    if not re.search(regexIP, host):
       print('error: server ip invalid, connection refused') 
       sys.exit()
    if not re.search(regexUser, user):
        print('error: username has wrong format, connection refused')
        
    return host, port, user

def validateTag(tag):
    valid = True
    for index in range(len(tag)-1):
        if tag[index] == tag[index+1]:
            if tag[index] == "#":
                valid = False
                print('hashtag illegal format, connection refused.')
    return valid


            


    

    
main()