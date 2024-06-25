import numpy as np

def calculate_linear_velocity(prev_position, current_position, time_interval):
    # Calculate the difference in positions
    delta_position = np.array(current_position) - np.array(prev_position)
    # Calculate the velocity
    velocity = delta_position / time_interval
    return velocity

def create_pose(relative_north, relative_east, relative_down, linear_velocity, angular_velocity_z):
    # Define the pose structure with provided values
    pose = {
        "aFromB": {
            "rotation": {
                "unitQuaternion": {
                    "imag": {
                        "z": -0.6871226213588081
                    },
                    "real": 0.7265414669631735
                }
            },
            "translation": {
                "x": relative_east,
                "y": -relative_north
            }
        },
        "frameA": "world",
        "frameB": "goal1_35",
        "tangentOfBInA": {
            "linearVelocity": {
                "x": linear_velocity[0],  # Linear velocity in the east direction
                "y": linear_velocity[1]   # Linear velocity in the north direction
            },
            "angularVelocity": {
                "z": angular_velocity_z    # Angular velocity around the z-axis
            }
        }
    }
    return pose

# Example usage:
relative_north = 23.167083193484956
relative_east = 6.939125721012264
relative_down = 0.0

# Example GPS positions (latitude, longitude, altitude)
prev_gps_position = (37.7749, -122.4194, 10)  # Previous position (lat, lon, alt)
current_gps_position = (37.7750, -122.4195, 10)  # Current position (lat, lon, alt)
time_interval = 1  # Time interval in seconds

# Calculate linear velocity from GPS positions
linear_velocity = calculate_linear_velocity(prev_gps_position, current_gps_position, time_interval)

# Example angular velocity (radians per second)
angular_velocity_z = -0.002500322489257857

# Create the pose
generated_pose = create_pose(relative_north, relative_east, relative_down, linear_velocity, angular_velocity_z)
print(generated_pose)
