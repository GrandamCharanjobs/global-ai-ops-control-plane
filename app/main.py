from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import uuid4
import os
import sqlite3
from contextlib import contextmanager
import json
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI(
    title="Global AI Ops Control Plane",
    version="0.6.0",
    description="Production SRE platform with LOCAL ML AI + PERSISTENT SQLite.",
)

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

DB_PATH = "incidents.db"

# ===== LOCAL ML MODELS (100% FREE, NO API KEYS) =====
model = SentenceTransformer('all-MiniLM-L6-v2')
tfidf_vectorizer = TfidfVectorizer(max_features=1000)

# Pre-trained remediation patterns
REMEDIATION_PATTERNS = {
    "latency": ["Scale replicas to 10+", "Check database connections", "Review recent deployments"],
    "error": ["Rollback latest deployment", "Check application logs", "Verify downstream services"], 
    "traffic": ["Review eBPF flows", "Inspect Cilium policies", "Check autoscaling limits"],
    "deploy": ["Monitor post-deployment metrics", "Verify canary rollout", "Check GitHub Actions logs"],
    "security": ["🚨 PAGE SECURITY TEAM", "Review eBPF anomalies", "Block suspicious pod traffic"]
}

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id TEXT PRIMARY KEY,
                received_at TEXT,
                source TEXT,
                service TEXT,
                severity TEXT,
                title TEXT,
                details TEXT,
                region TEXT,
                ai_summary TEXT,
                ai_recommended_actions TEXT
            )
        """)
        conn.commit()

init_db()

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

# ===== LOCAL ML AI INTEGRATION =====
def generate_ai_summary(incident: IncidentIn) -> str:
    """Local ML-powered incident summary"""
    text = f"{incident.title} {incident.service} {incident.details}"
    
    # Semantic analysis using sentence transformers
    embedding = model.encode(text)
    
    summary_templates = [
        f"🚨 {incident.severity}: {incident.title} impacting {incident.service}",
        f"Critical {incident.service} incident: {incident.title}",
        f"{incident.service} experiencing {incident.title.lower()}",
        f"ALERT: {incident.title} on {incident.service} ({incident.source})"
    ]
    
    # Simple ML scoring
    scores = cosine_similarity([embedding], [model.encode(t) for t in summary_templates])[0]
    best_template = summary_templates[np.argmax(scores)]
    
    return best_template

def generate_ai_recommendations(incident: IncidentIn) -> List[str]:
    """Local ML-powered remediation recommendations"""
    text = f"{incident.title} {incident.details}".lower()
    
    # Keyword matching + ML similarity
    recommendations = []
    
    for pattern, actions in REMEDIATION_PATTERNS.items():
        if pattern in text:
            recommendations.extend(actions[:2])
    
    # ML-powered semantic recommendations
    incident_embedding = model.encode(text)
    pattern_embeddings = model.encode(list(REMEDIATION_PATTERNS.keys()))
    similarities = cosine_similarity([incident_embedding], pattern_embeddings)[0]
    
    top_pattern_idx = np.argmax(similarities)
    top_pattern = list(REMEDIATION_PATTERNS.keys())[top_pattern_idx]
    recommendations.extend(REMEDIATION_PATTERNS[top_pattern][:1])
    
    # Severity-based actions
    if incident.severity.upper().startswith("SEV1"):
        recommendations.insert(0, "🚨 PAGE ON-CALL ENGINEER IMMEDIATELY")
    
    return recommendations[:4]

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Global AI Ops Control Plane v0.6.0 - LOCAL ML AI + SQLite LIVE"}

@app.get("/health")
def health_check():
    return {"status": "ok", "db": "sqlite", "ai": "local-ml-sentence-transformers"}

@app.post("/ingest/incident", response_model=IncidentOut)
def ingest_incident(incident: IncidentIn):
    """LOCAL ML AI analysis + SQLite persistence"""
    ai_summary = generate_ai_summary(incident)
    ai_recs = generate_ai_recommendations(incident)

    incident_out = IncidentOut(
        id=str(uuid4()),
        received_at=datetime.utcnow(),
        ai_summary=ai_summary,
        ai_recommended_actions=ai_recs,
        **incident.dict(),
    )
    
    with get_db() as conn:
        conn.execute("""
            INSERT INTO incidents 
            (id, received_at, source, service, severity, title, details, region, 
             ai_summary, ai_recommended_actions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            incident_out.id, incident_out.received_at.isoformat(), incident_out.source,
            incident_out.service, incident_out.severity, incident_out.title,
            incident_out.details, incident_out.region, incident_out.ai_summary,
            json.dumps(incident_out.ai_recommended_actions)
        ))
        conn.commit()
    
    return incident_out

@app.get("/incidents", response_model=List[IncidentOut])
def list_incidents():
    with get_db() as conn:
        rows = conn.execute("""
            SELECT id, received_at, source, service, severity, title, details, 
                   region, ai_summary, ai_recommended_actions 
            FROM incidents ORDER BY received_at DESC
        """).fetchall()
        
        incidents = []
        for row in rows:
            inc_dict = dict(row)
            inc_dict['ai_recommended_actions'] = json.loads(inc_dict['ai_recommended_actions'])
            inc_dict['received_at'] = datetime.fromisoformat(inc_dict['received_at'])
            incidents.append(IncidentOut(**inc_dict))
        return incidents

@app.get("/stats")
def get_stats():
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]
        sev1 = conn.execute("SELECT COUNT(*) FROM incidents WHERE severity LIKE 'SEV1%'").fetchone()[0]
        sev2 = conn.execute("SELECT COUNT(*) FROM incidents WHERE severity LIKE 'SEV2%'").fetchone()[0]
    return {"total": total, "sev1": sev1, "sev2": sev2}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    incidents = list_incidents()
    stats = get_stats()
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "incidents": incidents,
            "sev1_count": stats["sev1"],
            "sev2_count": stats["sev2"],
            "total_count": stats["total"],
            "version": app.version,
        },
    )
