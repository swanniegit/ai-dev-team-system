# 🔍 AR Agent - Architecture Review Agent

A comprehensive Architecture Review agent that implements all 10 AR behaviors with Claude 3.7 Sonnet integration for intelligent code review and architectural decisions.

## 🎯 Mission

Deliver world-class code review and architectural guidance through AI-powered analysis, security assessment, performance optimization, and best practices enforcement.

## ✨ Core Features

- **Intelligent Code Review**: Claude 3.7 Sonnet analyzes code for quality, security, and best practices
- **Architecture Assessment**: Comprehensive architectural design review and recommendations
- **Security Analysis**: Automated security vulnerability detection and assessment
- **Performance Review**: Performance bottleneck identification and optimization suggestions
- **Maintainability Analysis**: Code maintainability and technical debt assessment
- **Testability Review**: Code testability and testing strategy recommendations
- **Documentation Review**: Documentation quality and completeness assessment
- **Best Practices Enforcement**: Industry best practices validation and recommendations
- **Dependency Review**: Security and maintenance analysis of dependencies
- **Compliance Review**: Regulatory and compliance requirement validation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Hub       │    │   AR Agent      │    │   Claude 3.7    │
│   (FastAPI)     │◄──►│   (Python)      │◄──►│   Sonnet        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub/GitLab │    │   Review        │    │   Security      │
│   Integration   │    │   Database      │    │   Tools         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Claude API Key
- API Hub running

### Installation

1. **Clone and setup**:
```bash
cd agents/ar
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment setup**:
```bash
export CLAUDE_API_KEY="your-claude-api-key"
export API_HUB_URL="http://localhost:8000"
export GITHUB_TOKEN="your-github-token"  # Optional
export GITLAB_TOKEN="your-gitlab-token"  # Optional
```

3. **Run the AR Agent**:
```bash
python main.py
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f ar-agent

# Stop services
docker-compose down
```

## 📋 AR Behaviors (10 Total)

### **Code Review & Quality**
- [x] **Code Review**: Real-time code quality and best practices review
- [x] **Architecture Review**: System architecture design assessment
- [x] **Security Review**: Security vulnerability detection and analysis
- [x] **Performance Review**: Performance optimization and bottleneck identification

### **Quality Assurance**
- [x] **Maintainability Review**: Code maintainability and technical debt analysis
- [x] **Testability Review**: Code testability and testing strategy assessment
- [x] **Documentation Review**: Documentation quality and completeness review
- [x] **Best Practices Review**: Industry best practices validation

### **Dependencies & Compliance**
- [x] **Dependency Review**: Security and maintenance analysis of dependencies
- [x] **Compliance Review**: Regulatory and compliance requirement validation

## 🔧 Configuration

### Environment Variables

```env
# Required
CLAUDE_API_KEY=your-claude-api-key
API_HUB_URL=http://localhost:8000

# Optional
GITHUB_TOKEN=your-github-token
GITLAB_TOKEN=your-gitlab-token
GITLAB_API_URL=your-gitlab-api-url
LOG_LEVEL=INFO
```

### Quality Standards

```python
# Default quality thresholds
min_code_quality_score = 7.0  # Minimum code quality score (1-10)
max_complexity_threshold = 10  # Maximum cyclomatic complexity
min_test_coverage = 80.0  # Minimum test coverage percentage
max_technical_debt = 5.0  # Maximum technical debt hours per 1000 lines
```

### Supported Languages

- Python, JavaScript, TypeScript, Java, C#, Go, Rust, PHP, Ruby, Swift

## 📊 Review Categories

The AR Agent reviews code across multiple categories:

- **Code Quality**: Readability, structure, and coding standards
- **Security**: Vulnerability detection and security best practices
- **Performance**: Optimization opportunities and bottlenecks
- **Maintainability**: Code maintainability and technical debt
- **Testability**: Testing strategy and test coverage
- **Architecture**: Design patterns and architectural decisions
- **Documentation**: Code documentation and comments
- **Best Practices**: Industry standards and conventions
- **Dependencies**: Security and maintenance of external dependencies
- **Compliance**: Regulatory and compliance requirements

## 🔍 API Integration

### API Hub Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/reviews/code` | POST | Store code review results |
| `/v1/reviews/architecture` | POST | Store architecture review results |
| `/v1/reviews/security` | POST | Store security review results |
| `/v1/reviews/performance` | POST | Store performance review results |
| `/v1/reviews/dependencies` | POST | Store dependency review results |

### External Integrations

- **GitHub**: Pull request review and code analysis
- **GitLab**: Merge request review and code analysis
- **Security Tools**: Vulnerability scanning integration
- **Code Quality Tools**: Static analysis integration

## 🧪 Testing

```bash
# Run AR Agent tests
python test_ar_agent.py

# Test specific behaviors
python -c "from main import ARAgent; agent = ARAgent(); print(agent.get_status())"
```

## 📈 Monitoring

### Health Checks

- **Agent Status**: `/health` endpoint (port 8004)
- **Behavior Status**: Real-time behavior execution tracking
- **Review Queue**: Pending review items monitoring
- **Review Results**: Completed review statistics

### Logging

```bash
# View AR Agent logs
tail -f logs/ar_agent.log

# Docker logs
docker-compose logs -f ar-agent
```

## 🔐 Security

- **Non-root Container**: Runs as non-root user
- **Secrets Management**: Environment variable configuration
- **Network Security**: Internal service communication
- **Input Validation**: All inputs validated and sanitized

## 🚀 Deployment Options

### Docker Compose (Recommended)
```bash
docker-compose up -d
```

### Kubernetes
```bash
kubectl apply -f ../../k8s/ar-agent-deployment.yaml
```

### Python Virtual Environment
```bash
python main.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new behaviors
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Documentation**: This README
- **Issues**: Create GitHub issues
- **Logs**: Check `logs/ar_agent.log`

---

## 🎯 Next Steps

1. **Integrate with real code repositories** (GitHub, GitLab, etc.)
2. **Add more language support** (Kotlin, Scala, etc.)
3. **Implement advanced security scanning** (SAST, DAST, etc.)
4. **Add more compliance frameworks** (SOC2, HIPAA, etc.)
5. **Create custom review templates** for different project types 