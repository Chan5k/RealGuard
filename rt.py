import sys
import cv2
import pyautogui
import numpy as np
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class WorkerThread(QThread):
    frame_processed = pyqtSignal(np.ndarray)

    def run(self):
        # Initialize the face and body detection cascade classifiers
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        lowerbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_lowerbody.xml')
        upperbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
        fullbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

        window_title = "Camera"
        while True:
            try:
                window = pyautogui.getWindowsWithTitle(window_title)[0]
                region = (window.left, window.top, window.width, window.height)
                screenshot = pyautogui.screenshot(region=region)
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

                if isinstance(screenshot, np.ndarray):
                    screenshot = cv2.resize(screenshot, (800, 600))

                    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

                    # Detect faces
                    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                    # Draw bounding boxes around detected faces
                    for (x, y, w, h) in faces:
                        cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        # Region of interest for the face
                        roi_gray = gray[y:y + h, x:x + w]
                        roi_color = screenshot[y:y + h, x:x + w]

                        # Detect eyes within the face
                        eyes = eye_cascade.detectMultiScale(roi_gray)
                        for (ex, ey, ew, eh) in eyes:
                            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)
                        
                        # Detect smiles within the face
                        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20, minSize=(25, 25))
                        for (sx, sy, sw, sh) in smiles:
                            cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (255, 0, 0), 2)

                    # Detect lower bodies
                    lowerbodies = lowerbody_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                    for (x, y, w, h) in lowerbodies:
                        cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    # Detect upper bodies
                    upperbodies = upperbody_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                    for (x, y, w, h) in upperbodies:
                        cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 255), 2)

                    # Detect full bodies
                    fullbodies = fullbody_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                    for (x, y, w, h) in fullbodies:
                        cv2.rectangle(screenshot, (x, y), (x + w, y + h), (255, 0, 255), 2)

                    self.frame_processed.emit(screenshot)
            except IndexError:
                pass


class WindowPreview(QMainWindow):
    def __init__(self, num_worker_threads=4):
        QMainWindow.__init__(self)

        self.num_worker_threads = num_worker_threads
        self.worker_threads = []

        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_preview)
        self.timer.start(100)  

    def initUI(self):
        self.setWindowTitle('RealGuard: Real-Time Human Detection and Recognition')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        for _ in range(self.num_worker_threads):
            thread = WorkerThread()
            thread.frame_processed.connect(self.update_label)
            thread.start()
            self.worker_threads.append(thread)

    def update_label(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap(q_image)
        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        for thread in self.worker_threads:
            thread.terminate()
            thread.wait()
        event.accept()

    def update_preview(self):
        pass  # No need to update the preview here

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowPreview(num_worker_threads=4)  # Adjust the number of worker threads as needed
    window.show()
    sys.exit(app.exec_())
