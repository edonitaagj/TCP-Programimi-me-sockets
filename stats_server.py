import socket
import os

HOST = "0.0.0.0"
PORT = 8080

http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
http.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
http.bind((HOST, PORT))
http.listen(5)

print(f"Monitorimi lokal: http://localhost:{PORT}/stats")

while True:
    c, addr = http.accept()
    try:
        req = c.recv(1024).decode()

        if "GET /stats" in req:
            data = open("stats.json").read() if os.path.exists("stats.json") else "{}"

            resp = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                f"Content-Length: {len(data)}\r\n"
                "\r\n" +
                data
            )

            c.sendall(resp.encode())
    except:
        pass

    c.close()
