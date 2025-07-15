# Agentic Agile System

A comprehensive autonomous agent system for agile project management, featuring multiple specialized AI agents working together to handle project management, development, testing, and team wellness.

## 🌟 Features

### Core System
- **Multi-Agent Architecture**: 8 specialized autonomous agents (PM, PO, SM, DEV, QA, AR, AD, MB)
- **Central API Hub**: FastAPI-based orchestration and communication
- **Event-Driven Architecture**: Redis Streams for async, decoupled agent communication
- **Memory System**: Persistent agent memory with PostgreSQL and MongoDB
- **Git Integration**: Automated GitHub webhook handling and repository management

### Frontend Dashboard
- **Modern React Interface**: TypeScript-based dashboard with real-time updates
- **Agent Management**: Monitor and control autonomous agents
- **Issue Tracking**: Comprehensive issue management with filtering and search
- **Wellness Monitoring**: Team health check-ins and wellness trends
- **Event System**: Real-time event monitoring and system communications
- **Settings**: Comprehensive system configuration options

### Infrastructure
- **Docker & Kubernetes**: Containerized deployment with K8s manifests
- **CI/CD Pipeline**: GitHub Actions with automated testing and deployment
- **Monitoring**: Health checks, logging, and performance metrics
- **Security**: Authentication, rate limiting, and secure communication

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.9+ (for backend development)
- Git

### 1. Clone and Setup
```bash
git clone <repository-url>
cd ai-dev
cp env.example .env
# Edit .env with your configuration
```

### 2. Start the System
```bash
# Start all services (API, Frontend, Database, Agents)
docker-compose up -d

# Or start individual components
docker-compose up api-hub frontend postgres redis mongo
```

### 3. Access the System
- **Frontend Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
ai-dev/
├── app/                    # FastAPI backend
│   ├── api/v1/            # API endpoints
│   ├── core/              # Core functionality
│   ├── models/            # Data models
│   └── main.py           # Application entry point
├── frontend/              # React TypeScript dashboard
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   └── main.tsx      # Entry point
│   ├── package.json      # Frontend dependencies
│   └── Dockerfile        # Frontend container
├── agents/               # Autonomous agent implementations
│   ├── pm_agent/         # Project Manager Agent
│   ├── po/              # Product Owner Agent
│   ├── sm/              # Scrum Master Agent
│   ├── dev/             # Developer Agent
│   ├── qa/              # QA Agent
│   ├── ar/              # Architect Agent
│   ├── ad/              # Admin Agent
│   └── mb/              # Morale Booster Agent
├── k8s/                 # Kubernetes manifests
├── scripts/             # Utility scripts
├── docker-compose.yml   # Development environment
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables
```bash
# Core Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/agentic_agile
REDIS_URL=redis://localhost:6379
MONGODB_URL=mongodb://localhost:27017/agentic_agile

# API Keys
ANTHROPIC_API_KEY=your_anthropic_key
GITHUB_TOKEN=your_github_token
SLACK_WEBHOOK_URL=your_slack_webhook

# GitHub Integration
GITHUB_WEBHOOK_SECRET=your_webhook_secret
GITHUB_REPO=your_username/your_repo
```

### Frontend Configuration
The frontend is configured to proxy API requests to the backend. Configuration is in `frontend/vite.config.ts`.

## 🏗️ Development

### Backend Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Agent Development
Each agent is a standalone service. See individual agent directories for specific setup instructions.

## 📊 Monitoring & Health

### Health Checks
- API Hub: `GET /health`
- Individual Agents: `GET /health` (agent-specific endpoints)
- Database: Automatic health checks in Docker Compose

### Logging
- Structured logging with structlog
- Log aggregation via Docker Compose
- Agent-specific log files in `logs/` directory

## 🔒 Security

### Authentication & Authorization
- JWT-based authentication
- Role-based access control
- API rate limiting
- Secure communication between agents

### Data Protection
- Encrypted data transmission
- Secure credential management
- Regular security updates

## 🚀 Deployment

### Docker Deployment
```bash
# Production build
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale pm-agent=2 --scale dev-agent=3
```

### Kubernetes Deployment
```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n agentic-agile
```

### CI/CD Pipeline
- Automated testing on pull requests
- Semantic versioning with changelog generation
- Automated deployment to staging/production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📚 Documentation

- [Functional Technical Specification](FUNCTIONAL_TECHNICAL_SPEC.md)
- [Agent Behaviors](agents/AGENT_BEHAVIORS.md)
- [Memory System Summary](MEMORY_SYSTEM_SUMMARY.md)
- [Deployment Summary](DEPLOYMENT_SUMMARY.md)
- [Setup Guide](SETUP.md)
- [Maintenance Checklist](MAINTENANCE_CHECKLIST.md)

## 🆘 Support

- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Documentation**: Check the docs directory
- **Community**: Join our Slack workspace

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with FastAPI, React, and modern DevOps practices
- Inspired by agile methodologies and autonomous systems
- Powered by Claude 3.7 Sonnet (Anthropic)

---

**Ready to revolutionize your agile workflow?** 🚀

Start with `docker-compose up -d` and visit http://localhost:3000 to see your autonomous agents in action! 

## Planned Enhancements: Diagnostics, Setup Checklist, and Recovery

- **Diagnostic Program:** Automated tool to check system health, configuration, and integration status, with actionable reports.
- **Setup Checklist:** Automated/manual checklist to ensure all environment variables, dependencies, and services are ready before deployment or development.
- **Recovery System:** Self-healing and recovery features to detect, restart, and restore failed components, with notifications and backup integration.

These features are part of the Agentic Agile System's commitment to first-principles, self-healing, and robust operations. 