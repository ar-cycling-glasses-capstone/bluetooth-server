import json
import bluetooth
import subprocess
from bluetooth import BluetoothSocket, RFCOMM
import time
import queue

class Server:
    def __init__(self):
        self.data = json.loads("{}")
        self.connected = False
        self.set_discoverable(True)

        self.server_socket = BluetoothSocket(RFCOMM)
        self.server_socket.bind(("", bluetooth.PORT_ANY))
        self.server_socket.listen(1)

        print("Waiting for connection...")

    def __del__(self):
        if 'self.client_socket' in locals():
            self.client_socket.close()

        self.connected = False
        self.server_socket.close()
        self.set_discoverable(False)

    def get_data(self):
        return self.data
    
    def get_connected(self):
        return self.connected

    def handle_data(self, data):
        self.data = data
        if "timer" in data:
            print(f"Timer: {data['timer']}")
        if "weather" in data:
            print(f"Weather: {data['weather']}")
        if "altitude" in data:
            print(f"Altitude: {data['altitude']}")
        if "hud_toggles" in data:
            print(f"HUD Toggles: {data['hud_toggles']}")

    def set_discoverable(self, state=True):
        mode = "piscan" if state else "noscan"
        subprocess.run(["sudo", "hciconfig", "hci0", mode])

    def main(self):
        while True:
            try:
                self.client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from {client_address}")
                self.connected = True
                try:
                    while True:
                        data = self.client_socket.recv(1024)
                        if len(data) == 0:
                            break
                        data_str = data.decode("utf-8")
                        data_json = json.loads(data_str)
                        self.handle_data(data_json)
                except json.JSONDecodeError:
                    print("Error: Invalid JSON data received")
                except Exception as e:
                    print(f"Error: {e}")
            except KeyboardInterrupt:
                print("Shutting down...")
                break
            except Exception as e:
                print(f"Error: {e}")
            finally:
                if 'self.client_socket' in locals():
                    self.client_socket.close()
                    self.connected = False
                    print("Client disconnected, waiting for a new connection...")

        self.connected = False
        self.server_socket.close()
        self.set_discoverable(False)

if __name__ == "__main__":
    server = Server()
    server.main()