import socket
import requests

HOST = ''
PORT = 8080
# PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(5)
print("Listening on", PORT)
while 1:
    conn, addr = s.accept()
    print("Connected to", addr[0], "at port", addr[1])
    data = conn.recv(4096).decode('utf-8')
    start = data.find("/")
    end = data.find(" ", 4)
    data = data[start+1:end]

    req = "http://api.openweathermap.org/data/2.5/weather?q="+data+"&appid=2da7014106d832589ce4fba62e798557"
    try:
        response = requests.get(req)
        data = response.json()
        conn.sendall(str(data['main']).encode())
        weather = data['weather'][0]['main']
        description = data['weather'][0]['description']
        conn.sendall(str("\n"+weather+"\n"+description).encode())
        print("Data Sent!")
    except Exception as e:
        print(e)
        conn.sendall("City not found".encode())

    conn.close()
s.close()

