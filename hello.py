# hello.py

import requests

def main():
    print("Hello, world!")

def get_weather():
    # Using wttr.in API which detects location from IP and provides simple weather info
    try:
        response = requests.get("https://wttr.in/?format=3", timeout=5)
        if response.status_code == 200:
            print(response.text)
        else:
            print("Error fetching weather")
    except requests.RequestException as e:
        print(f"Error fetching weather: {e}")

if __name__ == "__main__":
    main()
    # Call the function to get current weather
    get_weather()
