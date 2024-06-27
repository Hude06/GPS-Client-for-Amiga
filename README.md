# Ariel Aerial

### What is Ariel Aerial?

- Ariel Amiga is a Drone companion that makes using the Amiga much more enjoyable.

### What do I have working already?

1. Getting the amiga to be able to drive from plain Lat Long and from an outside source.
   - Right now the only way to create a track for the Amiga is with the teach and repeat inside of Autoplot.
2. Created a function that calculates the different and finds out where the base station is based on the GPS class using the amiga core

   - `    base_lat = (
    geodesic(meters=-north_from_base)
    .destination((amiga_lat, amiga_lon), bearing=0)
    .latitude
)
base_lon = (
    geodesic(meters=-east_from_base)
    .destination((amiga_lat, amiga_lon), bearing=90)
    .longitude
)
return base_lat, base_lon`
     This code allows me to reverse the RELPOSNED Coordinates of the Amiga and find out where the base station is

3. GPS Module and a Feather S2.
   - I have been using a Feather S2 and a GPS module to get the Longitude and Latitude of the Drone and then they it gets sent to my server. Then using my UI I am able to stop and start the tracking of the drone. Finally the server stores the GPS and waits for a call from the amiga. The amiga then sends out a fetch and pulls down the most recent Map or Run. The amiga then converts it to RELPOSNED using some of the functions I mentioned before and it will then format it in a way that the Auto Plot app can use.

# Ideas for the camera system

- 3 Raspberry Pi Cameras a 1X 3X and 5X
- Taking 2 pic per second. So I would have 6 Pics per second on a drive
- Have a external SSD on board to save to disk

### Partical IO

- Partical IO is a company that sells ESP 32 board but they have Cellular Data on them. Only a one time fee of around 50$ for one board. With that 50$ one time fee you can get up to 100,000 API calls per month. Each call can be up to 1KB.

### FPV Drone Parts and Arducopter

- Arducopter is a drone software that you can load onto you drones Flight Controller and it will let you autonomously fly your drone.
- The drone would then fly in a grid taking pictures every second and mapping those to GPS coordinates for latter

# Setup

`pip install --upgrade pip`

`pip install --upgrade setuptools`

`pip3 install farm-ng-amiga`

`pip install -r requirements.txt`
