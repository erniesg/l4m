from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import argparse
import pyautogui
import pygetwindow as gw
import os

def manage_browser_sessions(shutdown_hour, shutdown_minute, countdown_seconds):
    print("Script started")

    # Define chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # Setup ChromeDriver
    webdriver_service = Service(ChromeDriverManager().install())

    # Create a new Chrome browser instance
    browser1 = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    browser1.get("https://erniesg.budibase.app/app/testfeedback#/leaderboard")
    time.sleep(3)

    # Find the window and maximize
    window1 = gw.getWindowsWithTitle('Google Chrome')[0]
    print(f"Window1 position: {window1.left}, {window1.top}")

    # Move the browser window to the first screen (located above)
    print("Moving first window to first screen...")
    pyautogui.FAILSAFE = False  # Disable the fail-safe feature
    pyautogui.moveTo(0, 0)  # Move the cursor to the top-left corner of the screen
    print("Cursor initialised at the top left.")
    pyautogui.dragTo(0, -2160, 2, button='left')  # Then drag the cursor to the destination coordinates
    pyautogui.FAILSAFE = True  # Enable the fail-safe feature again
    print("Window1 moved to first screen.")

    # Fullscreen the window once it's on the first screen
    window1.maximize()
    print("Window1 maximized.")

    # Move the cursor back to the main screen
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(960, 540)  # These coordinates are in the middle of a 1920x1080 screen. Adjust if necessary.
    pyautogui.FAILSAFE = True
    print("Cursor moved back to main screen.")

    # Create a second Chrome browser instance
    browser2 = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    browser2.get("https://erniesg.budibase.app/app/testfeedback#/feedback")
    time.sleep(3)

    # Find the window and ensure it is on screen 2
    window2 = gw.getWindowsWithTitle('Google Chrome')[0]
    print(f"Window2 position: {window2.left}, {window2.top}")

    # Maximize window2
    window2.maximize()

    # If countdown_seconds is specified, we simply sleep for that long.
    if countdown_seconds:
        print(f"Waiting for {countdown_seconds} seconds to close browsers and turn off the monitor...")
        time.sleep(countdown_seconds)
    else:
        # Otherwise, we wait until it's the specified shutdown time
        print(f"Waiting until {shutdown_hour}:{shutdown_minute} to close browsers and turn off the monitor...")
        while True:
            now = datetime.datetime.now()
            if now.hour == shutdown_hour and now.minute == shutdown_minute:
                break
            time.sleep(1)

    # Close all browser windows
    browser1.quit()
    browser2.quit()
    print("Browser windows closed.")

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

    if args.countdown is None and (args.hour is None or args.minute is None):
        print("Either --hour and --minute, or --countdown must be specified.")
        exit(1)

    manage_browser_sessions(args.hour, args.minute, args.countdown)
