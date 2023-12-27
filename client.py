import socket
import sys

server_name = sys.argv[1] #'localhost'
server_port = int(sys.argv[2]) #1234
message_filename = sys.argv[3]
signature_filename = sys.argv[4]
   
messages = []
with open(message_filename, 'r') as message_file:
    while True:
        line = message_file.readline()
        if not line:
            break
        else:
            linenum = int(line)
        msg = message_file.readline(linenum).strip()
        if not msg:
            break
        messages.append(msg)
    message_file.close()
        

#signaturearr = []
with open(signature_filename, 'r') as signature_file:
        signature = list(map(lambda x: x.strip(), signature_file.readlines()))
        signature_file.close()


def main():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    
    client_socket.send("HELLO\n".encode('ASCII'))
    response_260OK = client_socket.recv(1024).decode('ASCII').strip()
    print(response_260OK)
    if response_260OK != "260 OK":
        print("Error: Unexpected response from server. Did not recieve 260 OK")
        client_socket.close()
        exit()

    message_counter = 0
    for message in messages:
        
        escaped_message = message.replace("\\", "\\\\").replace(".", "\.") + "\n.\n"
        client_socket.send("DATA\n".encode('ASCII')) #Sends DATA message before printing out message every line
        client_socket.send(escaped_message.encode('ASCII')) #Converts the byte of the message back into a String and sends to server
        #client_socket.sendall(b'.')
        
        response_270SIG = client_socket.recv(8).decode('ASCII').strip()
        print(response_270SIG)
        if response_270SIG != "270 SIG":
            print("Error: Unexpected response from server. Recieved", response_270SIG)
            client_socket.close()
            exit()
    
        signature_hash = client_socket.recv(1024).decode('ASCII').strip()
        print(signature_hash)
        #print(signaturearr[message_counter])
        if signature_hash == signature[message_counter]:    #.strip().encode('ASCII'):
            client_socket.send("PASS\n".encode('ASCII'))
            message_counter += 1
        else:
            client_socket.send("FAIL\n".encode('ASCII'))
            message_counter += 1

        response = client_socket.recv(7).decode('ASCII').strip()
        print(response)
        if response != "260 OK":
            print("Error: Response is not 260 OK")
            client_socket.close()
            exit()

    client_socket.send(bytes("QUIT\n", 'ASCII'))

    #print("Closing the TCP socket.")
    client_socket.close()
    exit()

if __name__ == "__main__":
    main()
    