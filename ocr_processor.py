from paddleocr import PaddleOCR
import csv

# Initialize OCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # English OCR support
log_csv_path = 'refined_text_log.csv'  # CSV file for logging refined text

def log_refined_text(refined_text):
    """
    Logs the refined OCR-extracted text into a CSV file.
    """
    with open(log_csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([refined_text])

def extract_and_clean_text(image_path):
    """
    Extracts text from an image using OCR and cleans it.
    """
    results = ocr.ocr(image_path, cls=True)
    cleaned_text = []
    for line in results[0]:
        text = line[1][0]
        if len(text) >= 3 and text.isprintable():
            cleaned_text.append(text)
    return cleaned_text
