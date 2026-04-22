# Antigravity Session Logs - KZTaxChecker

## Session 1: Initial Setup
**My prompt:** You are an AI developer. I am the architect. I do NOT write code manually. Build KZTaxChecker - a tool to check Kazakhstan ESF (electronic invoices) for tax risks. Tech stack: Streamlit, Google Gemini API, pdfplumber Create file: requirements.txt with these lines: streamlit google-generativeai pdfplumber python-dotenv Create file: app.py with: - Streamlit UI with file uploader for PDF - Title: "KZTaxChecker - ESF Tax Risk Analyzer for Kazakhstan" - Call analyzer.py function to process the PDF - Display results as color cards (red=error, yellow=warning, green=ok) - Button to download JSON report Create file: analyzer.py with: - Function extract_text_from_pdf(pdf_file) using pdfplumber - Function call_gemini(text) using google.generativeai - System prompt: "You are a tax expert in Tax Code of Kazakhstan. Analyze ESF invoice for errors." - Return dummy JSON for now Write complete code. No placeholders.

**AI response:** Created app.py, analyzer.py, requirements.txt
**My action:** Saved files, installed dependencies

## Session 2: Added TXT file support
**My prompt:** "Update app.py and analyzer.py to support both PDF and TXT files"
**AI response:** Updated file uploader and text extraction
**My action:** Saved updated files

## Session 3: Added Tax Code validation (CURRENT)
**My prompt:** Now update the system prompt in analyzer.py to implement REAL Kazakhstan Tax Code validation rules.

Replace the current dummy analysis with these specific checks:

1. BIN (БИН) validation:
   - Must be exactly 12 digits
   - Must pass checksum algorithm (implement checksum function)

2. VAT rate validation:
   - Must be one of: "12%", "0%", or "без НДС"
   - If anything else → ERROR

3. Date validation:
   - Cannot be in the future
   - Must be valid date format

4. VAT amount calculation check:
   - If VAT rate = 12%, then VAT = Total * 12/112
   - If calculated VAT doesn't match given VAT → WARNING

5. RNN format: must be 12 digits starting with 600, 500, 400, or 300

Return JSON with:
{
  "overall_risk": "HIGH" if any ERROR, "MEDIUM" if any WARNING, "LOW" if all pass,
  "checks": [
    {
      "field": "BIN продавца",
      "status": "PASS" or "ERROR" or "WARNING", 
      "message": "description",
      "recommendation": "fix instruction"
    }
  ]
}

Update app.py to show the overall_risk as colored banner (RED=HIGH, YELLOW=MEDIUM, GREEN=LOW).
**AI response:** updated the system promp
**My action:** Saved updated code, tested successfully