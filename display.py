from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import argparse
import os
import datetime
from screeninfo import get_monitors

def manage_browser_sessions(shutdown_hour, shutdown_minute, countdown_seconds):
    print("Script started")
    monitors = get_monitors()
    print(f"Detected {len(monitors)} monitors.\n")

    for monitor in monitors:
        print(f"Monitor Name: {monitor.name}, Width: {monitor.width}, Height: {monitor.height}, Position: (X: {monitor.x}, Y: {monitor.y})\n")

    urls = [
        "https://www.nationalgallery.sg/",
        "https://www.youtube.com/",
        "https://www.google.com"
    ]

    target_monitors = [monitors[2], monitors[1], monitors[3]]

    browsers = []  # List to store all browser instances

    # Open all the browser windows first
    for _ in urls:
        browser = webdriver.Chrome()  # Just open Chrome without any positioning arguments
        time.sleep(2)  # Let it render
        browsers.append(browser)  # Store the browser instance for later use

    # Position and maximize each browser
    for index, browser in enumerate(browsers):
        # Set the position using Selenium
        browser.set_window_position(target_monitors[index].x, target_monitors[index].y)
        time.sleep(2)  # Let the move complete
        browser.maximize_window()  # Now maximize it

        window_rect = browser.get_window_rect()
        print(f"Initial position for window {index + 1}: X={window_rect['x']}, Y={window_rect['y']}, Width={window_rect['width']}, Height={window_rect['height']}")

    # Navigate to the desired URLs
    for index, (browser, url) in enumerate(zip(browsers, urls)):
        browser.get(url)
        time.sleep(5)

        window_rect = browser.get_window_rect()
        print(f"Maximized position for window {index + 1}: X={window_rect['x']}, Y={window_rect['y']}, Width={window_rect['width']}, Height={window_rect['height']}")

        print(f"Browser window {index + 1} opened and maximized on monitor {index + 1} with URL: {url}\n")

    # Wait for shutdown or countdown
    if countdown_seconds:
        print(f"Waiting for {countdown_seconds} seconds to close browsers...")
        time.sleep(countdown_seconds)
        for browser in browsers:
            browser.quit()
    elif shutdown_hour is not None and shutdown_minute is not None:
        print(f"Waiting until {shutdown_hour}:{shutdown_minute} to close browsers...")
        while True:
            now = datetime.datetime.now()
            if now.hour == shutdown_hour and now.minute == shutdown_minute:
                break
            time.sleep(1)
        for browser in browsers:
            browser.quit()
    else:
        print("No shutdown time or countdown specified. Browsers will remain open. Press Enter when you wish to close them.")
        input()  # Wait for user to press Enter

    if countdown_seconds or (shutdown_hour and shutdown_minute):
        # Turn off the monitors using nircmd
        print("Turning off monitor...")
        os.system('C:\\Users\\erniesg\\Downloads\\nircmd\\nircmd.exe monitor off')
        time.sleep(5)

    print("Script finished")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hour", type=int, help="Hour to shutdown", default=None)
    parser.add_argument("--minute", type=int, help="Minute to shutdown", default=None)
    parser.add_argument("--countdown", type=int, help="Countdown seconds to shutdown", default=None)
    args = parser.parse_args()

    manage_browser_sessions(args.hour, args.minute, args.countdown)
