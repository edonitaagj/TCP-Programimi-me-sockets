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

print(f"Serveri po pret lidhje ne {PORT}...")