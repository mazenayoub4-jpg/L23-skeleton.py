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
import time
import logging
import os
import json
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException  # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse  # pyright: ignore[reportMissingImports]

app = FastAPI(title="...", version="1.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    if request.url.path == "/quote" and response.status_code == 200:
        usage["tokens"] += TOKENS_PER_QUOTE
    
    # Check if status code indicates an error (e.g., 404, 500, etc.)
    if response.status_code >= 400:
        logger.warning(f"Path: {request.url.path} | Status: {response.status_code} | Time: {process_time:.2f}s")
    else:
        logger.info(f"Path: {request.url.path} | Status: {response.status_code} | Time: {process_time:.2f}s")
        
    return response

# ───── المفتاح · من البيئة · مش من الكود ─────
SERVICE_KEY = os.environ.get("PRICING_API_KEY", "")
TOKENS_PER_QUOTE = 1500
USD_PER_1K_TOKENS = 0.002
usage = {"tokens": 0}
# ───── البيانات ─────
CATALOG = {"A-100": ("سعر الكتالوج 120 دينار", 120),
           "A-200": ("سعر الكتالوج 80 دينار",  80),
           "A-300": ("سعر الكتالوج 45 دينار",  45)}
PROMOS  = {"A-100": ("سعر العرض 95 دينار",      95)}

# ───── الحالة · بملف · زي ما صلّحناها بمحاضرة ٢٠ ─────
STATE = Path("state.json")


def اقرا_العداد() -> int:
    try:
        return int(json.loads(STATE.read_text())["count"])
    except Exception:
        return 0


def زيّد_العداد() -> int:
    n = اقرا_العداد() + 1
    try:
        STATE.write_text(json.dumps({"count": n}))
    except Exception:
        pass
    return n


def سعّر(code: str) -> str:
    """بترجّع السعر النهائي — الأرخص · مع تنبيه عن الباقي."""
    نتائج = []
    if code in CATALOG:
        نتائج.append(("catalog",) + CATALOG[code])
    if code in PROMOS:
        نتائج.append(("promo",) + PROMOS[code])
    if not نتائج:
        return ""
    src, txt, price = min(نتائج, key=lambda f: f[2])
    رد = txt
    باقي = [f for f in نتائج if f[0] != src]
    if باقي:
        رد += " · تنبيه: " + " · ".join(t for _, t, _ in باقي)
    return رد


@app.get("/", response_class=HTMLResponse)
def home():
    """صفحة الترحيب."""
    return """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<title>خدمة التسعير</title>
<style>
 body{font-family:system-ui,sans-serif;background:#0f1419;color:#e8eaed;
      display:flex;min-height:100vh;align-items:center;justify-content:center;margin:0}
 .c{text-align:center;padding:40px}
 h1{font-size:34px;margin:0 0 10px}
 p{color:#9aa0a6;margin:0 0 26px}
 a{display:inline-block;margin:6px;padding:10px 18px;border-radius:8px;
   background:#1f2937;color:#e8eaed;text-decoration:none;font-family:monospace}
 a:hover{background:#2d3748}
</style></head><body><div class="c">
<h1>خدمة التسعير شغّالة ✓</h1>
<p>وهاي على الإنترنت — مش على جهازك</p>
<a href="/quote?code=A-100">/quote?code=A-100</a>
<a href="/health">/health</a>
<a href="/stats">/stats</a>
<a href="/docs">/docs</a>
</div></body></html>"""


@app.get("/health")
def health():
    """حالة الخدمة · وهل المفتاح محمّل."""
    return {"status": "ok",
            "key_loaded": bool(SERVICE_KEY),
            "requests": اقرا_العداد()}


@app.get("/quote")
def quote(code: str):
    """بترجّع السعر النهائي لمنتج حسب كوده."""
    رد = سعّر(code)
    if not رد:
        raise HTTPException(status_code=404,
                            detail=f"ما لقيت سعر للكود {code}.")
    زيّد_العداد()
    return {"code": code, "answer": رد}

@app.get("/stats")
def stats():
    """كم طلب تسعير وصل من آخر إعادة تشغيل."""
    return {
        "count": اقرا_العداد(),
        "estimated_tokens": usage["tokens"],
        "estimated_cost_usd": round(
