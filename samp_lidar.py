import numpy as np
import matplotlib.pyplot as plt

def simulate_lidar_scan():
    # TiM781 specs: 270-degree FOV (-135 to +135 degrees), 0.33 degrees resolution (~811 points) - given in data sheet
    num_points = 811
    angles_deg = np.linspace(-135, 135, num_points)
    angles_rad = np.radians(angles_deg)
    
    # Distance formula for a flat wall straight ahead (Simulate background noise): r = 5.0 / cos(angle)
    distances = 5.0 / np.cos(angles_rad)
    
    # Clip to max range of TiM781 (25 meters) and add minor sensor noise
    distances = np.clip(distances, 0.05, 25.0)
    distances += np.random.normal(0, 0.015, num_points)
    distances = np.clip(distances, 0.05, 25.0)

    # obstacles (e.g., a pillar or person at an angle of 30 degrees, 2 meters away)
    obstacle_mask = (angles_deg >= 20) & (angles_deg <= 40)
    distances[obstacle_mask] = 2.0 + np.random.normal(0, 0.01, np.sum(obstacle_mask))
    
    return angles_rad, distances

def plot_lidar_data(angles_rad, distances):
    # Convert Polar coordinates (distance, angle) to Cartesian (X, Y) coordinates
    # x = forawrd, y = left
    x = distances * np.cos(angles_rad)
    y = distances * np.sin(angles_rad)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # scatter plot
    scatter = ax.scatter(y, x, c=distances, cmap='viridis', s=10)
    
    ax.set_title("Simulated SICK TiM781 2D LiDAR Scan (-135° to +135°)", fontsize=12)
    ax.set_xlabel("Y Position (meters) [Left/Right]", fontsize=10)
    ax.set_ylabel("X Position (meters) [Forward]", fontsize=10)
    ax.axhline(0, color='grey', linewidth=0.8, linestyle='--')
    ax.axvline(0, color='grey', linewidth=0.8, linestyle='--')
    
    # sensor position at (0,0 mark)
    ax.scatter([0], [0], color='red', s=100, label='LiDAR Sensor (0,0)', zorder=5)
    
    ax.set_xlim(-10, 10)
    ax.set_ylim(-2, 12)
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right')
    
    cbar = plt.colorbar(scatter)
    cbar.set_label('Distance (meters)')
    
    plt.tight_layout()

    plt.savefig(
    r"D:\Hochschule Bremerhaven\sem 2\Project\scripts\sample_data_lidar\lidar_scan.png",
    dpi=300,
    bbox_inches="tight"
    )

    plt.show()

if __name__ == "__main__":
    print("Generating simulated SICK TiM781 scan data...")
    angles, dists = simulate_lidar_scan()
    print(f"Generated {len(dists)} data points. Rendering plot...")
    plot_lidar_data(angles, dists)