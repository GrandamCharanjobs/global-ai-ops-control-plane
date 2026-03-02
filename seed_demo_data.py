import requests

BASE_URL = "http://127.0.0.1:8000"

INCIDENTS = [
    {
        "source": "aws-cloudwatch",
        "service": "payments-api",
        "severity": "SEV1",
        "title": "API latency spike",
        "details": "P95 latency above 2000ms for 10 minutes in us-east-1.",
        "region": "us-east-1",
    },
    {
        "source": "k8s-prometheus",
        "service": "orders-service",
        "severity": "SEV2",
        "title": "Error rate increase",
        "details": "5xx error rate above 3% over last 5 minutes.",
        "region": "eu-west-1",
    },
    {
        "source": "github-actions",
        "service": "frontend-web",
        "severity": "INFO",
        "title": "New deployment completed",
        "details": "Deploy #123 completed successfully on main branch.",
        "region": "us-central1",
    },
]

def main():
    for payload in INCIDENTS:
        r = requests.post(f"{BASE_URL}/ingest/incident", json=payload)
        print(r.status_code, r.json()["id"])

if __name__ == "__main__":
    main()
