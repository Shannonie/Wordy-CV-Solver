import cv2
import numpy as np
from PIL import Image

def pil_to_cv(image: Image.Image) -> np.ndarray:
    """Convert PIL Image → OpenCV format"""
    return np.array(image)

def cv_to_pil(image) -> Image:
    """Convert OpenCV → PIL Image"""
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def preprocess_image(image:Image) -> Image:
    """ Prepare image for OCR:
    - grayscale
    - invert
    - binarize
    - enhance contrast
    """
    gray_img = pil_to_cv(image.convert('L'))
    resized_img = cv2.resize(gray_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # invert (white text on dark → dark text on white)
    resized_img = cv2.bitwise_not(resized_img)
    _, thresh = cv2.threshold(resized_img, 10, 255, cv2.THRESH_BINARY)

    # smooth (reduce aliasing)
    blur_img = cv2.medianBlur(thresh, 3)

    # Morphological operation (clean up noise)
    kernel = np.ones((3, 3), np.uint8)
    final_img = cv2.morphologyEx(blur_img, cv2.MORPH_CLOSE, kernel)
    
    return final_img