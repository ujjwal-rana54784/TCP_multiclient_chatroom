# TCP_multiclient_chatroom
This is a python script for creating a simple TCP Multiclient chat room in python using Socket Programming and Multithreading.

To Run the script as a TCP server run

`python TcpChatroom.py server [server_ip] [server_port]` 

[ ] feilds are optional , you can specify them if you wish, or they would choose defualt address from your machine and defualt port of 5000.

Then you can connect client machines to this server using command

`python Tcpchatroom.py client server_ip server_port [client_ip]`

client port would be chosen randomly between 5000 to 10000.

NOTE:
* I have use Multithreading to handel diffrent clients.
* To handel the blocking calls, i have used a force shut down mechnism i.e when main_thread closes, the terminal does not wait for rest of threads to close and process ends
* All the exception and errors have been handeled in code itself and you can quit the program by typing "quit" or pressing CTRL+C
* The server should be deployed on public machines if users are all over internet or on a local machine if users are in a LAN environment.
* *This script does not take care of NAT traversal issue and if you intend to run server machine behind NAT, it may not work.*
