import os
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import shutil
import requests
import json
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Configuration
INPUT_FOLDER = "D:/Family/father's scans"  # Replace with your input folder path (e.g., "C:\\HouseScans")
OUTPUT_FOLDER = "D:/Family/father's scans named"  # Replace with your output folder path (e.g., "C:\\RenamedHouseFiles")
SUPPORTED_EXTENSIONS = (".pdf", ".png", ".jpg", ".jpeg")
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Default Ollama API endpoint
OLLAMA_MODEL = "qwen2.5:7b-instruct-q4_0"  # Replace with your model (e.g., "mistral" or "gemma")

def ensure_output_folder():
    """Create output folder if it doesn't exist."""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

def extract_text_from_pdf(file_path):
    """Extract text directly from a PDF file using PyPDF2."""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
            return text.strip()
    except Exception as e:
        print(f"Error extracting text directly from PDF {file_path}: {e}")
        return ""

def extract_text_from_image(file_path):
    """Extract text from an image file using OCR with Arabic support."""
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang="ara")
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from image {file_path}: {e}")
        return ""

def extract_text_from_pdf_ocr(file_path):
    """Convert PDF to images and extract text using OCR with Arabic support."""
    try:
        images = convert_from_path(file_path, dpi=300)  # Higher DPI for better OCR
        text = ""
        for image in images:
            extracted_text = pytesseract.image_to_string(image, lang="ara")
            if extracted_text:
                text += extracted_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF via OCR {file_path}: {e}")
        return ""

def query_ollama(text):
    """Query Ollama to generate an Arabic file name based on text."""
    prompt = (
        "You are an assistant that generates Arabic file names for house-building documents. "
        "Read the following text from a document and identify the company name, which is typically at the top in the first few lines. "
        "If the company name is in English, transliterate or translate it to Arabic (e.g., 'LingTechSystem' to 'لينغ_تك_سيستم'). "
        "Create a concise file name using the company name in Arabic. "
        "Include a date (e.g., 2025-04-15) if present in the text, or use today's date (2025-04-26). "
        "Format the name as: [CompanyName] [Date], with a space between the company name and date, "
        "and ensure the company name itself has spaces if needed (e.g., المقاولون العرب 2025-04-26). "
        "Return only the name without extension. Text: \n" + (text if text else "No text extracted")
    )

    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        result = json.loads(response.text)
        ollama_response = result.get("response", "")
        print(f"Ollama response: {ollama_response}")  # Log Ollama's response
        if not ollama_response:
            raise ValueError("Ollama returned an empty response")
        return ollama_response
    except Exception as e:
        print(f"Error querying Ollama: {e}")
        raise

def suggest_file_name(text, original_file):
    """Suggest a new file name using Ollama."""
    # Query Ollama for the file name
    new_name = query_ollama(text)
    # Ensure the name is filesystem-safe while preserving spaces
    # Allow Arabic characters, numbers, spaces, hyphens, and underscores
    new_name = "".join(c for c in new_name if c.isalnum() or c in (" ", "-", "_") or ord(c) >= 0x0600)
    # Preserve original extension
    extension = os.path.splitext(original_file)[1].lower()
    return f"{new_name}{extension}"

def process_file(file_path):
    """Process a single file and create a renamed copy."""
    file_name = os.path.basename(file_path)
    extension = os.path.splitext(file_name)[1].lower()

    # Extract text based on file type
    text = ""
    if extension == ".pdf":
        text = extract_text_from_pdf(file_path)  # Try direct extraction first
        if not text:  # Fallback to OCR if direct extraction fails
            text = extract_text_from_pdf_ocr(file_path)
    elif extension in (".png", ".jpg", ".jpeg"):
        text = extract_text_from_image(file_path)

    # Log extracted text for debugging
    print(f"Extracted text from {file_name}: {text[:100]}...")  # First 100 chars

    try:
        # Suggest new file name using Ollama
        new_name = suggest_file_name(text, file_name)
        new_file_path = os.path.join(OUTPUT_FOLDER, new_name)

        # Handle duplicate names by adding a counter
        counter = 1
        base_name, ext = os.path.splitext(new_name)
        while os.path.exists(new_file_path):
            new_name = f"{base_name}_{counter}{ext}"
            new_file_path = os.path.join(OUTPUT_FOLDER, new_name)
            counter += 1

        # Copy the file with the new name
        shutil.copy2(file_path, new_file_path)
        print(f"Renamed: {file_name} -> {new_name}")
    except Exception as e:
        print(f"Failed to rename {file_name}: {e}")

def main():
    """Main function to process all files in the input folder."""
    ensure_output_folder()

    for file_name in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(SUPPORTED_EXTENSIONS):
            process_file(file_path)

if __name__ == "__main__":
    main()