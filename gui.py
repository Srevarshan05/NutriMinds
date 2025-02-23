import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, QComboBox, QDialog
)
from PyQt5.QtGui import QFont
from .analysis import process_image_and_csv, process_medical_report, evaluate_food_safety

class NutritionMedicalAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Nutritional & Medical Analysis")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Image Upload Button (Food Label)
        self.image_label = QLabel("Select Food Label Image:")
        layout.addWidget(self.image_label)
        self.image_button = QPushButton("Upload Food Label")
        self.image_button.clicked.connect(self.upload_food_image)
        layout.addWidget(self.image_button)

        # Image Upload Button (Medical Report)
        self.report_label = QLabel("Select Medical Report Image:")
        layout.addWidget(self.report_label)
        self.report_button = QPushButton("Upload Medical Report")
        self.report_button.clicked.connect(self.upload_medical_report)
        layout.addWidget(self.report_button)

        # Model Selection
        self.model_label = QLabel("Select AI Model:")
        layout.addWidget(self.model_label)
        self.model_dropdown = QComboBox()
        self.model_dropdown.addItems(["llama-3.3-70b-versatile", "llama-3.2-1b-preview", "deepseek-r1-distill-llama-70b","qwen-2.5-32b"])
        layout.addWidget(self.model_dropdown)

        # Language Selection
        self.language_label = QLabel("Select Language for Recommendation:")
        layout.addWidget(self.language_label)
        self.language_dropdown = QComboBox()
        self.language_dropdown.addItems(["English", "French", "Spanish", "German", "Hindi"])
        layout.addWidget(self.language_dropdown)

        # Analyze Button
        self.analyze_button = QPushButton("Analyze & Evaluate")
        self.analyze_button.clicked.connect(self.analyze_data)
        layout.addWidget(self.analyze_button)

        # Output Display
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Arial", 12))
        layout.addWidget(self.result_text)

        self.setLayout(layout)

        # Variables for file paths
        self.food_image_path = None
        self.medical_report_path = None

    def upload_food_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Food Label Image", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if file_path:
            self.food_image_path = file_path
            self.image_label.setText(f"Selected: {os.path.basename(file_path)}")

    def upload_medical_report(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Medical Report", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if file_path:
            self.medical_report_path = file_path
            self.report_label.setText(f"Selected: {os.path.basename(file_path)}")

    def analyze_data(self):
        if not self.food_image_path or not self.medical_report_path:
            self.result_text.setText("Error: Please upload both food label and medical report images.")
            return

        selected_model = self.model_dropdown.currentText()
        selected_language = self.language_dropdown.currentText()

        # Process food label
        self.result_text.setText("Processing food label image...")
        nutritional_text, _, _ = process_image_and_csv(self.food_image_path, "")

        # Process medical report
        self.result_text.append("\nProcessing medical report...")
        medical_text = process_medical_report(self.medical_report_path)

        # Evaluate food safety
        self.result_text.append("\nEvaluating food safety...")
        final_output = evaluate_food_safety(nutritional_text, medical_text, selected_model, selected_language)

        # Show results in a pop-up
        self.show_result_popup(final_output)

    def show_result_popup(self, final_output):
        dialog = QDialog(self)
        dialog.setWindowTitle("Evaluation Result")
        dialog_layout = QVBoxLayout()

        output_text = QTextEdit()
        output_text.setReadOnly(True)
        output_text.setText(final_output)
        output_text.setFont(QFont("Arial", 12))

        dialog_layout.addWidget(output_text)
        dialog.setLayout(dialog_layout)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NutritionMedicalAnalyzer()
    window.show()
    sys.exit(app.exec_())
