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

while True:
    try:
        client.settimeout(1.0)
        try:
            data = client.recv(1024).decode()
        except socket.timeout:
            data = None

        if data == "AUTH_REQUIRED":
            if MY_ID is None:
                MY_ID = input("ID juaj: ")
                MY_ROLE = input("Roli (admin/user): ").lower()
            
            client.send(f"{MY_ID}:{MY_ROLE}".encode())
            client.settimeout(None)
            status = client.recv(1024).decode()
            print("SERVER:", status)
            if "GABIM" in status:
                MY_ID = None; MY_ROLE = None 
                client.close(); client = connect_to_server()
                continue
        elif data:
            print("SERVER:", data)

        client.settimeout(None)
        msg = input(f"\n{MY_ID}@{MY_ROLE} >> ")
        if not msg: continue
        
        client.send(msg.encode())
        res = client.recv(4096).decode()
        
        if msg.startswith("/download") and "GABIM" not in res and "Nuk" not in res:
            fname = "shkarkuar_" + msg.split()[1]
            with open(fname, "w") as f: f.write(res)
            print(f"SISTEMI: File u ruajt si {fname}")
        else:
            print("PERGJIGJA:", res)

    except (EOFError, KeyboardInterrupt):
        sys.exit()
    except:
        print("\n[!] Lidhja u shkeput. Rilidhja automatike...")
        client.close()
        client = connect_to_server()
