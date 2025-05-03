import pygame
import socket
import pickle
import threading
import random
import struct

# Game constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
FPS = 60

class Client:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Multiplayer Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        
        self.host = "localhost"
        self.port = 5555
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.player_id = random.randint(1000, 9999)
        self.nickname = f"Player{random.randint(1, 100)}"
        self.x, self.y = 100, 100
        self.players = {}
        self.nicknames = {}
        self.messages = []
        self.connected = False
        
        try:
            self.client.connect((self.host, self.port))
            self._send_data({"type": "connect", "player_id": self.player_id, "nickname": self.nickname})
            self.connected = True
            
            receive_thread = threading.Thread(target=self.receive_data, daemon=True)
            receive_thread.start()
            
        except Exception as e:
            print(f"Error connecting to server: {e}")
            self.messages.append("Failed to connect to server")
    
    def _send_data(self, data):
        try:
            data = pickle.dumps(data)
            # Prefix each message with a 4-byte length (network byte order)
            msg = struct.pack('>I', len(data)) + data
            self.client.sendall(msg)
        except Exception as e:
            print(f"Error sending data: {e}")
    
    def _receive_data(self):
        try:
            # First get the size of the data
            raw_msglen = self._recvall(4)
            if not raw_msglen:
                return None
            msglen = struct.unpack('>I', raw_msglen)[0]
            # Then get the data itself
            return pickle.loads(self._recvall(msglen))
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None
    
    def _recvall(self, n):
        data = bytearray()
        while len(data) < n:
            packet = self.client.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
    
    def receive_data(self):
        while self.connected:
            data = self._receive_data()
            if not data:
                self.connected = False
                self.messages.append("Disconnected from server")
                break
                
            if data["type"] == "players":
                self.players = data["players"]
                self.nicknames = data["nicknames"]
            
            elif data["type"] == "move":
                self.players[data["player_id"]] = {"x": data["x"], "y": data["y"]}
            
            elif data["type"] == "message":
                self.messages.append(f"{self.nicknames.get(data['player_id'], 'Unknown')}: {data['text']}")
                if len(self.messages) > 5:
                    self.messages.pop(0)
            
            elif data["type"] == "disconnect":
                if data["player_id"] in self.players:
                    del self.players[data["player_id"]]
                if data["player_id"] in self.nicknames:
                    del self.nicknames[data["player_id"]]
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        speed = 5
        moved = False
        
        if keys[pygame.K_LEFT]:
            self.x -= speed
            moved = True
        if keys[pygame.K_RIGHT]:
            self.x += speed
            moved = True
        if keys[pygame.K_UP]:
            self.y -= speed
            moved = True
        if keys[pygame.K_DOWN]:
            self.y += speed
            moved = True
            
        # Keep player on screen
        self.x = max(0, min(WIDTH - PLAYER_SIZE, self.x))
        self.y = max(0, min(HEIGHT - PLAYER_SIZE, self.y))
        
        if moved and self.connected:
            self._send_data({"type": "move", "player_id": self.player_id, "x": self.x, "y": self.y})
    
    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        
        # Draw all players
        for pid, player in self.players.items():
            # If it's the current player (client), make it green, else red
            if pid == self.player_id:
                color = (0, 255, 0)  # Green for the client
            else:
                color = (255, 0, 0)  # Red for other players
            
            pygame.draw.rect(self.screen, color, (player["x"], player["y"], PLAYER_SIZE, PLAYER_SIZE))
            
            # Draw nickname above player
            nickname = self.nicknames.get(pid, "Unknown")
            text = self.font.render(nickname, True, (255, 255, 255))
            self.screen.blit(text, (player["x"], player["y"] - 25))
        
        # Draw connection status
        status = "Connected" if self.connected else "Disconnected"
        status_color = (0, 255, 0) if self.connected else (255, 0, 0)
        status_text = self.font.render(f"Status: {status}", True, status_color)
        self.screen.blit(status_text, (10, 10))
        
        # Draw messages
        for i, message in enumerate(self.messages):
            text = self.font.render(message, True, (255, 255, 255))
            self.screen.blit(text, (10, 40 + i * 25))
        
        pygame.display.flip()  # Update the display
    
    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Simple chat input
                        message = input("Enter message: ")
                        if self.connected:
                            self._send_data({"type": "message", "player_id": self.player_id, "text": message})
            
            self.handle_input()
            self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    game_client = Client()
    game_client.run()
