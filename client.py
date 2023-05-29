import socket
import threading


class ChatClient:
    def __init__(self, host, sendPort, recvPort):
        self.host = host

        self.recvPort = recvPort
        self.sendPort = sendPort

        self.RecvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.username = ""

    def connect(self):

        self.RecvSocket.connect((self.host, self.sendPort))
        self.SendSocket.connect((self.host, self.sendPort))

        print(f"Connected to chat room at {self.host}:{self.sendPort}")
        print(f"Connected to chat room at {self.host}:{self.recvPort}")

        self.username = input("Enter your username: ")
        self.SendSocket.sendall(f"{self.username} joined the chat.".encode("utf-8"))

        threading.Thread(target=self.receive_messages).start()

        while True:
            message = input()
            packet = self.username + ": " + message
            self.SendSocket.sendall(packet.encode("utf-8"))

    def receive_messages(self):

        message = self.RecvSocket.recv(1024).decode("utf-8")
        print(message)

        while True:
            try:
                message = self.RecvSocket.recv(1024).decode("utf-8")
                print(message)

                if message == "exit":
                    print("Connection to the chat room was closed.")
                    break

            except ConnectionResetError:
                print("Connection to the chat room was closed.")
                break


if __name__ == "__main__":

    host = "0.0.0.0"
    sendPort = 5001
    recvPort = 5002

    chat_client = ChatClient(host, sendPort, recvPort)
    chat_client.connect()
