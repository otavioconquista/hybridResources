import re
import unicodedata
from typing import Set
from config import TECH_KEYWORDS

def strip_accents(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    nfkd = unicodedata.normalize('NFD', text)
    return "".join([c for c in nfkd if not unicodedata.category(c) == 'Mn'])

def normalize_text(text: str) -> str:
    text = (text or "").lower()
    text = strip_accents(text)
    text = re.sub(r"[^0-9a-zA-Z\.\+\#\/\-\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_skills_from_text(text: str, keywords: Set[str] = TECH_KEYWORDS) -> Set[str]:
    text_norm = normalize_text(text)
    found = set()
    for kw in keywords:
        pattern = r"\b" + re.escape(kw.lower()) + r"\b"
        if re.search(pattern, text_norm):
            found.add(kw.lower())
    return found