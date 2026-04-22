# analyzer.py
import os
import re
import json
from io import BytesIO
from datetime import datetime, date

import pdfplumber
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def extract_text_from_file(uploaded_file):
    filename = uploaded_file.name.lower()

    if filename.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore").strip()

    if filename.endswith(".pdf"):
        text = ""
        file_bytes = uploaded_file.read()

        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return text.strip()

    return ""


def normalize_number(value):
    if not value:
        return None

    value = value.replace(" ", "").replace(",", ".")
    nums = re.findall(r"\d+(?:\.\d+)?", value)

    if not nums:
        return None

    try:
        return float(nums[0])
    except:
        return None


def validate_bin_checksum(bin_value):
    if not re.fullmatch(r"\d{12}", bin_value):
        return False

    digits = list(map(int, bin_value))

    weights1 = list(range(1, 13))
    checksum = sum(digits[i] * weights1[i] for i in range(11)) % 11

    if checksum == 10:
        weights2 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]
        checksum = sum(digits[i] * weights2[i] for i in range(11)) % 11

        if checksum == 10:
            checksum = 0

    return checksum == digits[11]


def extract_first(pattern, text, flags=re.IGNORECASE):
    match = re.search(pattern, text, flags)
    if match:
        return match.group(1).strip()
    return None


def parse_date(date_str):
    formats = [
        "%d.%m.%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d/%m/%Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except:
            pass

    return None


def determine_risk(checks):
    has_error = any(c["status"] == "ERROR" for c in checks)
    has_warning = any(c["status"] == "WARNING" for c in checks)

    if has_error:
        return "HIGH"
    if has_warning:
        return "MEDIUM"
    return "LOW"


def call_gemini(text):
    checks = []

    # BIN
    bin_value = extract_first(r"(?:БИН|BIN)[^\d]*(\d{12})", text)

    if not bin_value:
        checks.append({
            "field": "BIN продавца",
            "status": "ERROR",
            "message": "BIN not found.",
            "recommendation": "Add supplier BIN."
        })
    elif validate_bin_checksum(bin_value):
        checks.append({
            "field": "BIN продавца",
            "status": "PASS",
            "message": "Valid BIN.",
            "recommendation": "No action required."
        })
    else:
        checks.append({
            "field": "BIN продавца",
            "status": "ERROR",
            "message": "BIN checksum invalid.",
            "recommendation": "Correct BIN number."
        })

    # VAT Rate
    vat_rate = extract_first(r"(?:НДС|VAT)[^%\n]*?(12%|0%|без НДС)", text)

    if vat_rate:
        checks.append({
            "field": "Ставка НДС",
            "status": "PASS",
            "message": f"Allowed VAT rate: {vat_rate}",
            "recommendation": "No action required."
        })
    else:
        checks.append({
            "field": "Ставка НДС",
            "status": "ERROR",
            "message": "Invalid VAT rate.",
            "recommendation": "Use only 12%, 0%, or без НДС."
        })

    # Date
    raw_date = extract_first(r"(?:Дата|Date)[^\d]*(\d{2}[./-]\d{2}[./-]\d{4}|\d{4}-\d{2}-\d{2})", text)

    if not raw_date:
        checks.append({
            "field": "Дата счета",
            "status": "ERROR",
            "message": "Invoice date not found.",
            "recommendation": "Add valid invoice date."
        })
    else:
        parsed = parse_date(raw_date)

        if not parsed:
            checks.append({
                "field": "Дата счета",
                "status": "ERROR",
                "message": "Invalid date format.",
                "recommendation": "Use DD.MM.YYYY format."
            })
        elif parsed > date.today():
            checks.append({
                "field": "Дата счета",
                "status": "ERROR",
                "message": "Date is in the future.",
                "recommendation": "Correct invoice date."
            })
        else:
            checks.append({
                "field": "Дата счета",
                "status": "PASS",
                "message": "Valid invoice date.",
                "recommendation": "No action required."
            })

    # RNN
    rnn = extract_first(r"(?:РНН|RNN)[^\d]*(\d{12})", text)

    if not rnn:
        checks.append({
            "field": "РНН",
            "status": "ERROR",
            "message": "RNN not found.",
            "recommendation": "Add taxpayer RNN."
        })
    elif rnn.startswith(("600", "500", "400", "300")):
        checks.append({
            "field": "РНН",
            "status": "PASS",
            "message": "Valid RNN format.",
            "recommendation": "No action required."
        })
    else:
        checks.append({
            "field": "РНН",
            "status": "ERROR",
            "message": "Invalid RNN prefix.",
            "recommendation": "Use RNN starting with 600/500/400/300."
        })

    # VAT Amount
    total_raw = extract_first(r"(?:Итого|Total)[^\d]*(\d+[ ,.]?\d*)", text)
    vat_raw = extract_first(r"(?:Сумма НДС|VAT Amount)[^\d]*(\d+[ ,.]?\d*)", text)

    total = normalize_number(total_raw) if total_raw else None
    vat_amount = normalize_number(vat_raw) if vat_raw else None

    if vat_rate == "12%" and total is not None and vat_amount is not None:
        expected_vat = round(total * 12 / 112, 2)

        if abs(expected_vat - vat_amount) <= 1:
            checks.append({
                "field": "Расчет НДС",
                "status": "PASS",
                "message": "VAT amount matches formula.",
                "recommendation": "No action required."
            })
        else:
            checks.append({
                "field": "Расчет НДС",
                "status": "WARNING",
                "message": f"Expected VAT ≈ {expected_vat}, found {vat_amount}.",
                "recommendation": "Recalculate VAT amount."
            })
    else:
        checks.append({
            "field": "Расчет НДС",
            "status": "PASS",
            "message": "VAT calculation not required.",
            "recommendation": "No action required."
        })

    return {
        "overall_risk": determine_risk(checks),
        "checks": checks
    }