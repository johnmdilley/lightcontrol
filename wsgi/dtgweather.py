import requests
import re

def get_temperature():
    r = requests.get("http://www.cl.cam.ac.uk/research/dtg/weather/current-obs.txt")
    r.raise_for_status()
    m = re.search(r"Temperature:\s+(.+)\s+C", r.content)
    return float(m.group(1))

if __name__ == "__main__":
    print get_temperature()
