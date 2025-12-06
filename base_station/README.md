# Base Station Control Panel

The **Base Station** is the mission control software for the Rover. It provides a GUI to send commands, switch autonomous modes, and view status updates.

## Structure
* **`run_station.py`**: The main entry point script.
* **`gui/`**: Contains the Tkinter source code, button logic, and serial handlers.

## How to Run

1.  **Dependencies**:
    Ensure you have Python 3 and the required libraries:
    ```bash
    pip3 install pyserial pillow
    # Tkinter is usually included with Python
    ```

2.  **Launch**:
    From this directory, run:
    ```bash
    python3 run_station.py
    ```

3.  **Usage**:
    * Select the correct COM port (e.g., `/dev/ttyUSB0` or `COM3`) and click **Refresh**.
    * Choose a mode (Manual, Auto, etc.).
    * Use **WASD** keys for manual driving.