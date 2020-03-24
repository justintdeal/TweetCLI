from socket import * 
import sys
import re

def main():
    host, port, user = validateArgs(sys.argv)
    print(sys.argv)
    csock = connect(host, port, user)
    while True:
        input("Options: tweet, subscribe, unsubscribe, timeline, users, tweets, exit")

def tweet():


# def subscribe(): 

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

def validateArgs(args):
    regexIP = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''
    regexUser = "^[a-zA-Z0-9_]*$"

    if len(args) != 4: 
        print('error: args should contain <ServerIP> <Server Port> <Username>')
        sys.exit()
    host, port, user = args[1], args[2], args[3]
    if port < 1024 or port > 65535: 
        print('error: server port invalid, connection refused')
        sys.exit()
    if not re.serach(regexIP, host):
       print('error: server ip invalid, connection refused') 
       sys.exit()
    if not re.search(regexUser, user):
        print('error: username has wrong format, connection refused')
        
    return host, port, user
    
main()