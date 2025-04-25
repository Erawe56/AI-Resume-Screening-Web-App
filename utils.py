import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_keywords_from_jd(jd_text):
    jd_text = re.sub(r"[^\w\s]", "", jd_text.lower())
    return set(jd_text.split())

def calculate_match_score(text, jd_text):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([jd_text, text])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return float(score)
