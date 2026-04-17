import socket
import select
import os
import time
import json

HOST = "127.0.0.1"
PORT = 5000
MAX_CLIENTS = 4
TIMEOUT = 60 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(MAX_CLIENTS)

monitoring_data = {"active_connections": 0, "message_count": 0, "all_messages": []}
clients = []
roles = {} 
client_ids = {} 
last_active = {} 

def save_stats():
    stats = {
        "active_count": len(clients),
        "total_messages": monitoring_data["message_count"],
        "connected_clients": [{"id": client_ids[s], "role": roles[s], "ip": s.getpeername()[0]} for s in clients if s in client_ids],
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

    for sock in read_sockets:
        if sock == server:
            c, addr = server.accept()
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

                if sock not in client_ids:
                    parts = data.split(":") 
                    cid, rrole = parts[0], parts[1].lower()
                    
                    if cid in client_ids.values():
                        sock.send("GABIM: Emri ekziston.".encode())
                        disconnect(sock)
                        continue
                    if rrole == "admin" and "admin" in roles.values():
                        sock.send("GABIM: Ka nje Admin.".encode())
                        disconnect(sock)
                        continue

                    client_ids[sock], roles[sock] = cid, rrole
                    save_stats()
                    sock.send(f"AUTH_OK: Miresevini {cid}".encode())
                    continue

            except Exception as e: # kodi vazhdon kjo pjese eshte e perkohshme 
                print(f"Gabim: {e}")
                disconnect(sock) # deri ketu 