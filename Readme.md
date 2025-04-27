## AI Arabic Namer
it renames your files (PDFs, PNGs, JPGs) in arabic names with the power of LLM you could give a prompt of what type of names you want it to be

## To use it you need to download the next requirements
### 1. python 3.6+
### 2. Tesseract OCR

- ** Windows**:
  - Download Tesseract OCR GitHub
  - Install to `C:\Program Files\Tesseract-OCR`.
  - Add to PATH: `C:\Program Files\Tesseract-OCR`.
  - Arabic support: Download `ara.traineddata` from tessdata, place in `C:\Program Files\Tesseract-OCR\tessdata`.
  - Verify: `tesseract --version` and `tesseract --list-langs` (should list `ara`).
- **Linux**: `sudo apt-get install tesseract-ocr tesseract-ocr-ara`
- **Mac**: `brew install tesseract tesseract-lang`

### 3. Poppler (for pdf2image Library)

- **Windows**:
  - Download: Poppler GitHub.
  - Add `bin` to PATH (e.g., `C:\poppler-23.01.0\Library\bin`).
- **Linux**: `sudo apt-get install poppler-utils`
- **Mac**: `brew install poppler`

### 4. Ollama

- Install: ollama.ai.
- Pull model: `ollama pull qwen2.5:7b-instruct-q4_0`. (you can use any LLM you want from here([Ollama Models](https://ollama.com/search)) just make sure it's good at arabic)
- Run: `ollama run qwen2.5:7b-instruct-q4_0`.


## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/your-username/house-scans-renamer.git
   cd house-scans-renamer
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```


## Configuration

Edit `namer.py`:

- `INPUT_FOLDER`: Path to scans (e.g., `"C:\\scanned-document"`).
- `OUTPUT_FOLDER`: Path for renamed files (e.g., `"C:\\Rename-scanned-document"`).
- `pytesseract.pytesseract.tesseract_cmd`: Tesseract path (e.g., `r"C:\Program Files\Tesseract-OCR\tesseract.exe"`).
- `OLLAMA_MODEL`: Your Ollama model (e.g., `"qwen2.5:7b-instruct-q4_0"`).
- To customize naming, edit the prompt in `query_ollama` (e.g., change `[CompanyName] [Date]` to `[Date] [CompanyName]`).

## Contributing 

Fork and contribute! Idea Add a UI.

- Fork the repo.
- Branch: `git checkout -b feature/ui`.
- Commit: `git commit -m "Add UI"`.
- Push: `git push origin feature/ui`.
- Open a pull request.
