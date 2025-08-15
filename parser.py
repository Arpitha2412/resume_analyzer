# parser.py

import fitz  # PyMuPDF
import docx2txt

def extract_text(file):
    """
    Extracts text from uploaded .pdf or .docx file.
    """
    if file.name.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in doc])
    elif file.name.endswith(".docx"):
        text = docx2txt.process(file)
    else:
        text = ""
    return text.strip()
