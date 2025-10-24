# -------------------- LegalGPT: AI Lawyer for Contract Review & Risk Scoring --------------------
import streamlit as st
from openai import OpenAI
from docx import Document
from fpdf import FPDF
import io
import os

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="LegalGPT - AI Contract Reviewer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- Sidebar --------------------
st.sidebar.markdown("<h2 style='text-align:center;'>LegalGPT</h2>", unsafe_allow_html=True)

logo_path = "DeWatermark.ai_1761195400402.jpg"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=150, caption="AI Contract Reviewer")
else:
    st.sidebar.markdown("<p style='text-align:center; color:gray;'>🖼️ Logo not found</p>", unsafe_allow_html=True)

st.sidebar.title("⚖️ LegalGPT Menu")
uploaded_file = st.sidebar.file_uploader("📁 Upload a contract (.docx or .txt)", type=["docx", "txt"])
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by **SASIKUMAR G**")

# -------------------- Main Area --------------------
st.title("⚖️ LegalGPT - AI Lawyer for Contract Review & Risk Scoring")
st.markdown("""
This tool **analyzes contracts**, highlights key clauses, identifies risky terms, and calculates a risk score.
""")

# -------------------- OpenAI Client --------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------- Helper Functions --------------------
def read_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

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

# -------------------- Contract Processing --------------------
contract_text = None
if uploaded_file:
    if uploaded_file.name.endswith(".docx"):
        contract_text = read_docx(uploaded_file)
    else:
        contract_text = uploaded_file.read().decode("utf-8")

    st.subheader("📄 Contract Preview")
    st.text_area("Preview", contract_text[:2000], height=200)

    # -------------------- GPT Analysis --------------------
    if st.button("🔍 Analyze Contract"):
        with st.spinner("Analyzing with LegalGPT..."):
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

            try:
                ai_output = response.choices[0].message.content
            except AttributeError:
                ai_output = response.choices[0].message["content"]

            st.subheader("🧠 LegalGPT Analysis")
            st.write(ai_output)

            # Risk Score
            st.subheader("⚠️ Risk Score")
            st.metric(label="Estimated Risk (1–10)", value=risk_score(contract_text))

# -------------------- Footer --------------------
st.markdown("---")
st.markdown('<p style="color:gray; font-size:12px;">© 2025 LegalGPT | Built with Python, Streamlit & OpenAI</p>', unsafe_allow_html=True)
