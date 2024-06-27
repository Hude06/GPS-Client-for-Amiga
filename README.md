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
