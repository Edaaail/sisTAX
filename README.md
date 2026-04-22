# KZTaxChecker - ESF Tax Risk Analyzer for Kazakhstan

KZTaxChecker is a lightweight Streamlit application that analyzes Kazakhstan ESF (electronic invoice) files for common tax risks and compliance issues. It supports PDF and TXT files and generates an easy-to-read risk report.

## Features

- Upload PDF or TXT files with ESF invoices
- AI-powered validation against Tax Code of Kazakhstan
- Color-coded risk assessment (HIGH / MEDIUM / LOW)
- BIN, VAT, date, and RNN checks
- Export JSON report
- Simple local web interface with Streamlit

## Installation

### 1. Clone or download this folder

Download the project files or clone the repository.

### 2. Install dependencies

```bash
pip install -r requirements.txt
````

### 3. Get a free API key

Create a free Google AI Studio API key:

[https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 4. Create `.env` file

Create a file named `.env` in the project folder:

```env
GOOGLE_API_KEY=your_key_here
```

## Usage

Run the application:

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in your terminal (usually `http://localhost:8501`).

## How It Works

1. Upload an ESF invoice file (`.pdf` or `.txt`)
2. Click analyze
3. Receive a color-coded risk report
4. Review validation checks
5. Download JSON results

## Risk Levels

* **HIGH** – One or more critical errors found
* **MEDIUM** – Warnings found, review recommended
* **LOW** – All checks passed

## Example Checks

* BIN format and checksum
* VAT rate validation
* Future or invalid invoice dates
* VAT amount mismatch
* RNN format validation

## Tech Stack

* Streamlit
* Google Gemini API
* pdfplumber
* python-dotenv

## Notes

* Best results depend on readable invoice text.
* Scanned image PDFs may require OCR before upload.
* This tool assists review and does not replace professional tax advice.

## License

Educational / internal use.

```
```
