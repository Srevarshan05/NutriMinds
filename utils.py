import csv
import os

log_csv_path = 'refined_text_log.csv'

def log_refined_text(refined_text):
    """
    Logs the refined OCR-extracted text into a CSV file.
    """
    with open(log_csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([refined_text])

def check_file_exists(file_path):
    """
    Checks if a file exists.
    """
    return os.path.exists(file_path)

def read_csv(file_path):
    """
    Reads a CSV file and returns its content as a list of rows.
    """
    if not check_file_exists(file_path):
        return []
    
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        return list(reader)

def save_to_csv(file_path, data):
    """
    Saves a list of data to a CSV file.
    """
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def clean_text(text):
    """
    Cleans extracted text by removing unnecessary spaces and non-printable characters.
    """
    return ''.join(c for c in text if c.isprintable()).strip()
