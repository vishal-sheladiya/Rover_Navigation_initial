import numpy as np
import time
import matplotlib.pyplot as plt

def simulate_imu_data():
    accel_x = np.random.normal(0.0, 0.05)
    accel_y = np.random.normal(0.0, 0.05)
    accel_z = np.random.normal(9.81, 0.05)
    
    gyro_x = np.random.normal(0.0, 0.1)
    gyro_y = np.random.normal(0.0, 0.1)
    gyro_z = np.random.normal(0.0, 0.1)
    
    return (accel_x, accel_y, accel_z), (gyro_x, gyro_y, gyro_z)

def simulate_dgps_data(step):
    base_lat = 53.539500
    base_lon = 8.580000
    
    current_lat = base_lat + (step * 0.00001) + np.random.normal(0, 0.000002)
    current_lon = base_lon + (step * 0.00001) + np.random.normal(0, 0.000002)
    
    return current_lat, current_lon

# Data storage lists for visualization
timestamps = []
accel_data = []
gyro_data = []
gps_data = []

print("Starting Rover IMU and DGPS Telemetry Stream...\n")

start_time = time.time()
for i in range(10):  # Stream 10 samples
    elapsed = time.time() - start_time
    accel, gyro = simulate_imu_data()
    lat, lon = simulate_dgps_data(i)
    
    # Save measurements to lists
    timestamps.append(elapsed)
    accel_data.append(accel)
    gyro_data.append(gyro)
    gps_data.append((lat, lon))
    
    print(f"--- Timestamp: {time.time():.2f} ---")
    print(f"IMU Accel (m/s^2): X={accel[0]:.3f}, Y={accel[1]:.3f}, Z={accel[2]:.3f}")
    print(f"IMU Gyro  (deg/s): X={gyro[0]:.3f}, Y={gyro[1]:.3f}, Z={gyro[2]:.3f}")
    print(f"DGPS Pos: Lat={lat:.6f}, Lon={lon:.6f}\n")
    
    time.sleep(0.5)

# Convert recorded data to NumPy arrays for easy indexing
accel_np = np.array(accel_data)
gyro_np = np.array(gyro_data)
gps_np = np.array(gps_data)

fig, axs = plt.subplots(3, 1, figsize=(10, 10))
fig.suptitle('Rover IMU and DGPS Telemetry Analysis', fontsize=14, fontweight='bold')

#Subplot_1 : Acceleration
axs[0].plot(timestamps, accel_np[:, 0], label='Accel X (m/s²)', color='r')
axs[0].plot(timestamps, accel_np[:, 1], label='Accel Y (m/s²)', color='g')
axs[0].plot(timestamps, accel_np[:, 2], label='Accel Z (m/s²)', color='b')
axs[0].set_ylabel('Acceleration (m/s²)')
axs[0].set_title('IMU Linear Acceleration')
axs[0].grid(True, linestyle='--', alpha=0.6)
axs[0].legend(loc='upper right')

#subplot_2 - Gyroscope
axs[1].plot(timestamps, gyro_np[:, 0], label='Gyro Roll (deg/s)', color='m')
axs[1].plot(timestamps, gyro_np[:, 1], label='Gyro Pitch (deg/s)', color='c')
axs[1].plot(timestamps, gyro_np[:, 2], label='Gyro Yaw (deg/s)', color='y')
axs[1].set_ylabel('Angular Velocity (deg/s)')
axs[1].set_title('IMU Gyroscope Readings')
axs[1].grid(True, linestyle='--', alpha=0.6)
axs[1].legend(loc='upper right')

# Subplot_3 - DGPS Trajectory
plt.subplot(3, 1, 3)
plt.plot(gps_np[:, 1], gps_np[:, 0], label='Rover Path', color='purple', marker='s', linestyle='-')
plt.title('DGPS Trajectory (Hochschule Bremerhaven Coordinates)')
plt.xlabel('Longitude (°E)')
plt.ylabel('Latitude (°N)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='upper left')

plt.tight_layout()

plt.show()




