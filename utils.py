# utils.py

import re

def clean_text(text):
    """
    Lowercases and removes unwanted characters from text.
    """
    return re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())

def extract_keywords(text, min_len=4):
    """
    Extracts unique keywords of minimum length from the text.
    """
    cleaned = clean_text(text)
    words = re.findall(r'\b\w{%d,}\b' % min_len, cleaned)
    return sorted(set(words))

def match_skills(resume_text, skills_list):
    """
    Returns list of matched skills from the predefined list.
    """
    resume_text = clean_text(resume_text)
    return [skill for skill in skills_list if skill.lower() in resume_text]
