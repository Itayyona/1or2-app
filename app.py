
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json

app = FastAPI()

reports = []
user_bathrooms = []
reviews = {}

class Report(BaseModel):
    bathroom_id: int
    lat: float
    lon: float
    status: str
    gender: str
    timestamp: Optional[str] = None

class UserBathroom(BaseModel):
    lat: float
    lon: float
    name: str
    note: Optional[str] = ""

class Review(BaseModel):
    bathroom_id: int
    text: str
    gender: str

@app.get("/")
def root():
    with open("wc_map.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/bathrooms")
def get_bathrooms():
    with open("bathrooms.json", "r") as f:
        bathrooms = json.load(f)
    return {"bathrooms": bathrooms + user_bathrooms, "count": len(bathrooms) + len(user_bathrooms)}

@app.post("/bathroom/add")
def add_bathroom(b: UserBathroom):
    new_id = 9000000000 + len(user_bathrooms)
    new_b = {
        "id": new_id,
        "lat": b.lat,
        "lon": b.lon,
        "name": b.name or "Public Toilet",
        "access": "unknown",
        "fee": "unknown",
        "wheelchair": "unknown",
        "user_added": True,
        "note": b.note,
        "added_at": datetime.now().isoformat()
    }
    user_bathrooms.append(new_b)
    return {"message": "✅ Bathroom added!", "bathroom": new_b}

@app.post("/report")
def submit_report(report: Report):
    report.timestamp = datetime.now().isoformat()
    reports.append(report.dict())
    return {"message": "✅ Report submitted!", "report": report}

@app.get("/reports")
def get_reports(bathroom_id: Optional[int] = None):
    if bathroom_id:
        filtered = [r for r in reports if r["bathroom_id"] == bathroom_id]
        return {"reports": filtered}
    return {"reports": reports, "count": len(reports)}

@app.post("/review")
def add_review(review: Review):
    bid = review.bathroom_id
    if bid not in reviews:
        reviews[bid] = []
    reviews[bid].append({
        "text": review.text,
        "gender": review.gender,
        "timestamp": datetime.now().isoformat()
    })
    return {"message": "✅ Review added!"}

@app.get("/reviews/{bathroom_id}")
def get_reviews(bathroom_id: int):
    return {"reviews": reviews.get(bathroom_id, [])}
