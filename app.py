
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json

app = FastAPI()

# ----------- IN MEMORY DATABASE (for now) -----------
reports = []

# ----------- MODELS -----------
class Report(BaseModel):
    bathroom_id: int
    lat: float
    lon: float
    status: str  # "clean", "dirty", "locked", "no_supplies", "long_wait"
    gender: str  # "male" or "female"
    timestamp: Optional[str] = None

# ----------- ROUTES -----------

@app.get("/")
def root():
    return {"message": "🚽 1or2 API is running!"}

@app.get("/bathrooms")
def get_bathrooms():
    # Load from OpenStreetMap data
    with open("bathrooms.json", "r") as f:
        bathrooms = json.load(f)
    return {"bathrooms": bathrooms, "count": len(bathrooms)}

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
