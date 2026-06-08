import cv2
import mediapipe as mp
import time
import threading
import keyboard
from math import dist # ear = landmarks
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from cvzone.PlotModule import LivePlot

class CameraStream:
    """Reads frames from a camera in a background thread to avoid blocking."""
    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)  
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.frame = None
        self.lock = threading.Lock()
        self.running = True

        self._thread = threading.Thread(target=self._reader, daemon=True)
        self._thread.start()

        print("Camera was turned as: ", self.cap.isOpened())

    def _reader(self):
        while self.running:
            success, frame = self.cap.read()
            if success:
                with self.lock:
                    self.frame = frame

    def read(self):
        with self.lock:
            return self.frame is not None, (
                self.frame.copy() 
                if self.frame is not None else None
            )

    def release(self):
        self.running = False
        self._thread.join()   
        self.cap.release()

MODEL_PATH = "models/face_landmarker.task"

BaseOptions           = python.BaseOptions
FaceLandmarker        = vision.FaceLandmarker
FaceLandmarkerOptions = vision.FaceLandmarkerOptions
VisionRunningMode     = vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_faces=1,
    output_face_blendshapes=True
)

detector = FaceLandmarker.create_from_options(options)

EYE_VERTICALS  = [(160, 144), (159, 145), (158, 153)]
EYE_HORIZONTAL = (33, 133)