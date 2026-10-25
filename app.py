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
import re
from fastapi import FastAPI, HTTPException

app = FastAPI(title="My Project")

# Task 2: Arabic text normalization function
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

# Knowledge base dictionary (value format: [answer, topic/source])
knowledge = {
    "ما هي الإجارة؟": ["الإجارة هي عقد تمويل مبني على استئجار الأصول.", "مستندات الشركة"],
    "ما هي الشروط؟": ["يشترط توفر الأصول ووضوح المدة.", "دليل السياسات"],
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

# Task 3: Metrics endpoint to track questions per topic
@app.get("/metrics")
def get_metrics():
    by_topic = {}
    for key, val in knowledge.items():
        topic = val[1]  # Topic/source field
        by_topic[topic] = by_topic.get(topic, 0) + 1
        
    return {
        "total_questions": len(knowledge),
        "by_topic": by_topic
    }
