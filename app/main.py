from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import uuid4
import os

app = FastAPI(
    title="Global AI Ops Control Plane",
    version="0.3.0",
    description="Central control plane for multi-cloud SRE, cost, and security incidents.",
)

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# ----- Models -----

class IncidentIn(BaseModel):
    source: str
    service: str
    severity: str
    title: str
    details: str
    region: Optional[str] = None
    created_at: Optional[datetime] = None

class IncidentOut(IncidentIn):
    id: str
    received_at: datetime
    ai_summary: Optional[str] = None
    ai_recommended_actions: List[str] = []

# ----- In-memory storage -----

INCIDENTS: List[IncidentOut] = []

# ----- Helper: fake AI for now -----

def generate_ai_summary(incident: IncidentIn) -> str:
    return f"{incident.severity} incident on {incident.service}: {incident.title}"

def generate_ai_recommendations(incident: IncidentIn) -> List[str]:
    recs = [
        "Check recent deployments for regressions.",
        "Inspect service logs around the incident time.",
    ]
    if incident.severity.upper().startswith("SEV1"):
        recs.insert(0, "Page on-call engineer immediately.")
    if "latency" in incident.title.lower():
        recs.append("Scale service replicas and verify downstream dependencies.")
    return recs

# ----- API Endpoints -----

@app.get("/")
def read_root():
    return {"message": "Global AI Ops Control Plane is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ingest/incident", response_model=IncidentOut)
def ingest_incident(incident: IncidentIn):
    ai_summary = generate_ai_summary(incident)
    ai_recs = generate_ai_recommendations(incident)

    incident_out = IncidentOut(
        id=str(uuid4()),
        received_at=datetime.utcnow(),
        ai_summary=ai_summary,
        ai_recommended_actions=ai_recs,
        **incident.dict(),
    )
    INCIDENTS.append(incident_out)
    return incident_out

@app.get("/incidents", response_model=List[IncidentOut])
def list_incidents():
    return INCIDENTS

# ----- HTML Dashboard -----

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    incidents = list(reversed(INCIDENTS))  # newest first
    sev1_count = sum(1 for i in incidents if i.severity.upper() == "SEV1")
    sev2_count = sum(1 for i in incidents if i.severity.upper() == "SEV2")

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "incidents": incidents,
            "sev1_count": sev1_count,
            "sev2_count": sev2_count,
            "version": app.version,
        },
    )
