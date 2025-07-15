# 🔄 Agentic Agile System - Maintenance Checklist

## 📅 **Regular Maintenance Schedule**

### **Daily Tasks**
- [ ] Check system logs for errors
- [ ] Verify all agents are running
- [ ] Monitor memory system backups
- [ ] Check API health endpoints

### **Weekly Tasks**
- [ ] Run system health check script
- [ ] Review security scan results
- [ ] Update dependencies if needed
- [ ] Test all agent functionalities
- [ ] Review and clean up logs

### **Monthly Tasks**
- [ ] Comprehensive system audit
- [ ] Update documentation
- [ ] Review and update GitHub templates
- [ ] Check deployment configurations
- [ ] Performance optimization review

### **Quarterly Tasks**
- [ ] Major version updates
- [ ] Security policy review
- [ ] Backup strategy review
- [ ] Team training and onboarding
- [ ] System architecture review

---

## 🔍 **System Health Checks**

### **Agent Status Check**
```bash
# Run the update script
python scripts/update_system.py

# Check individual agents
cd agents/pm_agent && python main.py --health
cd agents/qa_agent && python main.py --health
# ... repeat for all agents
```

### **Infrastructure Check**
```bash
# Docker health
docker-compose ps
docker-compose logs --tail=50

# Kubernetes health (if deployed)
kubectl get pods -n agentic-agile
kubectl logs -f deployment/agentic-agile-api -n agentic-agile

# Database health
docker exec -it agentic_agile_postgres pg_isready
```

### **Security Check**
```bash
# Run security scans
bandit -r app/ -f json -o bandit-report.json
safety check --json --output safety-report.json

# Check for vulnerabilities
pip-audit
```

---

## 📦 **Dependency Management**

### **Check for Updates**
```bash
# List outdated packages
pip list --outdated

# Update specific packages
pip install --upgrade package-name

# Update all packages (be careful!)
pip-review --auto
```

### **Security Updates**
```bash
# Check for security vulnerabilities
safety check

# Update vulnerable packages
safety check --full-report | grep -E "VULNERABILITY" | awk '{print $2}' | xargs pip install --upgrade
```

---

## 🗄️ **Memory System Maintenance**

### **Backup Verification**
```bash
# Run manual backup
python scripts/backup_memory.py

# Verify backup integrity
python scripts/backup_memory.py --verify

# Clean up old backups
python scripts/backup_memory.py --cleanup --days=30
```

### **Memory Optimization**
```bash
# Check memory usage
python -c "from app.models.corporate_memory import CorporateMemory; print(f'Total memories: {CorporateMemory.query.count()}')"

# Archive old memories
python scripts/archive_old_memories.py --older-than=90-days

# Optimize database
python scripts/optimize_database.py
```

---

## 🚀 **Deployment Maintenance**

### **Docker Maintenance**
```bash
# Clean up unused images
docker system prune -a

# Update base images
docker-compose pull
docker-compose build --no-cache

# Check disk usage
docker system df
```

### **Kubernetes Maintenance**
```bash
# Update deployments
kubectl rollout restart deployment/agentic-agile-api -n agentic-agile

# Check resource usage
kubectl top pods -n agentic-agile

# Clean up old resources
kubectl delete pods --field-selector=status.phase=Succeeded -n agentic-agile
```

---

## 📊 **Monitoring and Alerts**

### **Health Endpoints**
- API Health: `GET /health`
- Agent Health: `GET /agents/{agent}/health`
- Memory Health: `GET /memory/stats`
- System Metrics: `GET /metrics`

### **Log Monitoring**
```bash
# Check application logs
docker-compose logs -f api

# Check agent logs
docker-compose logs -f pm-agent

# Check system logs
journalctl -u agentic-agile -f
```

### **Performance Monitoring**
```bash
# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/health"

# Monitor database performance
docker exec -it agentic_agile_postgres psql -U user -d agentic_agile -c "SELECT * FROM pg_stat_activity;"
```

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Agent Not Responding**
```bash
# Check agent status
curl http://localhost:8001/health

# Restart agent
docker-compose restart pm-agent

# Check logs
docker-compose logs pm-agent
```

#### **Database Connection Issues**
```bash
# Check database status
docker-compose ps postgres

# Restart database
docker-compose restart postgres

# Check connection
docker exec -it agentic_agile_postgres psql -U user -d agentic_agile -c "SELECT 1;"
```

#### **Memory System Issues**
```bash
# Check memory system
curl http://localhost:8000/memory/stats

# Restart API
docker-compose restart api

# Check database tables
docker exec -it agentic_agile_postgres psql -U user -d agentic_agile -c "\dt"
```

---

## 📈 **Performance Optimization**

### **Database Optimization**
```bash
# Analyze table statistics
docker exec -it agentic_agile_postgres psql -U user -d agentic_agile -c "ANALYZE;"

# Check slow queries
docker exec -it agentic_agile_postgres psql -U user -d agentic_agile -c "SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"
```

### **Application Optimization**
```bash
# Check memory usage
docker stats

# Optimize Python performance
python -m cProfile -o profile.stats scripts/update_system.py

# Check for memory leaks
python -m memory_profiler scripts/update_system.py
```

---

## 🔐 **Security Maintenance**

### **Regular Security Tasks**
- [ ] Update SSL certificates
- [ ] Rotate API keys and secrets
- [ ] Review access logs
- [ ] Update security policies
- [ ] Run penetration tests

### **Security Commands**
```bash
# Check for security vulnerabilities
bandit -r . -f json -o bandit-report.json
safety check --json --output safety-report.json

# Update security packages
pip install --upgrade cryptography requests urllib3

# Check SSL certificates
openssl s_client -connect localhost:8000 -servername localhost
```

---

## 📝 **Documentation Updates**

### **Required Documentation Reviews**
- [ ] README.md - Update setup instructions
- [ ] SETUP.md - Update deployment guides
- [ ] API documentation - Update endpoints
- [ ] Agent documentation - Update behaviors
- [ ] Security documentation - Update policies

### **Documentation Commands**
```bash
# Generate API documentation
pydoc-markdown --render-toc

# Update README badges
python scripts/update_readme_badges.py

# Check documentation links
python scripts/check_documentation_links.py
```

---

## 🎯 **Quality Assurance**

### **Testing Checklist**
- [ ] Run unit tests: `pytest tests/`
- [ ] Run integration tests: `pytest tests/integration/`
- [ ] Run performance tests: `pytest tests/performance/`
- [ ] Run security tests: `pytest tests/security/`
- [ ] Manual testing of all agents

### **Code Quality**
```bash
# Run linting
flake8 app/ agents/ tests/
black --check app/ agents/ tests/
isort --check-only app/ agents/ tests/

# Run type checking
mypy app/ agents/

# Check code coverage
pytest --cov=app --cov=agents --cov-report=html
```

---

## 📞 **Support and Escalation**

### **When to Escalate**
- [ ] System downtime > 15 minutes
- [ ] Data loss or corruption
- [ ] Security breach
- [ ] Performance degradation > 50%
- [ ] Multiple agent failures

### **Escalation Contacts**
- **Primary Contact**: [Your Name] - [Your Email]
- **Backup Contact**: [Backup Name] - [Backup Email]
- **Emergency Contact**: [Emergency Name] - [Emergency Phone]

### **Escalation Process**
1. **Immediate**: Stop the issue from spreading
2. **Assessment**: Evaluate the impact and scope
3. **Communication**: Notify stakeholders
4. **Resolution**: Fix the root cause
5. **Documentation**: Record the incident and lessons learned

---

## Slack Integration

- [ ] Create a Slack channel for the project
- [ ] Create a Slack App/Bot and add to workspace
- [ ] Add Bot User OAuth Token to .env and env.example as SLACK_BOT_TOKEN
- [ ] Test Slack notifications using scripts/send_slack_test.py
- [ ] Document Slack integration in README

## ✅ **Maintenance Completion Checklist**

After completing maintenance:

- [ ] All health checks passed
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Backups verified
- [ ] Team notified of changes
- [ ] Maintenance log updated
- [ ] Next maintenance scheduled

---

**Last Updated**: December 2024  
**Next Review**: January 2025  
**Maintained By**: [Your Name] 

# Environment Variable and Service Validation (First Step)

Before troubleshooting or deploying, always validate your environment and services:

1. Ensure your `.env` file is present and all required variables are set (see below).
2. Run the validation script:

   ```sh
   python scripts/validate_env_and_services.py
   ```

3. If any variables are missing or services are not running, fix them before proceeding.

## Required Environment Variables Checklist

- [ ] DATABASE_URL
- [ ] MONGODB_URL
- [ ] REDIS_URL
- [ ] SECRET_KEY
- [ ] ALGORITHM
- [ ] ACCESS_TOKEN_EXPIRE_MINUTES
- [ ] SLACK_WEBHOOK_URL
- [ ] GITHUB_WEBHOOK_SECRET
- [ ] API_BASE_URL
- [ ] ANTHROPIC_API_KEY
- [ ] GITHUB_TOKEN (if using GitHub agents)
- [ ] GITHUB_REPO (if using GitHub agents)
- [ ] GITLAB_WEBHOOK_TOKEN (if using GitLab)

--- 