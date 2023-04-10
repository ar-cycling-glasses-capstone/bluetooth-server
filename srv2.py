import json
import bluetooth
import subprocess
from bluetooth import BluetoothSocket, RFCOMM
import time

def handle_data(data):
    if "timer" in data:
        print(f"Timer: {data['timer']}")
    if "weather" in data:
        print(f"Weather: {data['weather']}")
    if "altitude" in data:
        print(f"Altitude: {data['altitude']}")
    if "hud_toggles" in data:
        print(f"HUD Toggles: {data['hud_toggles']}")

def set_discoverable(state=True):
    mode = "piscan" if state else "noscan"
    subprocess.run(["sudo", "hciconfig", "hci0", mode])

def main():
    set_discoverable(True)

    server_socket = BluetoothSocket(RFCOMM)
    server_socket.bind(("", bluetooth.PORT_ANY))
    server_socket.listen(1)

    # uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    # bluetooth.advertise_service(server_socket, "RaspberryPiServer", service_id=uuid, service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS], profiles=[bluetooth.SERIAL_PORT_PROFILE])

    print("Waiting for connection...")
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            try:
                while True:
                    data = client_socket.recv(1024)
                    if len(data) == 0:
                        break
                    data_str = data.decode("utf-8")
                    data_json = json.loads(data_str)
                    handle_data(data_json)
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
            if 'client_socket' in locals():
                client_socket.close()
                print("Client disconnected, waiting for a new connection...")

    server_socket.close()
    set_discoverable(False)

if __name__ == "__main__":
    main()