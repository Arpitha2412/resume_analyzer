import streamlit as st
import docx2txt
import fitz  # PyMuPDF
import re
import time
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from reportlab.pdfgen import canvas
from io import BytesIO
from streamlit_lottie import st_lottie

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ IMPROVED CUSTOM CSS ------------------
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            font-size: 17px;
        }

        .custom-header {
            background-image: linear-gradient(to right, #4e54c8, #8f94fb);
            padding: 1.2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
            font-size: 36px;
            font-weight: 700;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }

        .custom-footer {
            background-color: #f5f5f5;
            padding: 1rem;
            border-radius: 12px;
            margin-top: 2rem;
            text-align: center;
            font-size: 16px;
            color: #555;
            box-shadow: 0 -1px 10px rgba(0, 0, 0, 0.1);
        }

        .stButton button, .stDownloadButton button {
            background-color: #4e54c8;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-size: 16px;
        }

        .stButton button:hover, .stDownloadButton button:hover {
            background-color: #3d42a8;
            color: #fff;
        }

        textarea {
            font-size: 16px !important;
        }

        .stAlert {
            font-size: 16px;
        }

        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown('<div class="custom-header">📄 AI Resume Analyzer</div>', unsafe_allow_html=True)


# ------------------ LOAD LOTTIE ------------------
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_resume = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_tno6cg2w.json")

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=110)
    st.title("📌 Instructions")
    st.markdown("""
    - Upload your resume in `.docx` or `.pdf` format  
    - Enter job description  
    - View matched skills and analysis  
    - Export your report  
    """)

    st.markdown("---")
    st.info("Made with ❤️ by Arpitha N")
    # Theme logic



# ------------------ SKILLS ------------------
skills_list = [
    "python", "java", "c++", "html", "css", "javascript", "react", "node", "sql",
    "django", "flask", "machine learning", "deep learning", "data science",
    "communication", "teamwork", "leadership", "problem solving", "time management",
    "github", "linux"
]

# ------------------ TEXT EXTRACTION ------------------
def extract_text_from_docx(file):
    return docx2txt.process(file)

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "".join(page.get_text() for page in doc)

# ------------------ SCORE & KEYWORDS ------------------
def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())
    return list(set(words))

def score_resume(resume_text, jd_text):
    jd_keywords = extract_keywords(jd_text)
    matched = [kw for kw in jd_keywords if kw in resume_text.lower()]
    score = int((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 0
    return score, list(set(jd_keywords) - set(matched)), matched

# ------------------ EXPORT TO PDF ------------------
def generate_pdf_report(score, found_skills, missing, suggestions):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Resume Analysis Report")

    y = 770
    p.setFont("Helvetica", 12)
    p.drawString(100, y, f"Score: {score} / 100")
    y -= 30

    p.drawString(100, y, "Matched Skills:")
    for skill in found_skills:
        y -= 20
        p.drawString(120, y, f"- {skill.capitalize()}")

    y -= 30
    p.drawString(100, y, "Missing Keywords:")
    for key in missing:
        y -= 20
        p.drawString(120, y, f"- {key}")

    y -= 30
    p.drawString(100, y, "Suggestions:")
    for s in suggestions:
        y -= 20
        p.drawString(120, y, f"- {s[:60]}...")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# ------------------ WORD CLOUD ------------------
def display_wordcloud(keywords):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(keywords))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

# ------------------ BAR CHART ------------------
def show_bar_chart(matched, missing):
    fig = go.Figure(data=[
        go.Bar(name="Matched", x=matched, y=[1]*len(matched), marker_color='green'),
        go.Bar(name="Missing", x=missing, y=[1]*len(missing), marker_color='red')
    ])
    fig.update_layout(title="Keyword Matching", barmode='stack', height=400)
    st.plotly_chart(fig)

# ------------------ FILE UPLOAD ------------------
st_lottie(lottie_resume, height=200, key="resume")

st.subheader("🔍 Upload Your Resume File")
uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])



# ------------------ MAIN LOGIC ------------------
if uploaded_file:
    st.success("✅ Resume Uploaded Successfully!")
    with st.spinner("⏳ Analyzing Resume..."):
        time.sleep(2)

        text = extract_text_from_docx(uploaded_file) if uploaded_file.name.endswith(".docx") else extract_text_from_pdf(uploaded_file)
        jd_text = st.text_area("🧑‍💼 Paste Job Description", height=155)

        st.markdown("### 📝 Extracted Text (Preview):")
        st.code(text[:1000] + "..." if len(text) > 1000 else text)

        st.markdown("### 🧠 Matched Skills:")
        found_skills = [skill for skill in skills_list if re.search(rf"\b{skill}\b", text, re.IGNORECASE)]
        for skill in found_skills:
            st.success(f"✅ {skill.capitalize()}")
            

        if jd_text.strip():
            score, missing, matched = score_resume(text, jd_text)
            st.markdown(f"### 📊 Resume Score: **{score} / 100**")
            st.markdown("#### ❌ Missing Keywords:")
            st.warning(", ".join(missing) if missing else "None. Good job!")

            st.markdown("#### 💡 Smart Suggestions:")
            suggestions = []
            for sec in ["education", "experience", "skills", "projects"]:
                if sec not in text.lower():
                    suggestions.append(f"Consider adding a **{sec.capitalize()}** section.")

            suggestions += [f"Add more detail on '{kw}'" for kw in missing[:5]]
            for tip in suggestions:
                st.markdown(f"- {tip}")

            st.markdown("#### ☁️ Keyword Cloud")
            display_wordcloud(matched + missing)

            st.markdown("#### 📊 Keyword Match Chart")
            show_bar_chart(matched, missing)

            # Download PDF
            pdf_bytes = generate_pdf_report(score, found_skills, missing, suggestions)
            st.download_button("📄 Download Full Report (PDF)", data=pdf_bytes, file_name="resume_report.pdf", mime="application/pdf")

else:
    st.warning("📁 Please upload a resume file to begin.")
# ------------------ FOOTER ------------------
st.markdown("""
    <div class="custom-footer">
        <img src="https://cdn-icons-png.flaticon.com/512/1828/1828817.png" width="20"/>
        <span style="margin-left: 8px;">© 2025 Resume Analyzer | Built with ❤️ using Streamlit</span>
    </div>
""", unsafe_allow_html=True)

