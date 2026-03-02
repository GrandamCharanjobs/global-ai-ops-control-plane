from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import uuid4

app = FastAPI(
    title="Global AI Ops Control Plane",
    version="0.2.0",
    description="Central control plane for multi-cloud SRE, cost, and security incidents.",
)

# ----- Models -----

class IncidentIn(BaseModel):
    source: str              # e.g. "aws-cloudwatch", "k8s-prometheus", "github-actions"
    service: str             # e.g. "payments-api", "eks-cluster-1"
    severity: str            # e.g. "SEV1", "SEV2", "INFO"
    title: str               # short description
    details: str             # longer message / raw alert
    region: Optional[str] = None      # optional, e.g. "us-east-1"
    created_at: Optional[datetime] = None  # client timestamp (optional)

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

# ----- Endpoints -----

@app.get("/")
def read_root():
    return {"message": "Global AI Ops Control Plane is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ingest/incident", response_model=IncidentOut)
def ingest_incident(incident: IncidentIn):
    """Ingest a single incident/alert from any source."""
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
    """List all incidents ingested so far."""
    return INCIDENTS
