## AI-Powered CI/CD Monitoring Dashboard

An end-to-end DevOps portfolio project showcasing a production-style stack:

- **Backend**: FastAPI, PostgreSQL, SQLAlchemy, JWT auth, AI anomaly detection (IsolationForest)
- **Frontend**: React (Vite + TypeScript), Tailwind CSS
- **Infra**: Docker, `docker-compose`, GitHub Actions CI, Kubernetes
- **Observability**: Prometheus metrics, Grafana dashboards, structured logging

### Features

- **Real-time CI/CD monitoring** via webhook-style event ingestion (GitHub Actions compatible endpoint)
- **Pipeline management**: define pipelines by repo/branch
- **Historical metrics**: success rate, run counts, duration
- **AI-powered anomaly detection** on run durations
- **JWT authentication** with role-based access (admin/viewer)
- **Production-ready Docker setup** and CI workflows

### Architecture Overview

- `backend/`: FastAPI app
  - `app/main.py`: app factory + routers + CORS + Prometheus `/metrics`
  - `app/models.py`: `User`, `Pipeline`, `PipelineRun`, `RunMetric`
  - `app/schemas.py`: Pydantic request/response models
  - `app/services/`: `auth_service`, `pipeline_service`, `anomaly_service`
  - `app/core/`: `config`, `security`, `deps`
  - DB: PostgreSQL via SQLAlchemy
- `frontend/`: React + TS + Tailwind
  - Vite-based SPA consuming backend APIs
- `docker-compose.yml`: runs `db`, `backend`, `frontend`, `prometheus`, and `grafana`
- `.github/workflows/ci.yml`: backend tests, frontend lint+build
- `monitoring/prometheus.yml`: local Prometheus scrape configuration
- `k8s/`: production-style Kubernetes manifests (namespace, backend, frontend, Postgres, Prometheus, Grafana, ingress)

### Local Development

#### Prerequisites

- Python 3.12+
- Node 20+ (or 22)
- Docker + Docker Compose

#### Backend (without Docker)

```bash
cd backend
cp .env.example .env  # adjust secrets if needed
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs will be at `http://localhost:8000/docs`.

#### Frontend (without Docker)

```bash
cd frontend
npm install
npm run dev
```

The app will be at `http://localhost:5173`.

Set `VITE_API_BASE_URL` (e.g. in `.env` or command line) to point to your backend if needed.

### Running with Docker

```bash
docker compose up --build
```

- Backend: `http://localhost:8000` (API + `/docs` + `/metrics`)
- Frontend: `http://localhost:5173`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (default: `admin` / `admin`)

In Grafana, add Prometheus as a data source (`http://prometheus:9090`) and build dashboards for the `backend` job (latency, error rates, etc.).

### CI/CD Integration (GitHub Actions Example)

1. Create a pipeline entry via the API or future UI, referencing your repo and branch.
2. Configure a GitHub Actions webhook to point at:

   - `POST http://<backend-host>/events/github`

3. The backend will:

   - Match the incoming event to a configured pipeline (by `repo` and `branch`)
   - Store a `PipelineRun` record and update metrics
   - Feed run durations into the IsolationForest model for anomaly scoring

### GitHub Actions CI

The workflow in `.github/workflows/ci.yml`:

- Installs backend dependencies and runs `pytest`
- Installs frontend dependencies, runs `npm run lint` and `npm run build`

You can extend this with deploy jobs (e.g. Docker push, Kubernetes, SSH to VM).

### Kubernetes Deployment

Kubernetes manifests live in `k8s/` and target a namespace `ai-cicd-monitor`:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
kubectl apply -f k8s/monitoring.yaml
kubectl apply -f k8s/ingress.yaml
```

- Backend/Frontend images are referenced as `your-docker-registry/ai-cicd-backend:latest` and `your-docker-registry/ai-cicd-frontend:latest` — push your built images there and update as needed.
- Ingress assumes an NGINX ingress controller and host `ai-cicd.local` (adjust to your environment and add a local DNS entry if necessary).

### Screenshots

- `docs/screenshots/dashboard.png` – main dashboard with KPIs and anomaly list
- `docs/screenshots/pipeline-detail.png` – detailed view of a single pipeline run history

Create these screenshots after you run the stack locally and commit them to the repo to enrich your portfolio.

### Next Steps / Customization

- Add a real authentication UI and backend user bootstrap script
- Enhance anomaly logic (per-pipeline models, additional features)
- Add more visualizations (latency distributions, failure reasons)
- Integrate with other CI providers (GitLab CI, CircleCI, etc.)

