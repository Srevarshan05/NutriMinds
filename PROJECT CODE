import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QLabel, QFileDialog, QDialog, QComboBox)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from groq import Groq
from paddleocr import PaddleOCR
import csv

# Initialize OCR and Groq
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # English OCR support
client = Groq(api_key="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")

# Global variables
image_path = None  # Placeholder for the nutritional image path
csv_path = 'data.csv'  # Not used for medical data now
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

def process_image_and_csv(image_path, csv_path):
    """
    Processes a nutritional image, sending data to the Groq API for analysis.
    """
    if not image_path:
        return "Error: No image path provided!", "", ""
    try:
        # Extract text from the image
        cleaned_text = extract_and_clean_text(image_path)
        extracted_text = ", ".join(cleaned_text)

        # Prepare Groq prompt for nutritional data
        prompt = f"""
        I am using OCR to extract the Nutritional information from the Food pack labels. 
        I need you to refine the text: {extracted_text}. Just return the nutritional facts and Ingredients. 
        Based on the ingredients, what is the Food name? No other words.
        """

        # Send the prompt to Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are a professional medical advisor."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300,
            top_p=1,
            stream=False
        )
        refined_text = response.choices[0].message.content
        log_refined_text(refined_text)
        return refined_text, "", ""
    except Exception as e:
        return f"Error occurred: {e}", "", ""

class NutritionalAnalysisApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Overall green theme for the background
        self.setStyleSheet("background-color: #e0f7e9;")
        self.setWindowTitle("Nutritional & Medical Analysis")
        self.setGeometry(100, 100, 1000, 700)

        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Nutritional & Medical Analysis Tool")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2e7d32;")
        main_layout.addWidget(title)

        # Create a horizontal layout for the Nutritional and Medical sections
        top_layout = QHBoxLayout()

        # Left Column: Nutritional Section
        nutritional_layout = QVBoxLayout()
        nutritional_title = QLabel("Nutritional Data")
        nutritional_title.setFont(QFont("Arial", 18, QFont.Bold))
        nutritional_title.setAlignment(Qt.AlignCenter)
        nutritional_title.setStyleSheet("color: #2e7d32;")
        nutritional_layout.addWidget(nutritional_title)

        self.upload_button = QPushButton("Upload Nutritional Image")
        self.upload_button.setStyleSheet("background-color: #66bb6a; color: white; padding: 10px;")
        self.upload_button.clicked.connect(self.upload_image)
        nutritional_layout.addWidget(self.upload_button)

        # Label to display the uploaded nutritional image
        self.image_display_label = QLabel("Uploaded Nutritional Image will be displayed here.")
        self.image_display_label.setAlignment(Qt.AlignCenter)
        self.image_display_label.setFixedSize(400, 400)
        self.image_display_label.setStyleSheet("border: 2px dashed #2e7d32;")
        nutritional_layout.addWidget(self.image_display_label)

        self.analyze_button = QPushButton("Analyze Nutritional Data")
        self.analyze_button.setStyleSheet("background-color: #66bb6a; color: white; padding: 10px;")
        self.analyze_button.clicked.connect(self.analyze_data)
        nutritional_layout.addWidget(self.analyze_button)

        self.refined_text_box = QTextEdit()
        self.refined_text_box.setPlaceholderText("Nutritional Analysis Output")
        self.refined_text_box.setFont(QFont("Arial", 12))  # Increased font size

        nutritional_layout.addWidget(self.refined_text_box)

        top_layout.addLayout(nutritional_layout)

        # Right Column: Medical Report Section
        medical_layout = QVBoxLayout()
        medical_title = QLabel("Medical Report")
        medical_title.setFont(QFont("Arial", 18, QFont.Bold))
        medical_title.setAlignment(Qt.AlignCenter)
        medical_title.setStyleSheet("color: #2e7d32;")
        medical_layout.addWidget(medical_title)

        self.upload_medical_btn = QPushButton("Upload Medical Report")
        self.upload_medical_btn.setStyleSheet("background-color: #66bb6a; color: white; padding: 10px;")
        self.upload_medical_btn.clicked.connect(self.process_medical_report)
        medical_layout.addWidget(self.upload_medical_btn)

        self.medical_text_box = QTextEdit()
        self.medical_text_box.setPlaceholderText("Medical Report Analysis Output")
        self.medical_text_box.setFont(QFont("Arial", 12))  # Increased font size
        medical_layout.addWidget(self.medical_text_box)

        top_layout.addLayout(medical_layout)

        main_layout.addLayout(top_layout)

        # Combined Evaluation Section
        combined_title = QLabel("Combined Evaluation")
        combined_title.setFont(QFont("Arial", 18, QFont.Bold))
        combined_title.setAlignment(Qt.AlignCenter)
        combined_title.setStyleSheet("color: #2e7d32;")
        main_layout.addWidget(combined_title)
        
        # Layout for dropdowns (model and language)
        dropdown_layout = QHBoxLayout()
        
        # Model dropdown
        model_label = QLabel("Select Model: ")
        model_label.setFont(QFont("Arial", 14))
        model_label.setStyleSheet("color: #2e7d32;")
        dropdown_layout.addWidget(model_label)
        
        self.model_dropdown = QComboBox()
        self.model_dropdown.addItems([
            "llama-3.3-70b-versatile",
            "deepseek-r1-distill-llama-70b",
            "llama-3.2-1b-preview",
            "qwen-2.5-32b"
        ])
        dropdown_layout.addWidget(self.model_dropdown)
        
        # Language dropdown
        lang_label = QLabel("Select Language: ")
        lang_label.setFont(QFont("Arial", 14))
        lang_label.setStyleSheet("color: #2e7d32;")
        dropdown_layout.addWidget(lang_label)
        
        self.language_dropdown = QComboBox()
        self.language_dropdown.addItems([
            "English",
            "Tamil",
            "Hindi"
        ])
        dropdown_layout.addWidget(self.language_dropdown)
        
        main_layout.addLayout(dropdown_layout)

        self.combined_button = QPushButton("Evaluate Combined Data")
        self.combined_button.setStyleSheet("background-color: #66bb6a; color: white; padding: 10px;")
        self.combined_button.clicked.connect(self.evaluate_combined)
        main_layout.addWidget(self.combined_button)

        self.setLayout(main_layout)

    def upload_image(self):
        global image_path
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Nutritional Image", "", "Image Files (*.jpg *.png *.jpeg)")
        if file_name:
            image_path = file_name
            pixmap = QPixmap(file_name)
            # Scale the image to fit nicely in the label
            self.image_display_label.setPixmap(pixmap.scaled(self.image_display_label.size(), Qt.KeepAspectRatio))

    def analyze_data(self):
        if not image_path:
            self.refined_text_box.setText("Please upload a nutritional image first.")
            return
        refined_text, _, _ = process_image_and_csv(image_path, csv_path)
        self.refined_text_box.setText(refined_text)
    
    def process_medical_report(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Medical Report Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            extracted_text = extract_and_clean_text(file_path)
            # Prepare Groq prompt for Medical Report
            medical_prompt = f"""
            I am using OCR to extract the text from a medical report. 
            Refine the text: {extracted_text}, remove any noise, and provide a clear summary of the medical findings. 
            Just return the important medical details and diagnosis if available, no extra words.
            """
            # Send to Groq for Refinement
            medical_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "You are a professional medical advisor."},
                          {"role": "user", "content": medical_prompt}],
                temperature=0.7,
                max_tokens=300,
                top_p=1,
                stream=False
            )
            medical_refined_text = medical_response.choices[0].message.content
            self.medical_text_box.setText(medical_refined_text)

    def evaluate_combined(self):
        nutritional_text = self.refined_text_box.toPlainText().strip()
        medical_text = self.medical_text_box.toPlainText().strip()

        if not nutritional_text:
            error_dialog = QDialog(self)
            error_dialog.setWindowTitle("Error")
            error_layout = QVBoxLayout()
            error_label = QLabel("Please analyze nutritional data first.")
            error_layout.addWidget(error_label)
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(error_dialog.close)
            error_layout.addWidget(close_btn)
            error_dialog.setLayout(error_layout)
            error_dialog.exec_()
            return
        if not medical_text:
            error_dialog = QDialog(self)
            error_dialog.setWindowTitle("Error")
            error_layout = QVBoxLayout()
            error_label = QLabel("Please process medical report first.")
            error_layout.addWidget(error_label)
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(error_dialog.close)
            error_layout.addWidget(close_btn)
            error_dialog.setLayout(error_layout)
            error_dialog.exec_()
            return

        # Get the selected model and language from the dropdowns
        selected_model = self.model_dropdown.currentText()
        selected_language = self.language_dropdown.currentText()

        next_prompt = f"""
        Dear User,

        Based on the extracted text from your food pack labels: {nutritional_text},
        and the details from your medical report: {medical_text},
        please evaluate the ingredients for safety.
        Provide a short recommendation on whether the food is safe to consume,
        including the safe quantity for intake if applicable.
        If the food is not recommended, briefly explain why it should be avoided.

        Please provide the response in the following format:

        1. First, a short and clear recommendation in **English**.
        2. After that, a short and clear recommendation in **{selected_language}** that corresponds to the English response.
        """
        final_response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "system", "content": "You are a professional medical advisor."},
                      {"role": "user", "content": next_prompt}],
            temperature=0.7,
            max_tokens=400,
            top_p=1,
            stream=False
        )
        final_output = final_response.choices[0].message.content

        # Create a pop-up dialog to display the combined evaluation
        dialog = QDialog(self)
        dialog.setWindowTitle("Combined Evaluation")
        dialog_layout = QVBoxLayout()
        
        output_text = QTextEdit()
        output_text.setReadOnly(True)
        output_text.setText(final_output)
        output_text.setFont(QFont("Arial", 12))  # Font size increased

        dialog_layout.addWidget(output_text)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        dialog_layout.addWidget(close_button)
        
        dialog.setLayout(dialog_layout)
        dialog.resize(600, 400)
        
        # Center the dialog relative to the main window
        main_rect = self.geometry()
        dialog.move(main_rect.center() - dialog.rect().center())
        
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = NutritionalAnalysisApp()
    main_window.show()
    sys.exit(app.exec_())
