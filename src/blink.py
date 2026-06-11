import cv2 
import mediapipe as mp
import time
import threading
import keyboard
from math import dist
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
# from cvzone.PlotModule import LivePlot

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

BLINK_THRESHOLD     = 0.30
PRESS_HOLD_TIME     = 0.0008
RELEASE_HOLD_TIME   = 0.0004
PROCESS_EVERY_N_FRAMES = 2
PLOT_EVERY_N_FRAMES = 4
DISPLAY_WINDOW      = True

blinking         = False
eye_closed_since = None
eye_open_since   = None
frame_count      = 0
last_blink_score = 0.0
last_landmarks   = None

space_held = False

# plotY = LivePlot(640, 360, [0, 60], invert=True)

## It causes delay
# def eye_aspect_ratio(vertical_pairs, horizontal_pair, landmarks, w, h):
#     """this function calculates the Eye Aspect Ratio"""
#     used_points = set()
#     for pair in vertical_pairs:
#         used_points.update(pair)
#     used_points.update(horizontal_pair)

#     landmark_points = {}
#     for idx in used_points:
#         lm = landmarks[idx]
#         landmark_points[idx] = (int(lm.x * w), int(lm.y * h))

#     vertical_sum = sum(
#         dist(landmark_points[top], landmark_points[bottom])
#         for top, bottom in vertical_pairs
#     )
#     horizontal = dist(
#         landmark_points[horizontal_pair[0]],
#         landmark_points[horizontal_pair[1]]
#     )

#     return (vertical_sum / len(vertical_pairs)) / horizontal, landmark_points

cam = CameraStream(0)

while True:
    success, frame = cam.read()
    if not success or frame is None:
        continue

    frame_count += 1
    h, w, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image  = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    frame_timestamp_ms = int(time.perf_counter() * 1000)
    result = detector.detect_for_video(mp_image, frame_timestamp_ms)

    if not (result.face_landmarks and result.face_blendshapes):
        if DISPLAY_WINDOW:
            print("Put the eye on the camera")
            cv2.imshow("BlinkDetection", frame)
            if cv2.waitKey(1) == 27:
                break
        continue

    blendshapes = {
        b.category_name: b.score
        for b in result.face_blendshapes[0]
    }

    blink_score = blendshapes.get("eyeBlinkRight", 0)

    landmarks   = result.face_landmarks[0]

    # _, right_points = eye_aspect_ratio(
    #     EYE_VERTICALS, EYE_HORIZONTAL, landmarks, w, h
    # )

    # for point in right_points.values():
    #     cv2.circle(frame, point, 3, (255, 0, 255), cv2.FILLED)
    # for top, bottom in EYE_VERTICALS: 
    #     cv2.line(frame, right_points[top], right_points[bottom], (0, 255, 0), 2)
    # cv2.line(
    #     frame,
    #     right_points[EYE_HORIZONTAL[0]],
    #     right_points[EYE_HORIZONTAL[1]],
    #     (255, 0, 0), 2
    # )


## This shows the status, whether the eye is open or not in the webcam and the blink score
    # status = "Closed" if blinking else "Opened"
    # cv2.putText(frame, f"BLINK: {blink_score:.3f}", (30, 40),
    #             cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2)
    # cv2.putText(frame, f"Eye: {status}", (30, 80),
    #             cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 2)

    now = time.perf_counter()
            
    if blink_score > BLINK_THRESHOLD:
        eye_open_since = None
        if not blinking:
            if eye_closed_since is None:
                eye_closed_since = now
            elif now - eye_closed_since >= PRESS_HOLD_TIME:
                if not space_held:
                    keyboard.press("space")
                    space_held = True
                blinking = True
                eye_closed_since = None
    else:
        eye_closed_since = None
        if blinking:
            if eye_open_since is None:
                eye_open_since = now
            elif now - eye_open_since >= RELEASE_HOLD_TIME:
                if space_held:
                    keyboard.release("space")
                    space_held = False
                blinking = False
                eye_open_since = None