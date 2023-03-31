# Opens up a serial bluetooth connection 

import bluetooth
import datetime
import subprocess
import uuid

import json

class Server:
    def get_info(self):
        return self.data
    
    def __init__(self):
        self.data = []

        # Make the Raspberry Pi discoverable
        subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])

        self.main_loop()
    
    def main_loop(self):
        # Define the Bluetooth server parameters
        server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        port = 1  # This should match the port number on the client device
        # server_socket.bind(("", port))
        server_socket.bind(("", bluetooth.PORT_ANY))
        server_socket.listen(1)
        connected = False;


        # Open a log file to write the received data
        log_file = open("bluetooth_log.txt", "a")

        
        while True:
            try:
                if (connected == False):
                    print("Waiting for connection...")

                    # Wait for a client to connect
                    client_socket, address = server_socket.accept()
                    # client_socket.setblocking(False)
                    print("Connected to", address)
                    connected = True
                
                
                # Receive data from the client
                data = client_socket.recv(1024)
                
                
                if not data:
                    break

                # Update class variable to prepare for retrieval
                self.data = json.loads(data.decode())

                # Log the received data with timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                log_file.write(f"{timestamp}: {data.decode()}\n")
                log_file.flush()  # Force write to file

                # Send an acknowledgement back to the client
                ack = "Received: " + data.decode()
                client_socket.send(ack.encode())

            except KeyboardInterrupt:
                print("\nClosing Bluetooth Server...")
                log_file.close()
                client_socket.close()
                server_socket.close()
                break;
            except bluetooth.btcommon.BluetoothError: # User disconnected from Bluetooth 
                print("Disconnected")
                connected = False;

        # Close the log file and the Bluetooth sockets
        # log_file.close()
        # client_socket.close()
        # server_socket.close()
    

    