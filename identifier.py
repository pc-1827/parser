import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageOps
import os

banks = ["HDFC", "Kotak"]

def bankIdentifier(filePath):
    data = imageDataExtractor(filePath)
    for bank in banks:
        if bank.lower() in data.lower():
            return bank
    return "Bank name not found"


def imageDataExtractor(filePath):
    # Convert first page of PDF to image
    pages = convert_from_path(filePath, first_page=0, last_page=1)
    first_page_image = pages[0]

    # Get image dimensions
    width, height = first_page_image.size

    # Crop the image to get the top 1/4th
    crop_area = (0, 0, width, height // 4)
    cropped_image = first_page_image.crop(crop_area)

    # Convert image to grayscale
    gray_image = ImageOps.grayscale(cropped_image)

    # Increase contrast
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2)  # Increase contrast

    # Save the preprocessed image temporarily
    image_path = 'temp_image.png'
    enhanced_image.save(image_path, 'PNG')

    # Perform OCR on the image
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Path to Tesseract executable on Ubuntu
    text = pytesseract.image_to_string(Image.open(image_path))

    # Clean up temporary image file
    os.remove(image_path)

    return text
