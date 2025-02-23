import os
import sys
from groq import Groq
from .ocr_processor import extract_and_clean_text, log_refined_text

# Debugging: Start of script
print("Starting analysis.py...")

# Check if API key is set
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    print("Error: GROQ_API_KEY is not set! Exiting script.")
    sys.exit(1)
else:
    print("API Key loaded successfully.")

# Initialize Groq client
try:
    client = Groq(api_key=API_KEY)
    print("Groq client initialized successfully.")
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    sys.exit(1)

def process_image_and_csv(image_path, csv_path):
    """
    Processes a nutritional image, sending data to the Groq API for analysis.
    """
    print(f"Processing image: {image_path}")

    if not image_path:
        print("Error: No image path provided!")
        return "Error: No image path provided!", "", ""

    try:
        # Extract text from the image
        print("Extracting text from image...")
        cleaned_text = extract_and_clean_text(image_path)
        extracted_text = ", ".join(cleaned_text)

        # Prepare Groq prompt for nutritional data
        prompt = f"""
        I am using OCR to extract the Nutritional information from the Food pack labels. 
        I need you to refine the text: {extracted_text}. Just return the nutritional facts and Ingredients. 
        Based on the ingredients, what is the Food name? No other words.
        """

        print("Sending request to Groq API...")
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
        print(f"Refined Text from Groq API: {refined_text}")

        log_refined_text(refined_text)
        print("Refined text logged successfully.")
        
        return refined_text, "", ""

    except Exception as e:
        print(f"Error occurred in process_image_and_csv: {e}")
        return f"Error occurred: {e}", "", ""

def process_medical_report(file_path):
    """
    Processes a medical report image, sending data to the Groq API for analysis.
    """
    print(f"Processing medical report: {file_path}")

    try:
        print("Extracting text from medical report...")
        extracted_text = extract_and_clean_text(file_path)

        # Prepare Groq prompt for Medical Report
        medical_prompt = f"""
        I am using OCR to extract the text from a medical report. 
        Refine the text: {extracted_text}, remove any noise, and provide a clear summary of the medical findings. 
        Just return the important medical details and diagnosis if available, no extra words.
        """

        print("Sending request to Groq API for medical report analysis...")
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

        refined_medical_text = medical_response.choices[0].message.content
        print(f"Refined Medical Report: {refined_medical_text}")

        return refined_medical_text

    except Exception as e:
        print(f"Error occurred in process_medical_report: {e}")
        return f"Error occurred: {e}"

def evaluate_food_safety(nutritional_text, medical_text, selected_model, selected_language):
    """
    Evaluates food safety based on the nutritional details and medical history.
    """

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

    print("Sending request to Groq API for food safety evaluation...")
    final_response = client.chat.completions.create(
        model=selected_model,
        messages=[{"role": "system", "content": "You are a professional medical advisor."},
                  {"role": "user", "content": next_prompt}],
        temperature=0.7,
        max_tokens=400,
        top_p=1,
        stream=False
    )

    return final_response.choices[0].message.content

print("Analysis script execution complete!")

if __name__ == "__main__":
    # Test image and CSV processing
    test_image_path = "Boost.jpg"  # Change this to an actual image path
    test_csv_path = "data.csv"  # Change this to an actual CSV path (if needed)

    print("\n--- Running process_image_and_csv() ---")
    result, _, _ = process_image_and_csv(test_image_path, test_csv_path)
    print(f"Processed Nutritional Data:\n{result}")

    # Test medical report processing
    test_medical_report_path = "report2.png"  # Change this to an actual medical report image path

    print("\n--- Running process_medical_report() ---")
    medical_result = process_medical_report(test_medical_report_path)
    print(f"Processed Medical Report:\n{medical_result}")

    # Test food safety evaluation
    selected_model = "llama-3.3-70b-versatile"  # Example model
    selected_language = "French"  # Example language

    print("\n--- Running evaluate_food_safety() ---")
    final_evaluation = evaluate_food_safety(result, medical_result, selected_model, selected_language)
    print(f"Food Safety Evaluation:\n{final_evaluation}")
