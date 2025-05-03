import socket
import threading
import pickle
import struct

class Server:
    def __init__(self):
        self.host = "localhost"
        self.port = 5555
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen()
        
        self.clients = []
        self.players = {}
        self.nicknames = {}
        self.lock = threading.Lock()
        self.next_player_id = 1
        
        print(f"Server started on {self.host}:{self.port}")

    def _receive_data(self, client):
        try:
            raw_msglen = self._recvall(client, 4)
            if not raw_msglen:
                return None
            msglen = struct.unpack('>I', raw_msglen)[0]
            return pickle.loads(self._recvall(client, msglen))
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None

    def _recvall(self, sock, n):
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def _send_data(self, client, data):
        try:
            data = pickle.dumps(data)
            msg = struct.pack('>I', len(data)) + data
            client.sendall(msg)
            return True
        except Exception as e:
            print(f"Error sending data: {e}")
            return False

    def broadcast(self, data):
        with self.lock:
            disconnected_clients = []
            for client in self.clients:
                if not self._send_data(client, data):
                    disconnected_clients.append(client)
            
            for client in disconnected_clients:
                self._remove_client(client)

    def _remove_client(self, client):
        with self.lock:
            if client in self.clients:
                index = self.clients.index(client)
                player_id = index + 1  # Player IDs start at 1
                
                self.clients.remove(client)
                client.close()
                
                if player_id in self.players:
                    del self.players[player_id]
                if player_id in self.nicknames:
                    del self.nicknames[player_id]
                
                self.broadcast({
                    "type": "disconnect",
                    "player_id": player_id
                })

    def handle_client(self, client, address):
        with self.lock:
            player_id = self.next_player_id
            self.next_player_id += 1
            self.clients.append(client)

        print(f"Player {player_id} connected from {address}")

        try:
            while True:
                data = self._receive_data(client)
                if not data:
                    print(f"Player {player_id} disconnected (No data received)")
                    break

                if data["type"] == "connect":
                    with self.lock:
                        self.players[player_id] = {
                            "x": 100,
                            "y": 100,
                            "color": (0, 255, 0)  # Server assigns color
                        }
                        self.nicknames[player_id] = data["nickname"]

                    self._send_data(client, {
                        "type": "welcome",
                        "player_id": player_id,
                        "players": self.players.copy(),
                        "nicknames": self.nicknames.copy()
                    })

                    self.broadcast({
                        "type": "players",
                        "players": self.players.copy(),
                        "nicknames": self.nicknames.copy()
                    })

                elif data["type"] == "move":
                    with self.lock:
                        if player_id in self.players:
                            self.players[player_id]["x"] = data["x"]
                            self.players[player_id]["y"] = data["y"]
                    
                    self.broadcast({
                        "type": "move",
                        "player_id": player_id,
                        "x": data["x"],
                        "y": data["y"]
                    })

                elif data["type"] == "message":
                    self.broadcast({
                        "type": "message",
                        "player_id": player_id,
                        "text": data["text"],
                        "nickname": self.nicknames.get(player_id, "Unknown")
                    })

        except Exception as e:
            print(f"Error with player {player_id}: {e}")
        finally:
            self._remove_client(client)
            print(f"Player {player_id} disconnected")

    def run(self):
        try:
            while True:
                client, address = self.server.accept()
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client, address)
                )
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("Shutting down server...")
        finally:
            self.server.close()

if __name__ == "__main__":
    server = Server()
    server.run()
