# Manufacturing Analytics Website

A full-stack manufacturing analytics website with a complete DevOps pipeline. Built with Vue 3 and FastAPI, deployed on AWS ECS Fargate with infrastructure managed by Terraform and CI/CD via GitHub Actions.

## Architecture
```
┌─────────────────────────────────────────────────────────┐
│                     GitHub Actions                      │
│         Build → Test → Push to Docker Hub               │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                        AWS                              │
│                                                         │
│   ┌─────────┐     ┌─────────────────────────────────┐   │
│   │   ALB   │────▶│         ECS Fargate            │   │
│   └─────────┘     │  ┌──────────┐  ┌─────────────┐  │   │
│                   │  │ Frontend │  │   Backend   │  │   │
│                   │  │  Vue 3   │  │   FastAPI   │  │   │
│                   │  │  nginx   │  │             │  │   │
│                   │  └──────────┘  └──────┬──────┘  │   │
│                   └─────────────────────┬─┘─────────┘   │
│                                         │               │
│                   ┌─────────────────────▼───────────┐   │
│                   │         RDS PostgreSQL          │   │
│                   └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Features

- **Defect Analysis** — Time-series visualization of defect counts with configurable grouping (hour, day, week)
- **Machine Performance Metrics** — Tracking of average cycle times, injection pressures, and barrel temperatures
- **Defect Distribution** — Categorical breakdown of defect types (flash, short mold, contamination)

## Tech Stack

| Layer | Technology |
| Frontend | Vue 3, TypeScript, Tailwind CSS |
| Backend | Python, FastAPI, SQLAlchemy |
| Database | PostgreSQL |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Registry | Docker Hub |
| Infrastructure | Terraform |
| Cloud | AWS ECS Fargate, RDS, ALB, VPC |
| Monitoring | Prometheus, Grafana, cAdvisor |

## DevOps Pipeline

1. **Code pushed to `main`** triggers GitHub Actions
2. **Docker images** are built for frontend and backend
3. **Images are pushed** to Docker Hub
4. **AWS infrastructure** is provisioned via Terraform (ECS, RDS, ALB, VPC)
5. **ECS Fargate** pulls images and runs containers
6. **Backend automatically seeds** the database on startup
7. **Prometheus + Grafana** monitor container metrics


## Running Locally

### Prerequisites
- Docker Desktop
- Node.js 20+
- Python 3.10+

### Quick Start with Docker Compose

```bash
# Clone the repo
git clone https://github.com/bdauria1/Interview-Project.git
cd Interview-Project

# Start all services
docker-compose up --build
```

This starts:
- Frontend at `http://localhost:80`
- Backend at `http://localhost:8000`
- PostgreSQL on port `5432`
- Grafana at `http://localhost:3000` (admin/admin)
- Prometheus at `http://localhost:9090`

### Manual Setup

#### Backend
```bash
cd Backend

# Create .env file
echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/appdb" > .env

# Install dependencies
pip install -r requirements.txt

# Create tables and seed data
python app/scripts/create_tables.py
python app/scripts/ingest_data.py

# Start server
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd Frontend

# Create .env file
echo "VITE_API_URL=http://127.0.0.1:8000" > .env

# Install dependencies
npm install

# Start dev server
npm run dev
```

## Deploying to AWS

### Prerequisites
- AWS CLI configured (`aws configure`)
- Terraform installed
- Docker Hub account

### Deploy

```bash
cd terraform

# Initialize Terraform
terraform init

# Preview changes
terraform plan -var="dockerhub_username=<your-username>" -var="db_password=<your-password>"

# Deploy
terraform apply -var="dockerhub_username=<your-username>" -var="db_password=<your-password>"
```

### Tear Down

```bash
terraform destroy -var="dockerhub_username=<your-username>" -var="db_password=<your-password>"
```

## Project Structure

```
Interview-Project/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD pipeline
├── Backend/
│   ├── app/
│   │   ├── core/           # Database config
│   │   ├── endpoints/      # API routes
│   │   ├── models/         # SQLAlchemy models
│   │   ├── repositories/   # Data access layer
│   │   ├── schemas/        # Pydantic schemas
│   │   └── scripts/        # DB init and seed scripts
│   ├── Dockerfile
│   ├── start.sh            # Container startup script
│   └── requirements.txt
├── Frontend/
│   ├── src/                # Vue 3 components
│   ├── Dockerfile
│   └── nginx.conf.template # nginx reverse proxy config
├── terraform/
│   ├── main.tf             # VPC, ALB, ECS cluster
│   ├── ecs.tf              # ECS services and task definitions
│   ├── rds.tf              # RDS PostgreSQL instance
│   ├── variables.tf
│   └── outputs.tf
├── monitoring/
│   └── prometheus.yml      # Prometheus scrape config
└── docker-compose.yml      # Local development stack
```