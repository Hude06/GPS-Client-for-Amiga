import requests
import subprocess

# URL to fetch GPS data
url = 'https://apps.judemakes.com/amiga/gps'

# Make GET request to fetch GPS data
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Write response text to GPS.txt file
    with open('GPS.txt', 'w') as file:
        file.write(response.text)
    print("Data written to GPS.txt successfully.")
else:
    print(f"Error fetching data: {response.status_code}")

# Optionally, print the response text to console
print(response.text)

# Call main.py script with GPS.txt as service config
try:
    result = subprocess.run(['python', './gps_client/main.py', '--service-config', './gps_client/service_config.json'], capture_output=True, text=True)

    # Check if the command was successful
    print("Output:", result.stdout)
    print("Error running main.py:", result.stderr)
except subprocess.CalledProcessError as e:
    print("Error:", e)

