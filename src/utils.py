import cv2
import numpy as np
import math

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red


def overlay_image(
    base_image: np.ndarray,
    overlay_image: np.ndarray,
    x: int,
    y: int,
    width=int | None,
    height=int | None,
):
    """
    Overlays an image on top of another image at specified coordinates with optional resizing.
    Both images should be in BGR format (default OpenCV format).
    """
    # Create a copy of the base image
    result = base_image.copy()

    # Make a copy of overlay image
    overlay = overlay_image.copy()

    # Convert the overlay from BGR(A) to RGB(A)
    if overlay_image.shape[-1] == 4:
        # For BGRA images, convert only the BGR part
        overlay = cv2.cvtColor(overlay_image[:, :, :3], cv2.COLOR_BGR2RGB)
        # Add alpha channel back
        overlay = np.dstack((overlay, overlay_image[:, :, 3]))
    else:
        overlay = cv2.cvtColor(overlay_image, cv2.COLOR_BGR2RGB)

    # Resize overlay if dimensions are specified
    if width is not None and height is not None:
        overlay = cv2.resize(overlay, (width, height))

    # Get dimensions
    h, w = overlay.shape[:2]
    base_h, base_w = base_image.shape[:2]

    # Calculate valid coordinates
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(base_w, x + w), min(base_h, y + h)

    # Check if the overlay is completely outside the image
    if x2 <= x1 or y2 <= y1:
        return result

    # Calculate overlay offset (for cases where overlay is partially outside)
    overlay_x1 = abs(min(0, x))
    overlay_y1 = abs(min(0, y))
    overlay_x2 = overlay_x1 + (x2 - x1)
    overlay_y2 = overlay_y1 + (y2 - y1)

    # Extract the alpha channel if it exists
    if overlay.shape[-1] == 4:  # With alpha channel
        overlay_region = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2]
        alpha = overlay_region[:, :, 3] / 255.0
        overlay_bgr = overlay_region[:, :, :3]

        # Blend each color channel
        for c in range(3):
            result[y1:y2, x1:x2, c] = (
                alpha * overlay_bgr[:, :, c] + (1 - alpha) * result[y1:y2, x1:x2, c]
            )
    else:  # No alpha channel
        result[y1:y2, x1:x2] = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2]

    return result


def normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int, image_height: int
) -> tuple[int, int]:
    x_px = min(math.floor(normalized_x * image_width), image_width - 1)
    y_px = min(math.floor(normalized_y * image_height), image_height - 1)
    return x_px, y_px


def visualize_detection(image, detection_result) -> np.ndarray:
    """Draws bounding boxes and keypoints on the input image and return it.
    Args:
      image: The input RGB image.
      detection_result: The list of all "Detection" entities to be visualize.
    Returns:
      Image with bounding boxes.
    """
    annotated_image = image.copy()
    height, width, _ = image.shape

    for detection in detection_result.detections:
        # Draw bounding_box
        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        cv2.rectangle(annotated_image, start_point, end_point, TEXT_COLOR, 3)

        # Draw keypoints
        for keypoint in detection.keypoints[:4]:
            keypoint_px = normalized_to_pixel_coordinates(
                keypoint.x, keypoint.y, width, height
            )
            color, thickness, radius = (0, 255, 0), 2, 2
            cv2.circle(annotated_image, keypoint_px, thickness, color, radius)

        # Draw label and score
        category = detection.categories[0]
        category_name = category.category_name
        category_name = "" if category_name is None else category_name
        probability = round(category.score, 2)
        result_text = category_name + " (" + str(probability) + ")"
        text_location = (MARGIN + bbox.origin_x, MARGIN + ROW_SIZE + bbox.origin_y)
        cv2.putText(
            annotated_image,
            result_text,
            text_location,
            cv2.FONT_HERSHEY_PLAIN,
            FONT_SIZE,
            TEXT_COLOR,
            FONT_THICKNESS,
        )

    return annotated_image
