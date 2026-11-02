import socket

# SICK TiM781 Front LiDAR Network Configuration (from your specifications)
LIDAR_IP = "195.37.48.222"
LIDAR_PORT = 2111

def test_lidar_connection():
    print(f"Attempting to connect to SICK TiM781 at {LIDAR_IP}:{LIDAR_PORT}...")
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)  # 5 second timeout so it doesn't freeze if it fails
    
    try:
        # 1. Connect to the sensor
        sock.connect((LIDAR_IP, LIDAR_PORT))
        print("✅ SUCCESS: Connected to SICK TiM781 hardware!")
        
        # 2. Send command to enable scan data output (CoLa-A / ASCII format request)
        # 'sEN ScanDataEnable 1' tells the sensor to start sending data frames
        command = b"\x02sEN ScanDataEnable 1\x03"
        print("Sending stream request command...")
        sock.sendall(command)
        
        # 3. Read the first incoming response packet
        print("Listening for incoming data packet...")
        data = sock.recv(2048)  # Read up to 2KB of data
        
        if data:
            print(f"🎉 Received {len(data)} bytes of live sensor data!")
            print(f"Raw data preview (first 50 bytes): {data[:50]}")
        else:
            print("⚠️ Connected, but received empty data from the sensor.")
            
    except socket.timeout:
        print("❌ TIMEOUT: Could not reach the sensor. Check if:")
        print("   - Your laptop's Ethernet IP is on the correct subnet.")
        print("   - The LiDAR power supply (9-28V DC) is turned on.")
    except ConnectionRefusedError:
        print("❌ REFUSED: Connection refused. Check if the IP address is correct.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        # Always close the socket when finished
        sock.close()
        print("Socket closed.")

if __name__ == "__main__":
    test_lidar_connection()