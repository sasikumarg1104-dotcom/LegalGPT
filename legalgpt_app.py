import streamlit as st
from openai import OpenAI
from docx import Document
from fpdf import FPDF
import io
import os

# ----------------------------
# Initialize OpenAI
# ----------------------------
client = OpenAI(api_key="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")  # <-- Replace with your OpenAI key

# ----------------------------
# Risk Score Function
# ----------------------------
def risk_score(text):
    keywords = {
        "penalty": 10,
        "termination": 8,
        "liability": 10,
        "indemnity": 9,
        "confidentiality": 5,
        "warranty": 7,
        "arbitration": 6,
        "governing law": 4
    }
    score = sum(val for word, val in keywords.items() if word in text.lower())
    return min(score, 10)

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="LegalGPT - AI Contract Reviewer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Sidebar
# ----------------------------
# --- Sidebar Logo Section ---
import os
import streamlit as st

logo_path = r"DeWatermark.ai_1761195400402.jpg"

with st.sidebar:
    st.markdown("<h2 style='text-align: top;'>LegalGPT</h2>", unsafe_allow_html=True)
    if os.path.exists(logo_path):
        st.image(logo_path, width=150, caption="AI Contract Reviewer", use_container_width=False)
    else:
        st.markdown("<p style='text-align: center; color: gray;'>🖼️ Logo not found</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)


st.sidebar.title("⚖️ LegalGPT Menu")
st.sidebar.markdown("""
**Upload your contract:**  
- .docx or .txt files  

**Analyze:**  
- Click the button to get GPT summary, clause highlights & risk score
""")
uploaded_file = st.sidebar.file_uploader("📁 Choose a contract", type=["docx", "txt"])
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by **SASIKUMAR G**")

# ----------------------------
# Main Area
# ----------------------------
st.title("⚖️ LegalGPT - AI Lawyer for Contract Review & Risk Scoring")
st.markdown("""
This tool **analyzes contracts**, highlights key clauses, identifies risky terms, calculates risk score, and allows PDF export.
""")

contract_text = None

if uploaded_file:
    # Read document
    if uploaded_file.name.endswith(".docx"):
        doc = Document(uploaded_file)
        contract_text = "\n".join([p.text for p in doc.paragraphs])
    else:
        contract_text = uploaded_file.read().decode("utf-8")

    # Contract Preview
    st.subheader("📄 Contract Preview")
    st.text_area("Preview", contract_text[:2000], height=200)

    # Analyze Button
    if st.button("🔍 Analyze Contract"):
        with st.spinner("Analyzing with LegalGPT..."):
            # Prompt GPT for summary, clauses, and risk analysis
            prompt = f"""
            Review this contract and:
            1. Summarize key clauses
            2. Highlight risky terms
            3. Rate overall risk (1–10)
            Provide results in sections: Summary, Clause Highlights, Risk Analysis.
            Contract Text:
            {contract_text}
            """
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            ai_output = response.choices[0].message.content

            # Display GPT Analysis in Sections
            st.subheader("🧠 LegalGPT Analysis")
            st.write(ai_output)

            # Risk Score Metric
            st.subheader("⚠️ Risk Score")
            st.metric(label="Estimated Risk (1–10)", value=risk_score(contract_text))

            # ----------------------------

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown('<p style="color:gray; font-size:12px;">© 2025 LegalGPT | Built with Python, Streamlit & OpenAI</p>', unsafe_allow_html=True)

