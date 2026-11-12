import time
import csv
from sbp.client.drivers.network_drivers import TCPDriver
from sbp.client import Handler, Framer
from sbp.imu import SBP_MSG_IMU_RAW

# Piksi Multi Network Settings
PIKSI_IP = "195.37.48.233"
PIKSI_PORT = 55555  # Default SBP TCP Server port
LOG_FILENAME = "real_imu_telemetry.csv"

# Bosch BMI160 Scale Factors (Default Piksi Multi configuration: +-2g accel, +-250 deg/s gyro)
ACCEL_SCALE = 9.81 / 16384.0   # Converts raw LSB to m/s^2
GYRO_SCALE = 1.0 / 131.0       # Converts raw LSB to deg/s

def run_real_imu_logger():
    print(f"Connecting to Piksi Multi SBP stream at {PIKSI_IP}:{PIKSI_PORT}...")
    
    with open(LOG_FILENAME, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "Timestamp",
            "IMU_Accel_X_ms2", "IMU_Accel_Y_ms2", "IMU_Accel_Z_ms2",
            "IMU_Gyro_X_degs", "IMU_Gyro_Y_degs", "IMU_Gyro_Z_degs"
        ])

        try:
            with TCPDriver(PIKSI_IP, PIKSI_PORT) as driver:
                with Handler(Framer(driver.read, None, verbose=False)) as source:
                    print(f" Connected! Logging real Bosch BMI160 IMU data to '{LOG_FILENAME}' (Ctrl+C to stop)...")
                    
                    for msg, metadata in source.filter(SBP_MSG_IMU_RAW):
                        current_time = time.time()
                        
                        # Convert raw integer readings to physical units
                        ax = msg.acc_x * ACCEL_SCALE
                        ay = msg.acc_y * ACCEL_SCALE
                        az = msg.acc_z * ACCEL_SCALE
                        
                        gx = msg.gyr_x * GYRO_SCALE
                        gy = msg.gyr_y * GYRO_SCALE
                        gz = msg.gyr_z * GYRO_SCALE
                        
                        writer.writerow([
                            f"{current_time:.3f}",
                            f"{ax:.3f}", f"{ay:.3f}", f"{az:.3f}",
                            f"{gx:.3f}", f"{gy:.3f}", f"{gz:.3f}"
                        ])
                        
                        print(f"[{time.strftime('%H:%M:%S')}] Accel (m/s²): X={ax:.2f}, Y={ay:.2f}, Z={az:.2f} | Gyro (deg/s): Z={gz:.2f}")

        except KeyboardInterrupt:
            print(f"\n Stopped logging. Real IMU session saved to '{LOG_FILENAME}'.")
        except Exception as e:
            print(f" Connection Error: {e}")

if __name__ == "__main__":
    run_real_imu_logger()