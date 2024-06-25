from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from farm_ng.core.event_client import EventClient
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.core.events_file_reader import proto_from_json_file
from farm_ng.gps import gps_pb2
from geopy.distance import geodesic
from geopy import Point
import requests
import math

url = 'https://apps.judemakes.com/amiga/gps'
response = requests.get(url)
amigaLat = 0
amigaLong = 0

global PastRelativeEast = 0
global PastRelativeNorth = 0

def latlon_to_relposned(base_lat, base_lon, target_lat, target_lon):

    """Convert latitude and longitude to North, East relative positions.

    Parameters:
    - base_lat, base_lon: The latitude and longitude of the reference point (e.g., current robot position).
    - target_lat, target_lon: The latitude and longitude of the target point.

    Returns:
    - (north, east): The North and East displacement from the reference point in meters.
    """
    # Calculate the North displacement (in meters)
    north = geodesic((base_lat, base_lon), (target_lat, base_lon)).meters

    # Calculate the East displacement (in meters)
    east = geodesic((base_lat, base_lon), (base_lat, target_lon)).meters

    return north, east

def calculate_base_station(amiga_lat, amiga_lon, north_from_base, east_from_base):
    base_lat = geodesic(meters=-north_from_base).destination((amiga_lat, amiga_lon), bearing=0).latitude
    base_lon = geodesic(meters=-east_from_base).destination((amiga_lat, amiga_lon), bearing=90).longitude
    return base_lat, base_lon

def calculate_heading_from_relpos(north1, east1, north2, east2):
    """
    Calculate the heading (bearing) between two points based on relative north and east coordinates.

    Parameters:
    north1, east1 : float : Relative north and east coordinates of the first point
    north2, east2 : float : Relative north and east coordinates of the second point

    Returns:
    dict : Dictionary containing unit quaternion components for the heading
    """
    
    # Calculate the difference in north and east coordinates
    delta_north = north2 - north1
    delta_east = east2 - east1
    
    # Calculate the initial bearing (angle from east direction)
    if delta_east == 0:
        if delta_north > 0:
            initial_bearing = 0
        elif delta_north < 0:
            initial_bearing = 180
        else:
            initial_bearing = 0  # or any default value when both deltas are 0
    else:
        initial_bearing = math.atan2(delta_east, delta_north) * (180 / math.pi)
    
    # Normalize the bearing to 0-360 degrees
    compass_bearing = (initial_bearing + 360) % 360
    
    # Convert the compass bearing to a unit quaternion representation
    heading_quaternion = {}
    heading_quaternion['rotation'] = {
        'unitQuaternion': {
            'imag': {
                'z': math.sin(math.radians(compass_bearing) / 2)
            },
            'real': math.cos(math.radians(compass_bearing) / 2)
        }
    }
    
    return heading_quaternion

def create_pose(relative_pose_north, relative_pose_east, relative_pose_up):
    print("heading",calculate_heading_from_relpos(PastRelativeNorth, PastRelativeEast, relative_pose_north, relative_pose_east))
    pose = {
        "aFromB": {
            "heading": calculate_heading_from_relpos(PastRelativeNorth, PastRelativeEast, relative_pose_north, relative_pose_east),
            "translation": {
                "x": -relative_pose_east,
                "y": relative_pose_north
            }
        },
        "frameA": "world",
        "frameB": "robot",
        "tangentOfBInA": {
            "linearVelocity": {
                "x": 0.0019160988792246395
            },
            "angularVelocity": {
                "z": -0.004774989732354348
            }
        }
    }
    return pose

def print_relative_position_frame(msg, amigaLat, amigaLong):
    """Prints the relative position frame message.

    Args:
        msg: The relative position frame message.
        amigaLat: Latitude from the Amiga GPS.
        amigaLong: Longitude from the Amiga GPS.
    """

    if amigaLat != 0:
        BaseLat, BaseLong = calculate_base_station(amigaLat, amigaLong, msg.relative_pose_north, msg.relative_pose_east)
        PastRelativeNorth = msg.relative_pose_north
        PastRelativeEast = msg.relative_pose_east
        north, east = latlon_to_relposned(BaseLat, BaseLong, amigaLat, amigaLong)
        print("One Pose IS",create_pose(north,east,0))
    print("-" * 50)

def print_gps_frame(msg):
    """Prints the gps frame message.

    Args:
        msg: The gps frame message.
    """
    print("PVT FRAME \n")
    print(f"Message stamp: {msg.stamp.stamp}")
    print(f"GPS time: {msg.gps_time.stamp}")
    print(f"Latitude: {msg.latitude}")
    print(f"Longitude: {msg.longitude}")
    return float(msg.latitude), float(msg.longitude)

def print_ecef_frame(msg):
    """Prints the ecef frame message.

    Args:
        msg: The ecef frame message.
    """
    pass

async def main(service_config_path: Path) -> None:
    """Run the gps service client.

    Args:
        service_config_path (Path): The path to the gps service config.
    """
    global amigaLat, amigaLong  # Declare global variables
    config: EventServiceConfig = proto_from_json_file(service_config_path, EventServiceConfig())
    async for event, msg in EventClient(config).subscribe(config.subscriptions[0]):
        if isinstance(msg, gps_pb2.RelativePositionFrame):
            print_relative_position_frame(msg, amigaLat, amigaLong)
        elif isinstance(msg, gps_pb2.GpsFrame):
            amigaLat, amigaLong = print_gps_frame(msg)
            print (print_gps_frame(msg))
        elif isinstance(msg, gps_pb2.EcefCoordinates):
            print_ecef_frame(msg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="python main.py", description="Amiga GPS stream example.")
    parser.add_argument("--service-config", type=Path, required=True, help="The GPS config.")
    args = parser.parse_args()

    asyncio.run(main(args.service_config))
