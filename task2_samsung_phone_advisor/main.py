from fastapi import FastAPI
from pydantic import BaseModel

from database import fetch_phone_by_model, best_battery_under_price
from agents import data_extractor, review_generator

app = FastAPI(title="Samsung Phone Advisor")


class Question(BaseModel):
    question: str


def detect_intent(q):
    q = q.lower()
    if "compare" in q:
        return "compare"
    elif "best battery" in q:
        return "recommend"
    else:
        return "spec"


@app.post("/ask")
def ask(question: Question):
    intent = detect_intent(question.question)

    # -------- Specs (RAG) --------
    if intent == "spec":
        phone = data_extractor(fetch_phone_by_model, question.question)
        if not phone:
            return {"answer": "Phone not found."}
        return {"answer": review_generator(phone)}

    # -------- Compare --------
    if intent == "compare":
        p1 = data_extractor(fetch_phone_by_model, "S23 Ultra")
        p2 = data_extractor(fetch_phone_by_model, "S22 Ultra")
        return {"answer": review_generator(p1, p2)}

    # -------- Recommendation --------
    if intent == "recommend":
        best = best_battery_under_price(1000)
        return {
            "answer": f"{best[0]} has the best battery ({best[1]}mAh) under $1000."
        }
