# SystemLogger

SystemLogger is a Python application for logging system information, keyboard events, and mouse activities on Windows operating systems. It provides detailed insights into the system's CPU, memory, and disk usage, while also recording real-time keyboard keystrokes and mouse interactions.

## Features

- **System Information:** Retrieve detailed system information including CPU, memory, and disk usage.
- **Keyboard Logging:** Record keyboard events such as key presses, including special keys like Enter and Space.
- **Mouse Logging:** Monitor mouse movements, clicks, and scroll actions.
- **Upload to Dropbox:** Automatically upload logs to Dropbox for remote access and backup.
- 
   **ALSO IP ADDRESS**

## Installation

1. Download and install Python for Windows from [python.org](https://www.python.org/downloads/).
   
2. Open a command prompt and navigate to the directory where SystemLogger is cloned or downloaded.
   
3. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```
4. Set up a Dropbox account and generate an access token for API usage.

## Usage

  Run the SystemLogger application:
  
   ```bash
   python system_logger.py
   ```

  SystemLogger will start logging keyboard events and mouse activities in real-time. Logs will be uploaded to Dropbox periodically.

  Monitor the logs by accessing the Dropbox folder specified in the configuration.


## Configuration

  Modify the dropbox_token variable in the system_logger.py file with your Dropbox access token.
    
  Adjust the interval variable to set the frequency of log uploads (in seconds).

## Bonus

 If you need this code run in background contact ratheeshrao100@gmail.com
