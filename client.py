import socket
import sys
import time

if len(sys.argv) < 3:
    print("Perdorimi: python client.py <SERVER_IP> <PORT>")
    sys.exit()

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

MY_ID = None
MY_ROLE = None

def connect_to_server():
    while True:
        try:
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.connect((SERVER_IP, SERVER_PORT))
            return c
        except:
            print("Serveri i fikur, provoj perseri ne 2 sekonda...")
            time.sleep(2)

client = connect_to_server()
