import os
import time
import csv
import socket
import threading

# --- SICK TiM781 Dual LiDAR Network Configuration ---
FRONT_LIDAR_IP = "195.37.48.222"
REAR_LIDAR_IP = "195.37.48.223"
LIDAR_PORT = 2111

# Automatically saves CSV in the exact same folder as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILENAME = os.path.join(SCRIPT_DIR, "dual_lidar_live_data.csv")

# Shared cache for both LiDAR background threads
recording = True
lidar_data = {
    "front_bytes": 0,
    "front_preview": "",
    "rear_bytes": 0,
    "rear_preview": ""
}

def lidar_reader_thread(name, ip, port, prefix):
    """Connects to a SICK TiM781 LiDAR and continuously updates its latest scan packet."""
    global recording, lidar_data
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3.0)

    try:
        sock.connect((ip, port))
        # Send CoLa command to enable continuous scan stream
        sock.sendall(b"\x02sEN ScanDataEnable 1\x03")
        print(f" {name} LiDAR connected at {ip}:{port}")

        while recording:
            try:
                data = sock.recv(4096)
                if data:
                    lidar_data[f"{prefix}_bytes"] = len(data)
                    decoded = data.decode("ascii", errors="ignore").strip()
                    lidar_data[f"{prefix}_preview"] = decoded[:60].replace("\n", " ").replace("\r", "")
                else:
                    lidar_data[f"{prefix}_bytes"] = 0
            except socket.timeout:
                lidar_data[f"{prefix}_bytes"] = 0

    except Exception as e:
        print(f" {name} LiDAR ({ip}) connection failed: {e}")
    finally:
        sock.close()
        print(f"Closed {name} LiDAR socket.")

def run_dual_lidar_logger():
    global recording
    print("Starting Dual SICK TiM781 LiDAR Logger...")
    print(f"Saving data to: {LOG_FILENAME}\n")

    # 1. Start Front and Rear LiDAR threads simultaneously
    front_thread = threading.Thread(
        target=lidar_reader_thread, args=("Front", FRONT_LIDAR_IP, LIDAR_PORT, "front"), daemon=True
    )
    rear_thread = threading.Thread(
        target=lidar_reader_thread, args=("Rear", REAR_LIDAR_IP, LIDAR_PORT, "rear"), daemon=True
    )
    front_thread.start()
    rear_thread.start()

    # Give sockets a moment to connect
    time.sleep(1.0)

    # 2. Write synchronized rows to CSV at ~15 Hz (matching TiM781 scan rate)
    with open(LOG_FILENAME, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "Timestamp",
            "Front_Packet_Bytes", "Front_Data_Preview",
            "Rear_Packet_Bytes", "Rear_Data_Preview"
        ])

        scan_count = 0
        try:
            print("📡 Logging live Front + Rear LiDAR scans (Press Ctrl+C to stop)...\n")
            while True:
                current_time = time.time()

                f_bytes = lidar_data["front_bytes"]
                f_prev = lidar_data["front_preview"]
                r_bytes = lidar_data["rear_bytes"]
                r_prev = lidar_data["rear_preview"]

                writer.writerow([
                    f"{current_time:.3f}",
                    f_bytes, f_prev,
                    r_bytes, r_prev
                ])
                scan_count += 1

                # Print live status once per second (every 15 cycles)
                if scan_count % 15 == 0:
                    print(
                        f"[{time.strftime('%H:%M:%S')}] Logged {scan_count} rows | "
                        f"Front: {f_bytes} B | Rear: {r_bytes} B"
                    )

                time.sleep(0.067)  # ~15 Hz logging interval

        except KeyboardInterrupt:
            print(f"\n Stopping logger...")
        finally:
            recording = False
            time.sleep(0.5)
            print(f" Saved {scan_count} dual-LiDAR records cleanly to '{LOG_FILENAME}'.")

if __name__ == "__main__":
    run_dual_lidar_logger()