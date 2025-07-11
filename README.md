# 🚀 Agentic Agile System - RESTful API Hub MVP

A central, extensible API hub that orchestrates all agent and system interactions for the Agentic Agile System.

## 🎯 Mission

Deliver a central, extensible API hub that orchestrates all agent and system interactions, is ready for new modules and 3rd party integrations, and sets a new bar for developer experience.

## ✨ Core Features

- **Dynamic Agent Registration**: Agents register themselves and advertise capabilities at runtime
- **Versioned Endpoints**: All endpoints prefixed (e.g., `/v1/`) for future-proofing
- **Live OpenAPI Docs**: Interactive, always up-to-date documentation with try-it-now sandbox
- **Rate Limiting & Throttling**: Adaptive, per-agent quotas with burst and abuse protection
- **Centralized Error Handling**: Unified error format, remediation hints, and trace IDs
- **Event Bus Integration**: Redis Streams for async, decoupled agent communication
- **Health & Readiness Checks**: `/health` and `/ready` endpoints for monitoring
- **Audit & Analytics**: Full audit trail of all API and agent actions
- **Plug-in Friendly**: Designed for seamless onboarding of new agents
- **Security by Default**: OAuth2/JWT, RBAC, TLS, and automated security scanning

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Event Bus     │
│   Dashboard     │◄──►│   (FastAPI)     │◄──►│   (Redis)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │   MongoDB       │    │   Agent Pool    │
│   (Structured)  │    │   (Flexible)    │    │   (PM, PO, SM,  │
└─────────────────┘    └─────────────────┘    │   DEV, QA, etc) │
                                              └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Redis
- PostgreSQL
- MongoDB

### Installation

1. **Clone and setup**:
```bash
git clone <repository>
cd ai-dev
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment setup**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Database setup**:
```bash
docker-compose up -d postgres redis mongodb
alembic upgrade head
```

4. **Run the API**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. **Access the API**:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Ready Check: http://localhost:8000/ready

## 📋 API Endpoints

### Core Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/agents/{agent}/trigger` | POST | Trigger agent action |
| `/v1/agents/{agent}/status` | GET | Get agent status |
| `/v1/agents/register` | POST | Register new agent |
| `/v1/issues` | POST | Create new issue/story |
| `/v1/specs` | POST | Submit/retrieve specs |
| `/v1/code/commit` | POST | DEV agent pushes code |
| `/v1/tests/run` | POST | QA agent runs tests |
| `/v1/reviews/submit` | POST | AR agent submits review |
| `/v1/deploy` | POST | AD agent triggers deployment |
| `/v1/wellness/checkin` | POST | Morale Booster logs mood |
| `/v1/dashboard/metrics` | GET | Retrieve dashboard metrics |

### System Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | System health status |
| `/ready` | GET | System readiness status |
| `/metrics` | GET | Prometheus metrics |
| `/docs` | GET | Interactive API docs |

## 🔧 Configuration

Key environment variables:

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/agentic_agile
MONGODB_URL=mongodb://localhost:27017/agentic_agile
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Settings
API_V1_STR=/v1
PROJECT_NAME=Agentic Agile System API
VERSION=1.0.0
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_agents.py
```

## 📊 Monitoring

- **Health Checks**: `/health` and `/ready` endpoints
- **Metrics**: Prometheus metrics at `/metrics`
- **Logging**: Structured logging with trace IDs
- **Audit Trail**: All API calls logged with user context

## 🔐 Security

- **Authentication**: OAuth2/JWT tokens
- **Authorization**: Role-based access control (RBAC)
- **Encryption**: TLS/SSL for all traffic
- **Rate Limiting**: Per-agent quotas and burst protection
- **Input Validation**: Pydantic models for all inputs
- **SQL Injection Protection**: SQLAlchemy ORM

## 🚀 Deployment

### 🐳 Docker Compose (Recommended for Development & Demo)

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### ☸️ Kubernetes (Production)

```bash
# Quick deployment
kubectl create namespace agentic-agile
kubectl apply -f k8s/

# Or use Kustomize
kubectl apply -k k8s/

# Check deployment
kubectl get all -n agentic-agile
```

**📖 [Full Kubernetes Guide](k8s/README.md)**

### 🐍 Python Virtual Environment (Development)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run PM Agent
cd agents/pm_agent
python run.py
```

### 🚀 Cloud Deployment

#### AWS EKS
```bash
# Deploy to EKS
eksctl create cluster --name agentic-agile --region us-west-2
kubectl apply -f k8s/
```

#### Google GKE
```bash
# Deploy to GKE
gcloud container clusters create agentic-agile --zone us-central1-a
kubectl apply -f k8s/
```

#### Azure AKS
```bash
# Deploy to AKS
az aks create --resource-group myResourceGroup --name agentic-agile
kubectl apply -f k8s/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Documentation**: `/docs` endpoint
- **Issues**: Create GitHub issues
- **Discussions**: Use GitHub Discussions

---

**Built with ❤️ for the future of agile development** 