import socket
import select
import os
import time
import json

HOST = "0.0.0.0"
PORT = 5000
MAX_CLIENTS = 4
TIMEOUT = 300

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f"Serveri duke punuar ne {HOST}:{PORT}")
print(f"IP lokale (përdore për klient): {local_ip}")

clients = []
roles = {} 
client_ids = {} 
sessions = {}
last_active = {}

monitoring_data = {"message_count": 0, "all_messages": []}

def save_stats():
    stats = {
        "active_count": len(clients),
        "total_messages": monitoring_data["message_count"],
        "connected_clients": [
            {"id": client_ids[s], "role": roles[s], "ip": s.getpeername()[0]} 
            for s in clients if s in client_ids
        ],
        "logs": monitoring_data["all_messages"][-15:]
    }
    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=4)

def disconnect(sock):
    if sock in clients: clients.remove(sock)
    if sock in roles: del roles[sock]
    if sock in client_ids: del client_ids[sock]
    if sock in last_active: del last_active[sock]
    sock.close()
    save_stats()

print(f"TCP Server running on {HOST}:{PORT}...")

while True:
    read_sockets, _, _ = select.select([server] + clients, [], [], 1)

# per te mos lejuar qasjen e me shume se 4 klienteve
    for sock in read_sockets:
        if sock == server: 
            c, addr = server.accept()
            print(f"Tentim lidhjeje nga {addr}")
            if len(clients) >= MAX_CLIENTS:
                c.send("GABIM: Serveri plot.".encode())
                c.close()
            else:
                clients.append(c)
                last_active[c] = time.time()
                c.send("AUTH_REQUIRED".encode())
        else:
            try:
                data = sock.recv(4096).decode().strip()
                if not data:
                    disconnect(sock)
                    continue

                last_active[sock] = time.time()
        # E domosdoshme te caktohet nje rol user ose admin
                if sock not in client_ids:
                    if ":" not in data:
                        sock.send("GABIM: Formati ID:ROLI".encode())
                        continue 
                    cid, rrole = data.split(":", 1)
                    rrole = rrole.lower()

                    if rrole not in ["admin", "user"] or not cid:
                        sock.send("GABIM: Duhet te jepni ID dhe rolin rreptesisht (admin/user):".encode())
                        continue
                    if rrole == "admin":
                        other_admin_exists = any(r == "admin" for s, r in roles.items() if client_ids.get(s) != cid)
               # ndalon krijimin e me shume se 1 admini per session         
                        if other_admin_exists:
                            sock.send("GABIM: Admini ekziston. Zgjidh rolin 'user' per te vazhduar:".encode())
                            continue 
                    if cid in sessions: # rikuperimi automatik pasi shkeputet lidhja pas kalimit te timeout
                        print(f"RIKUPERIM: {cid} u rikthye.")
                        for s, name in list(client_ids.items()):
                            if name == cid:
                                if s in clients: clients.remove(s)
                                s.close()
                                del client_ids[s]
                                if s in roles: del roles[s]
                    sessions[cid] = rrole
                    client_ids[sock] = cid
                    roles[sock] = rrole
                    sock.send(f"AUTH_OK: Miresevini {cid}".encode()) # kur kryhet autentikimi vazhdojme me komandat e tjera
                    save_stats()
                    continue

                monitoring_data["message_count"] += 1
                monitoring_data["all_messages"].append(f"{client_ids[sock]}: {data}")
                save_stats()

                if roles[sock] != "admin": time.sleep(1.5)

                cmd_parts = data.split(" ", 2)
                cmd = cmd_parts[0].lower()
                os.makedirs("server_files", exist_ok=True)

                if cmd == "/list" and roles[sock] == "admin":
                    sock.send(str(os.listdir("server_files")).encode())

                elif cmd == "/read" or cmd == "/download":
                    if len(cmd_parts) < 2: sock.send("GABIM".encode())
                    else:
                        path = f"server_files/{cmd_parts[1]}"
                        if os.path.exists(path):
                            with open(path, "r") as f: sock.send(f.read().encode())
                        else: sock.send("Nuk ekziston".encode())

                elif cmd == "/upload" and roles[sock] == "admin":
                    if len(cmd_parts) < 3: sock.send("GABIM".encode())
                    else:
                        with open(f"server_files/{cmd_parts[1]}", "w") as f: f.write(cmd_parts[2])
                        sock.send("OK UPLOAD".encode())

            except Exception as e: # kodi vazhdon kjo pjese eshte e perkohshme 
                print(f"Gabim: {e}")
                disconnect(sock) # deri ketu 
