import socket
import threading
import time

MY_ID = "3"
BROADCAST_IP = "192.168.1.255"
PORT = 12345
MESSAGE = "Hello from " + MY_ID


def listen_hello():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
      sock.bind(('', PORT))
      print("Listening on", PORT)
      while True:
          data, addr = sock.recvfrom(1024)
          print(f"Received msg from {addr}: {data.decode('utf-8')}")

def send_hello():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            sock.sendto(MESSAGE.encode('utf-8'), (BROADCAST_IP, PORT))
            print("Sent broadcast")
            time.sleep(10)

if __name__ == "__main__":
    listen_thread = threading.Thread(target=listen_hello, daemon=True)
    listen_thread.start()
    send_hello()
