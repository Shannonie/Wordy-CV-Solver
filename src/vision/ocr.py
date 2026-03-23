from PIL import Image
import pytesseract

from vision.preprocessing import preprocess_image

def extract_letter(image:Image) -> str:
    """
    Extract a single character from an image segment using OCR.
    """
    processed_img = preprocess_image(image)

    config="--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = pytesseract.image_to_string(processed_img, lang='eng', config=config).strip().replace("\n", "")

    return text