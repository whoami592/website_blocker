# Website Blocker Script
# Author: Mr. Sabaz Ali Khan (Ethical Hacker, Pakistan)
# Purpose: Block specified websites by modifying the host file for ethical purposes
# (e.g., productivity, parental controls). Run with administrative privileges.
# Disclaimer: Use only with proper authorization. Unauthorized use may be illegal.

import platform
import os
import time
from datetime import datetime

# Define host file path based on operating system
HOSTS_PATH = (
    r"C:\Windows\System32\drivers\etc\hosts"
    if platform.system() == "Windows"
    else "/etc/hosts"
)

# Localhost IP for blocking
REDIRECT_IP = "127.0.0.1"

# List of websites to block
WEBSITES = ["facebook.com", "www.facebook.com", "twitter.com", "www.twitter.com"]

# Time window for blocking (24-hour format, e.g., 9 AM to 5 PM)
BLOCK_START_HOUR = 9
BLOCK_END_HOUR = 17

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return os.geteuid() == 0 if platform.system() != "Windows" else True
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def block_websites():
    """Add websites to host file to block them."""
    try:
        with open(HOSTS_PATH, "r+") as file:
            content = file.read()
            for website in WEBSITES:
                if website not in content:
                    file.write(f"{REDIRECT_IP} {website}\n")
                    print(f"Blocked: {website}")
                else:
                    print(f"Already blocked: {website}")
    except PermissionError:
        print("Error: Run the script with administrative privileges.")
    except Exception as e:
        print(f"Error blocking websites: {e}")

def unblock_websites():
    """Remove websites from host file to unblock them."""
    try:
        with open(HOSTS_PATH, "r") as file:
            lines = file.readlines()
        with open(HOSTS_PATH, "w") as file:
            for line in lines:
                if not any(website in line for website in WEBSITES):
                    file.write(line)
        print("Unblocked all websites.")
    except PermissionError:
        print("Error: Run the script with administrative privileges.")
    except Exception as e:
        print(f"Error unblocking websites: {e}")

def main():
    """Main function to schedule website blocking/unblocking based on time."""
    if not is_admin():
        print("Please run this script as an administrator.")
        return

    print("Website Blocker by Mr. Sabaz Ali Khan (Ethical Hacker, Pakistan)")
    print("Running... Press Ctrl+C to stop.")

    try:
        while True:
            current_hour = datetime.now().hour
            if BLOCK_START_HOUR <= current_hour < BLOCK_END_HOUR:
                print(f"Blocking websites at {datetime.now()}")
                block_websites()
            else:
                print(f"Unblocking websites at {datetime.now()}")
                unblock_websites()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\nStopping website blocker.")
        unblock_websites()  # Ensure websites are unblocked on exit

if __name__ == "__main__":
    main()