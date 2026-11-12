import socket
import time

LIDAR_IP = "195.37.48.222"
LIDAR_PORT = 2111

print("Forcing LiDAR to stop all streams...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    sock.connect((LIDAR_IP, LIDAR_PORT))
    
    # Send all known SICK stop commands
    commands = [
        b"\x02sEN ScanDataEnable 0\x03",
        b"\x02sEN LMDscandata 0\x03",
        b"\x02sEA LMDscandata 0\x03"
    ]
    
    for cmd in commands:
        sock.sendall(cmd)
        time.sleep(0.1) # Brief pause between commands
        
    print(" SUCCESS: All stop commands sent! The sensor should be quiet now.")
    
except Exception as e:
    print(f" FAILED to connect: {e}")
    print(" -> Make sure SOPAS is entirely closed so Python can access port 2111.")
finally:
    sock.close()