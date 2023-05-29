import socket
import threading


class ChatRoom:
    def __init__(self, host, sendPort, recvPort):
        self.host = host
        self.sendPort = sendPort
        self.recvPort = recvPort

        self.RecvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientsRecv = []
        self.clientsSend = []

    def start(self):
        self.RecvSocket.bind((self.host, self.recvPort))
        self.SendSocket.bind((self.host, self.sendPort))

        self.RecvSocket.listen()
        self.SendSocket.listen()

        print(f"Chat room started on {self.host}:{self.recvPort}")

        while True:
            client_recv_socket, client_address = self.RecvSocket.accept()
            client_send_socket, client_address = self.SendSocket.accept()

            print(f"New connection from {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_recv_socket, client_send_socket,))
            client_thread.start()

    def handle_client(self, client_recv_socket, client_send_socket):

        self.clientsRecv.append(client_recv_socket)
        self.clientsSend.append(client_send_socket)

        self.broadcast(f"New client joined the chat. Total clients: {len(self.clientsSend)}")

        message = client_recv_socket.recv(1024).decode("utf-8")
        self.broadcast(message)

        while True:
            try:
                message = client_recv_socket.recv(1024).decode("utf-8")
                if message:
                    self.broadcast(message)

            except ConnectionResetError:

                self.clientsRecv.remove(client_recv_socket)
                self.clientsSend.remove(client_send_socket)

                self.broadcast(f"A client left the chat. Total clients: {len(self.clientsSend)}")
                break

    def broadcast(self, message):
        for send_socket in self.clientsSend:
            try:
                send_socket.sendall(message.encode("utf-8"))
            except ConnectionResetError:
                self.clientsSend.remove(send_socket)


if __name__ == "__main__":
    
    host = "0.0.0.0"
    sendPort = 5001
    recvPort = 5002

    chat_room = ChatRoom(host, sendPort, recvPort)
    chat_room.start()
