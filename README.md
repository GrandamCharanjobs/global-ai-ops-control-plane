# 🚀 Global AI Ops Control Plane ⭐ FLAGSHIP

**Production FastAPI control plane** that aggregates SRE, cost, and security incidents from AWS CloudWatch, Kubernetes Prometheus, and GitHub Actions into a unified mission-control dashboard with **AI-generated summaries and remediation recommendations**.

## 🎯 FEATURES

- **Multi-source ingestion**: AWS CloudWatch • K8s Prometheus • GitHub Actions
- **AI-powered analysis**: Auto-generated severity summaries + runbook recommendations  
- **Dark SRE mission-control UX**: Real-time incident timelines + SEV1/SEV2 counts
- **Production API**: Swagger docs + Pydantic validation + extensible models
- **Demo-ready**: `seed_demo_data.py` creates realistic incident streams

## 🏗️ ARCHITECTURE

AWS CloudWatch → K8s Prometheus → GitHub Actions →
↓ ↓ ↓
POST /ingest/incident ────────────────────────────→
In-Memory Store + AI Brain
↓
/dashboard (Live View)

text

## 🚀 QUICKSTART (90 seconds)
git clone https://github.com/GrandamCharanjobs/global-ai-ops-control-plane
cd global-ai-ops-control-plane
python3 -m venv venv && source venv/bin/activate
pip install fastapi uvicorn jinja2 requests
uvicorn app.main:app --reload
# New terminal:
python3 seed_demo_data.py
open http://127.0.0.1:8000/dashboard

📊 PRODUCTION METRICS (Demo)
text
Incidents: 3+ | SEV1: 1 | SEV2: 1
-  payments-api SEV1: "API latency spike" → "Page on-call immediately"
-  orders-service SEV2: "Error rate increase" 
-  frontend-web INFO: "New deployment completed"
🔗 CONNECTS TO MY PLATFORMS
This unifies my existing production systems:

AI SRE Co-Pilot

AWS Lambda Incident Command

eBPF Security Pipeline

🛠️ TECH STACK
FastAPI 0.111.0 • Uvicorn 0.30.1 • Jinja2 • Pydantic • Python 3.14

Built in 2hrs → Staff SRE platform quality → Ready for FAANG interviews 🚀
