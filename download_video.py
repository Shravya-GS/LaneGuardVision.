import requests
import sys
import os

# Alternate reliable URL
url = "https://github.com/intel-iot-devkit/sample-videos/raw/master/person-bicycle-car-detection.mp4"
output_path = "highway_sample.mp4"

print(f"Downloading video from {url}...")
try:
    if os.path.exists(output_path):
        os.remove(output_path)
        
    response = requests.get(url, stream=True, verify=False) # Skip SSL verify for speed/errors
    if response.status_code != 200:
        print(f"Failed with status code: {response.status_code}")
        sys.exit(1)
        
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Video downloaded successfully to {output_path}")
except Exception as e:
    print(f"Error downloading video: {e}")
    sys.exit(1)
