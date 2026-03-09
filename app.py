
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json

app = FastAPI()

reports = []

class Report(BaseModel):
    bathroom_id: int
    lat: float
    lon: float
    status: str
    gender: str
    timestamp: Optional[str] = None

@app.get("/")
def root():
    return FileResponse("wc_map.html")

@app.get("/bathrooms")
def get_bathrooms():
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
