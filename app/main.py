from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import uuid4

app = FastAPI(
    title="Global AI Ops Control Plane",
    version="0.1.0",
    description="Central control plane for multi-cloud SRE, cost, and security incidents.",
)

# ----- Models -----

class IncidentIn(BaseModel):
    source: str  # e.g. "aws-cloudwatch", "k8s-prometheus", "github-actions"
    service: str  # e.g. "payments-api", "eks-cluster-1"
    severity: str  # e.g. "SEV1", "SEV2", "INFO"
    title: str     # short description
    details: str   # longer message / raw alert
    region: str | None = None  # optional, e.g. "us-east-1"
    created_at: datetime | None = None  # client timestamp (optional)

class IncidentOut(IncidentIn):
    id: str
    received_at: datetime

# ----- In-memory storage -----

INCIDENTS: List[IncidentOut] = []

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
    incident_out = IncidentOut(
        id=str(uuid4()),
        received_at=datetime.utcnow(),
        **incident.dict(),
    )
    INCIDENTS.append(incident_out)
    return incident_out

@app.get("/incidents", response_model=List[IncidentOut])
def list_incidents():
    """List all incidents ingested so far."""
    return INCIDENTS
