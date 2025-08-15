# analyzer.py

import spacy
import language_tool_python
from utils import extract_keywords, match_skills

nlp = spacy.load("en_core_web_sm")
tool = language_tool_python.LanguageTool('en-US')

REQUIRED_SECTIONS = ["education", "experience", "skills", "projects"]

def analyze_resume(resume_text, jd_text, skills_list):
    """
    Main analysis function to evaluate resume against job description.
    Returns:
      - Matched skills
      - Missing JD keywords
      - Section suggestions
      - Grammar feedback
    """
    # Keyword match
    jd_keywords = extract_keywords(jd_text)
    matched_keywords = [kw for kw in jd_keywords if kw in resume_text.lower()]
    missing_keywords = list(set(jd_keywords) - set(matched_keywords))
    
    # Skill match
    matched_skills = match_skills(resume_text, skills_list)
    
    # Section suggestions
    section_tips = [
        f"Consider adding a **{sec.capitalize()}** section."
        for sec in REQUIRED_SECTIONS if sec not in resume_text.lower()
    ]

    # Grammar check (top 3 issues)
    grammar_issues = [match.message for match in tool.check(resume_text)[:3]]

    return {
        "matched_skills": matched_skills,
        "missing_keywords": missing_keywords,
        "suggestions": section_tips + grammar_issues,
        "keyword_score": int((len(matched_keywords) / len(jd_keywords)) * 100) if jd_keywords else 0
    }
