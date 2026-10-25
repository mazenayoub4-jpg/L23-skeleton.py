# ════════════════════════════════════════════════════════════
#  المحاضرة ٢١ · الخدمة اللي رح ننشرها
#
#  ⚠ ما بتعدّلوا هالملف بالعملي — بتنشروه زي ما هو.
#     (إلا بالتاسكات الإضافية · وهناك بنقلّكم وين بالضبط)
#
#  محلياً:  uvicorn app:app --reload
#  بالحاوية: بيشتغل على 0.0.0.0:10000
# ════════════════════════════════════════════════════════════
# Install dependencies from a terminal, not as Python code:
# pip install fastapi uvicorn
app = FastAPI(title="My Project")

# Your knowledge dictionary
knowledge = {
    # Make sure your knowledge items are here...
}

@app.get("/ask")
def ask_question(q: str = None):
    if not q:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "لا يوجد سؤال",
                "suggestions": list(knowledge.keys())[:5]
            }
        )
    
    cleaned_q = clean(q)
    
    for key, val in knowledge.items():
        if clean(key) == cleaned_q:
            return {"answer": val[0], "source": val[1]}
            
    raise HTTPException(
        status_code=404,
        detail={
            "message": f"ما لقيت جواب لـ: {q}",
            "suggestions": list(knowledge.keys())[:5]
        }
    )
    import re

def clean(s: str) -> str:
    # Remove Tashkeel (Arabic diacritics)
    s = re.sub(r'[\u064B-\u0652]', '', s)
    
    # Normalize Alif / Hamzas
    s = re.sub(r'[إأآ]', 'ا', s)
    
    # Normalize Taa Marbouta to Ha
    s = s.replace('ة', 'ه')
    
    # Normalize Alif Maqsoora to Ya
    s = s.replace('ى', 'ي')
    
    # Trim leading/trailing whitespace & lowercase
    return s.strip().lower()
    @app.get("/ask")
def ask_question(q: str = None):
    if not q:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "لا يوجد سؤال",
                "suggestions": list(knowledge.keys())[:5]
            }
        )
    
    cleaned_q = clean(q)
    
    # Check for a match after normalizing
    for key, val in knowledge.items():
        if clean(key) == cleaned_q:
            return {"answer": val[0], "source": val[1]}
            
    # If no match found, return 404 with suggestions
    raise HTTPException(
        status_code=404,
        detail={
            "message": f"ما لقيت جواب لـ: {q}",
            "suggestions": list(knowledge.keys())[:5]
        }
    )
