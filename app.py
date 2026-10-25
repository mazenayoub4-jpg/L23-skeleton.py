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
@app.get("/ask")
def ask_question(q: str = None):
    if q in knowledge:
        return {"answer": knowledge[q][0], "source": knowledge[q][1]}
    else:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Answer not found for your query.",
                "suggestions": list(knowledge.keys())[:5]
            }
        )
