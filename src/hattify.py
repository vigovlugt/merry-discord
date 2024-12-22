import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
from utils import overlay_image, visualize_detection


HAT_FILE = "assets/christmas-hat.png"


def hattify(image: mp.Image) -> np.ndarray:
    hat_image = cv2.imread(HAT_FILE, cv2.IMREAD_UNCHANGED)
    hat_width_ratio = hat_image.shape[1] / hat_image.shape[0]

    # Detect face
    # wget -q -O detector.tflite -q https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite
    base_options = python.BaseOptions(model_asset_path="assets/detector.tflite")
    options = vision.FaceDetectorOptions(base_options=base_options)
    detector = vision.FaceDetector.create_from_options(options)
    detection_result = detector.detect(image)

    annotated_image = np.copy(image.numpy_view())

    if len(detection_result.detections) == 0:
        return annotated_image

    detection = detection_result.detections[0]

    for detection in detection_result.detections:
        bbox = detection.bounding_box

        y1 = bbox.origin_y - bbox.height
        x1 = bbox.origin_x

        left_eye = detection.keypoints[0]
        right_eye = detection.keypoints[1]
        middle_x = (left_eye.x + right_eye.x) / 2

        # Flip the hat if the face is flipped
        if middle_x > 0.5:
            hat_image = cv2.flip(hat_image, 1)
            x1 = x1 - int(bbox.width * 0.4)

        # Overlay the hat on the image
        annotated_image = overlay_image(
            annotated_image,
            hat_image,
            x1,
            y1 + int(bbox.height * 0.2),
            width=int(bbox.width * hat_width_ratio),
            height=bbox.height,
        )

    rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

    return rgb_annotated_image
