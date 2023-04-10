# Opens up a serial bluetooth connection

import bluetooth
import datetime
import subprocess
import uuid

import json


class Server:
    def get_info(self):
        return self.data

    def send_data(self, data):
        self.client_socket.send(data.encode())

    def __init__(self):
        self.data = []

        # Make the Raspberry Pi discoverable
        subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])

        self.init_server()

    def init_server(self):
        # Define the Bluetooth server parameters
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        port = 1  # This should match the port number on the client device
        # server_socket.bind(("", port))
        self.server_socket.bind(("", bluetooth.PORT_ANY))
        self.server_socket.listen(1)
        self.connected = False

        # Open a log file to write the received data
        self.log_file = open("bluetooth_log.txt", "a")

    def main_loop(self):
        try:
            if (self.connected == False):
                print("Waiting for Bluetooth connection...")

                # Wait for a client to connect
                self.client_socket, address = self.server_socket.accept()
                # client_socket.setblocking(False)
                print("Connected to", address)
                self.connected = True

            # Receive data from the client
            data = self.client_socket.recv(1024)

            if not data:
                raise Exception

            # Update class variable to prepare for retrieval
            try:
                self.data = json.loads(data.decode())
            except Exception as e:
                print("Not a JSON")
                self.data = data.decode()

            print(self.data)

            # Log the received data with timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            self.log_file.write(f"{timestamp}: {data.decode()}\n")
            self.log_file.flush()  # Force write to file

            # Send an acknowledgement back to the client
            ack = "Received: " + data.decode()
            self.client_socket.send(ack.encode())

        except KeyboardInterrupt:
            print("\nClosing Bluetooth Server...")
            self.log_file.close()
            self.client_socket.close()
            self.server_socket.close()
        except bluetooth.btcommon.BluetoothError:  # User disconnected from Bluetooth
            print("Disconnected")
            connected = False

        # Close the log file and the Bluetooth sockets
        # log_file.close()
        # client_socket.close()
        # server_socket.close()
