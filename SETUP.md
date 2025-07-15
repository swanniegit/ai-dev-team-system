# 🚀 Agentic Agile System - Setup Guide

# Environment Variable and Service Validation (First Step)

Before setup or deployment, always validate your environment and services:

1. Copy `env.example` to `.env` if you haven't already.
2. Fill in all required environment variables in `.env` (see checklist below).
3. Run the validation script:

   ```sh
   python scripts/validate_env_and_services.py
   ```

4. If any variables are missing or services are not running, fix them before proceeding.

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

## 🔧 **Step 1: Fix Python Installation**

### **Option A: Install Python from Microsoft Store (Recommended for Windows)**
1. Open **Microsoft Store**
2. Search for **"Python 3.11"**
3. Click **"Get"** or **"Install"**
4. Wait for installation to complete
5. **Restart your terminal/PowerShell**

### **Option B: Install Python from python.org**
1. Go to https://www.python.org/downloads/
2. Click **"Download Python 3.11.x"**
3. **IMPORTANT**: Check ✅ **"Add Python to PATH"**
4. Click **"Install Now"**
5. **Restart your terminal/PowerShell**

## 🔍 **Step 2: Verify Python Installation**

Open a **new** terminal/PowerShell and run:
```bash
python --version
# Should show: Python 3.11.x

# Or try:
py --version
```

## 📦 **Step 3: Create Virtual Environment**

```bash
# Navigate to your project
cd C:\GitHub\ai-dev

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# You should see (venv) at the start of your prompt
```

## 📋 **Step 4: Install Dependencies**

### **Option A: Use Simplified Requirements (Recommended)**
```bash
pip install -r requirements-simple.txt
```

### **Option B: Use Full Requirements**
```bash
pip install -r requirements.txt
```

### **Option C: Install Core Dependencies Only**
```bash
pip install fastapi uvicorn[standard] pydantic sqlalchemy
```

## 🐳 **Step 5: Start with Docker (Recommended for Production)**

### **Install Docker Desktop**
1. Download from: https://www.docker.com/products/docker-desktop/
2. Install and restart your computer
3. Start Docker Desktop

### **Start the System**
```bash
# Start all services (API + Databases)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api

# The API will be available at: http://localhost:8000
```

### **Run PM Agent**
```bash
# Navigate to PM Agent directory
cd agents/pm_agent

# Build and run PM Agent
docker-compose up -d

# Check agent status
docker-compose logs -f pm-agent
```

## 🚀 **Step 6: Run the Application**

### **🐳 With Docker (Recommended):**
```bash
# Start API Hub
docker-compose up -d

# Start PM Agent
cd agents/pm_agent
docker-compose up -d

# Check everything is running
docker-compose ps
```

### **🐍 With Python (Development):**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Start the API
python start.py

# In another terminal, start PM Agent
cd agents/pm_agent
python run.py
```

### **☸️ With Kubernetes (Production):**
```bash
# Deploy to Kubernetes
kubectl create namespace agentic-agile
kubectl apply -f k8s/

# Check deployment
kubectl get all -n agentic-agile
```

## 🔍 **Step 7: Test the System**

### **Test API Hub:**
1. Open browser: http://localhost:8000
2. API Docs: http://localhost:8000/docs
3. Health Check: http://localhost:8000/health

### **Test PM Agent:**
```bash
# Test PM Agent functionality
cd agents/pm_agent
docker-compose run --rm pm-agent-test

# Or with Python
python test_agent.py
```

### **Create Test Issues:**
```bash
# Create a test issue via API
curl -X POST "http://localhost:8000/v1/issues/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Issue",
    "description": "This is a test issue for the PM Agent",
    "priority": "medium"
  }'
```

## ❌ **Common Issues & Solutions**

### **Issue: "python is not recognized"**
**Solution**: Install Python and add to PATH

### **Issue: "pip is not recognized"**
**Solution**: 
```bash
python -m pip install --upgrade pip
```

### **Issue: "Microsoft Visual C++ 14.0 is required"**
**Solution**: Install Visual Studio Build Tools or use Docker

### **Issue: "psycopg2 installation failed"**
**Solution**: Use Docker or install PostgreSQL development headers

### **Issue: "Permission denied"**
**Solution**: Run as Administrator or use virtual environment

## 🆘 **Still Having Issues?**

1. **Use Docker** - It's the most reliable option
2. **Try WSL2** - Windows Subsystem for Linux
3. **Use Python 3.11** - Most stable version
4. **Check PATH** - Make sure Python is in your system PATH

## 🚀 **Production Deployment**

### **🐳 Docker Compose (Recommended)**
```bash
# Production environment variables
cp env.example .env
# Edit .env with production values

# Start with production settings
docker-compose -f docker-compose.yml up -d

# Monitor logs
docker-compose logs -f
```

### **☸️ Kubernetes (Enterprise)**
```bash
# Update secrets first
kubectl apply -f k8s/api-hub-secrets.yaml

# Deploy everything
kubectl apply -k k8s/

# Check deployment
kubectl get all -n agentic-agile
```

### **☁️ Cloud Deployment**

#### **AWS EKS**
```bash
# Create EKS cluster
eksctl create cluster --name agentic-agile --region us-west-2

# Deploy application
kubectl apply -f k8s/
```

#### **Google GKE**
```bash
# Create GKE cluster
gcloud container clusters create agentic-agile --zone us-central1-a

# Deploy application
kubectl apply -f k8s/
```

#### **Azure AKS**
```bash
# Create AKS cluster
az aks create --resource-group myResourceGroup --name agentic-agile

# Deploy application
kubectl apply -f k8s/
```

## 📊 **Monitoring & Health Checks**

### **Health Endpoints**
- API Hub: `GET /health`
- PM Agent: `GET /health` (port 8000)

### **Monitoring Commands**
```bash
# Docker
docker-compose ps
docker-compose logs -f

# Kubernetes
kubectl get pods -n agentic-agile
kubectl logs -f deployment/agentic-agile-api -n agentic-agile
```

## 📞 **Need Help?**

- Check the logs for specific error messages
- Try the simplified requirements first
- Use Docker if Python setup is problematic
- The API will work the same way regardless of installation method
- **📖 [Full Kubernetes Guide](k8s/README.md)**
- **📖 [PM Agent Documentation](agents/pm_agent/README.md)** 