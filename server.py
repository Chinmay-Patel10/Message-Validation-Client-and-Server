import sys
import socket
import hashlib
#import time
#import re

listen_port = int(sys.argv[1])
key_file = sys.argv[2]


#key_file_arr = []
with open(key_file, "r") as keyfile:
    key = list(map(lambda x: x.strip(), keyfile.readlines()))
    keyfile.close()


def main():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', listen_port))
    server_socket.listen(5)

     
    client_socket, addr = server_socket.accept()
    #print("Connected from:", addr)
    hello_rec = client_socket.recv(1024).decode('ASCII').strip() #Decode uses UTF-8 to convert bytes into strings
    print(hello_rec)
    if hello_rec != "HELLO":
        print("Error: Unexpected message from client. Did not recieve HELLO")
        client_socket.close()
        server_socket.close()
        exit()
    client_socket.send("260 OK\n".encode("ASCII")) #Sending 260 OK to the client
        
    key_number = 0    
    while True:
        
        #for key in key_file_arr:
                
            command = client_socket.recv(5).decode('ASCII').strip()
            print(command)
            
            if command == "DATA":
                #sha256 = hashlib.sha256() # Created sha256 hash object
                #time.sleep(1)
                message = client_socket.recv(1024) #Decodes message from bytes to string
                message_original = message.decode('ASCII').replace('\.', '.').replace('\r\n.', '').replace("\n.", "").strip()
                #print(message_original)
                #dot = client_socket.recv(1024).decode()
                #print('.')
                #message = process_message(message) #escaped the message
                #print(message)
                
                client_socket.send("270 SIG\n".encode("ASCII"))
                #print(key)
                
                #HASHING
                sha256 = hashlib.sha256()
                sha256.update(message_original.encode('ASCII')) #updating the hash/ Adding the line to the SHA 256 Hash
                sha256.update(key[key_number].encode('ASCII'))
                signature_hash = sha256.hexdigest() #hashing the message + key/ Finished hash                    
                client_socket.send(signature_hash.encode('ASCII') + "\n".encode('ASCII'))
                
                #RECIEVING PASS OR FAIL CALL
                response = client_socket.recv(5).decode('ASCII').strip()
                if response == 'PASS':
                    print(response)
                    client_socket.send("260 OK\n".encode('ASCII'))
                    #key_counter += 1
                elif response == 'FAIL':
                    print(response)
                    client_socket.send("260 OK\n".encode('ASCII'))
                    #key_counter += 1
                elif response not in ["PASS", "FAIL"]:
                    print("Error: Option is not PASS or FAIL.")
                    #client_socket.close()
                    #return
                key_number += 1
                
            elif command == "QUIT":
                #print(command)
                #print("Client requested to QUIT. Closing the connection.")
                client_socket.close()
                exit()
            else:
                print("Error: command is neither DATA or QUIT.")
                client_socket.close()
                exit()
            

if __name__ == "__main__":
    main()