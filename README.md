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
<img width="1470" height="956" alt="Screenshot 2026-03-02 at 10 29 36 AM" src="https://github.com/user-attachments/assets/4f000d10-0d69-435f-bc8f-1071933325c0" />
<img width="1470" height="956" alt="Screenshot 2026-03-02 at 10 30 16 AM" src="https://github.com/user-attachments/assets/c54773be-db7c-48cf-a605-3c534571b94a" />

<img width="1470" height="956" alt="Screenshot 2026-03-02 at 10 35 32 AM" src="https://github.com/user-attachments/assets/288bd84a-b48b-4110-8582-4e6c3b47b4a9" />
<img width="1470" height="956" alt="Screenshot 2026-03-02 at 10 37 33 AM" src="https://github.com/user-attachments/assets/2abb93cf-1b51-476a-8ea8-bd64cb0e249b" />
<img width="1470" height="956" alt="Screenshot 2026-03-02 at 10 42 19 AM" src="https://github.com/user-attachments/assets/33f6e1b6-c9d7-4163-9a8e-af42d670f64d" />





