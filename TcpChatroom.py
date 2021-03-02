import socket
import time
import datetime
import threading
import sys
import random
import queue
text = """
    This is a sever and client program file together
    => help : to get help
    => server [server_ip] [server_port] these  2 arguments are to be given 
            after giving server. The argument with [] are optional and with <> are mandatory. if not given
            defualt value is chosen which is 5000 port and local ip given by computer

    => client <server_ip> <server_port> [client_ip] for running as client you need to 
            specify ip and port of server mandatory and  optionaly you can give
            ip of client program itself that you are running. port for this is chosen
             randomly between 5000 to 10000.

    ------------------------------------------
    => To close a connection with the server you can do CTRL +  C or type "quit"
    using quit is preffered
    
     
    """






clients = []
names = dict()
flag = False
relay_messages = queue.Queue()

def relay_messanger():
    while 1:
        while (not relay_messages.empty()):
            msg = relay_messages.get()
            for x in clients:
                try:
                    x[0].sendall(msg.encode('Utf-8'))
                except:
                    pass
                
                


def handel_connection(ser):
    while not flag:
        try:
            conn,addr = ser.accept()
            print(f"connected to {addr}")
            print(f"{len(clients)+ 1} Active conenctions")
            relay_messages.put(f"{ len(clients) +1 } online users ")
            clients.append( (conn,addr) )
            threading.Thread(target=handel_client,args=(conn,addr)).start()
        except:
            print("bye bye")
            ser.close()
            sys.exit(1)
            break
            


def handel_client(client,addr):
    while not flag:
        # clients[0][0].sendall(b"Hello dude")
        try:
            data = client.recv(1024)
            
            
            if ( data.decode('Utf-8')=="quit" ):
                print(f" {addr} : {name} left the room!")
                relay_messages.put(name + " Left the room!")
                client.close()
                clients.remove((client,addr))
                break

            elif(data.decode().split()[0] == "name"):
                name = data.decode().split()[1]
                names[addr] = name
                print(name," Joined the room!")
                relay_messages.put(name+" Joined the room!")
                continue
            print(name ," : ",data.decode('Utf-8'))
            if(data):
                relay_messages.put("\n\r"+name +" > " +str(data.decode('Utf-8')))


        except(KeyboardInterrupt):
            print("Going offline")
            client.close()
            ser.close()
            sys.exit(0)
        # except :
        #     print(f" {addr}  left the room!")
        #     client.close()
        #     clients.remove((client,addr))
        #     print("Without even telling us his name")
        #     break

            
def handel_response(c):
    while not flag:
        try:
            if(flag):
                print("sorry flag is on")
                break
            data,addr = c.recvfrom(1024)
            if(data):
                print(data.decode('Utf-8'))
    
        except:
           break

def server(servip = socket.gethostbyname(socket.gethostname()),servport=5000):
    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ser.bind((servip,servport))    
    ser.listen(10)
    print(f"server is up and running on {(servip,servport)}")
    t =threading.Thread(target=handel_connection,args=(ser,))
    t.setDaemon(1)
    t.start()
    t3 = threading.Thread(target=relay_messanger)
    t3.setDaemon(1)
    t3.start()
    while 1:
        try:
            x = input(">> ")

            if(x=="quit"):
                print("ohkay going down")
                ser.close()
                sys.exit()
                flag = True
                break
            else:
                for y in clients:
                    y[0].sendall( ( "Server :"+x ).encode('Utf-8'))
                    
        except(KeyboardInterrupt):
            print("Khatam tata bye bye gaya1")
            ser.close()
            sys.exit()
    
    
def client(server_addr, server_port =5000, client_IP = socket.gethostbyname(socket.gethostname())):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket = (server_addr,server_port)
    client_port = int(random.randint(5000,10000))
    client.bind((client_IP,client_port))
    client.connect(server_socket)
    t1 = threading.Thread(target=handel_response,args=(client,))
    t1.setDaemon(1)
    try:
        name = input("Enter you name ")
    except:
        print("here here")
        client.send("quit".encode('Utf-8'))     
        client.close()
        sys.exit()
    name = "name    "+ name
    client.send(name.encode('Utf-8'))

    t1.start()
    while 1:
        try:
            # msg = input("Enter your Query [SEND_TIME or  SEND_DATE]")
            msg = input()
            client.send(msg.encode('Utf-8'))

            if(msg=="quit"):
                
                print("shutting down..")
                client.send("quit".encode('Utf-8'))
                flag = True
                client.close()
                sys.exit(0)
                
        except KeyboardInterrupt:
                client.send("quit".encode('Utf-8'))
                client.close()
                flag = True
                print("shutting down..")
                sys.exit(0)



if sys.argv[1] == "help":
    
    print(text)
if sys.argv[1] == "client":
    if(len(sys.argv)==5):
        client(sys.argv[2],int(sys.argv[3]),sys.argv[4])
    elif(len(sys.argv)==4):
        client(sys.argv[2],int(sys.argv[3]))
    elif(len(sys.argv)==3):
        client(sys.argv[2])
    else:
        print("not enough arguments  please sepecify server adress [por] [client adress]")
elif sys.argv[1] == "server":
    if(len(sys.argv)==4):
        server( sys.argv[2],int(sys.argv[3]) )
    elif(len(sys.argv)==3):
        server(sys.argv[2])
    else:
        server()