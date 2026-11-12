import socket
import math
import csv

# SICK TiM781 Front LiDAR Network Configuration
LIDAR_IP = "195.37.48.222"
LIDAR_PORT = 2111

def test_lidar_connection():
    print(f"Attempting to connect to SICK TiM781 at {LIDAR_IP}:{LIDAR_PORT}...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)  # 5 second timeout
    
    try:
        # 1. Connect to the sensor
        sock.connect((LIDAR_IP, LIDAR_PORT))
        print("✅ SUCCESS: Connected to SICK TiM781 hardware!")
        
        # 2. Send command to enable scan data output
        command = b"\x02sEN ScanDataEnable 1\x03"
        print("Sending stream request command...")
        sock.sendall(command)
        
        # 3. Read the first incoming response packet
        print("Listening for incoming data packet...")
        data = sock.recv(2048)  # Read up to 2KB of data
        
        if data:
            print(f"🎉 Received {len(data)} bytes of live sensor data!")
            
            # Decode raw bytes to string, ignoring unreadable binary characters
            decoded_packet = data.decode('ascii', errors='ignore')
            
            # Split the packet into tokens/parameters
            tokens = decoded_packet.split()
            print(f"Extracted data tokens count: {len(tokens)}")
            
            # 4. Save data directly to a CSV file for Excel
            csv_filename = "lidar_scan_data.csv"
            with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                # Write header row
                writer.writerow(["Token_Index", "Value"])
                # Write each token/measurement value into a row
                for i, token in enumerate(tokens):
                    writer.writerow([i, token])
            
            print(f"💾 Successfully saved scan data to '{csv_filename}'! You can open this file directly in Excel.")
            
        else:
            print("⚠️ Connected, but received empty data from the sensor.")
            
    except socket.timeout:
        print("❌ TIMEOUT: Could not reach the sensor. Check IP and power.")
    except ConnectionRefusedError:
        print("❌ REFUSED: Connection refused. Verify the IP address.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        sock.close()
        print("Socket closed.")

if __name__ == "__main__":
    test_lidar_connection()