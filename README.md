# RealGuard: Real-Time Human Detection and Recognition

This Python application allows you to perform real-time human detection and recognition of faces, eyes, and smiles in a live video feed using OpenCV, PyAutoGUI, and PyQt5. It also detects and draws bounding boxes for the lower body, upper body, and full body. This program is suitable for monitoring and surveillance applications.

## Prerequisites

Before running the program, make sure you have the following prerequisites installed:

- Python 3.x
- OpenCV (cv2)
- PyQt5
- NumPy
- PyAutoGUI

You can install these dependencies using pip:

```bash
pip install opencv-python-headless pyqt5 numpy pyautogui
```
# Usage
  - Clone this repository or download the source code.
  - Open your terminal or command prompt.
  - Navigate to the project directory.
  - Run the program:
    ```bash
    py rt.py
    ```
The application will launch, displaying a live video feed of your selected window (e.g., a web camera or a specific application window). The program will detect and draw bounding boxes around faces, eyes, and smiles within the faces, as well as lower body, upper body, and full body.

# Customization

You can customize the program to work with different windows or regions. Modify the `window_title variable` to match the title of the window you want to capture.

# Notes

 - If you encounter any errors or issues, make sure you have the required dependencies installed.
 - For optimal results, use a well-lit environment for the video feed.
 -  This program continuously captures and analyzes frames from the selected window. To stop the program, close the window or terminate the script.

# License

This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to use and modify this code for your own projects, but give credit.
