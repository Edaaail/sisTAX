# app.py
import json
import streamlit as st
from analyzer import extract_text_from_file, call_gemini

st.set_page_config(page_title="KZTaxChecker", layout="wide")

st.title("KZTaxChecker - ESF Tax Risk Analyzer for Kazakhstan")

uploaded_file = st.file_uploader(
    "Upload ESF Invoice (PDF or TXT)",
    type=["pdf", "txt"]
)


def risk_banner(risk):
    if risk == "HIGH":
        color = "#ff4b4b"
    elif risk == "MEDIUM":
        color = "#f4c542"
    else:
        color = "#28c76f"

    st.markdown(
        f"""
        <div style="
            background:{color};
            padding:18px;
            border-radius:12px;
            margin-bottom:20px;
            color:black;
            font-size:24px;
            font-weight:bold;
            text-align:center;
        ">
            Overall Risk: {risk}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_card(item):
    status = item["status"]

    if status == "ERROR":
        color = "#ff4b4b"
    elif status == "WARNING":
        color = "#f4c542"
    else:
        color = "#28c76f"

    st.markdown(
        f"""
        <div style="
            background:{color};
            padding:16px;
            border-radius:12px;
            margin-bottom:12px;
            color:black;
        ">
            <h4>{item['field']} — {status}</h4>
            <p><b>Message:</b> {item['message']}</p>
            <p><b>Recommendation:</b> {item['recommendation']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if uploaded_file:
    with st.spinner("Analyzing invoice..."):
        text = extract_text_from_file(uploaded_file)
        result = call_gemini(text)

    risk_banner(result["overall_risk"])

    st.subheader("Validation Checks")

    for item in result["checks"]:
        render_card(item)

    json_report = json.dumps(result, indent=4, ensure_ascii=False)

    st.download_button(
        label="Download JSON Report",
        data=json_report,
        file_name="kztaxchecker_report.json",
        mime="application/json"
    )