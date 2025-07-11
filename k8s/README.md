# 🚀 Kubernetes Deployment Guide

This directory contains Kubernetes manifests for deploying the Agentic Agile System in production environments.

## 📋 Prerequisites

- Kubernetes cluster (v1.20+)
- kubectl configured
- Docker registry access
- Helm (optional, for advanced deployments)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LoadBalancer  │    │   API Service   │    │   PM Agent      │
│   (External)    │◄──►│   (Internal)    │◄──►│   (Internal)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Hub       │    │   PostgreSQL    │    │   Redis         │
│   (3 replicas)  │    │   (StatefulSet) │    │   (StatefulSet) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Manifest Files

### API Hub
- `api-hub-deployment.yaml` - Main API application deployment
- `api-hub-service.yaml` - LoadBalancer and ClusterIP services
- `api-hub-configmap.yaml` - Non-sensitive configuration
- `api-hub-secrets.yaml` - Sensitive configuration (update before deployment)

### PM Agent
- `pm-agent-deployment.yaml` - PM Agent deployment
- `pm-agent-configmap.yaml` - Agent configuration

### Management
- `kustomization.yaml` - Kustomize configuration for easy deployment

## 🔧 Configuration

### 1. Update Secrets

**IMPORTANT:** Update the secrets in `api-hub-secrets.yaml` before deployment:

```bash
# Generate base64 encoded values
echo -n "your-database-url" | base64
echo -n "your-secret-key" | base64
```

### 2. Environment Variables

Key environment variables to configure:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `MONGODB_URL` | MongoDB connection string | Required |
| `REDIS_URL` | Redis connection string | Required |
| `DEBUG` | Enable debug mode | false |
| `LOG_LEVEL` | Logging level | INFO |

## 🚀 Deployment

### Quick Start

```bash
# 1. Create namespace
kubectl create namespace agentic-agile

# 2. Apply secrets (update first!)
kubectl apply -f api-hub-secrets.yaml

# 3. Deploy everything
kubectl apply -k .

# 4. Check status
kubectl get all -n agentic-agile
```

### Step-by-Step Deployment

```bash
# 1. Create namespace
kubectl create namespace agentic-agile

# 2. Apply ConfigMaps
kubectl apply -f api-hub-configmap.yaml
kubectl apply -f pm-agent-configmap.yaml

# 3. Apply Secrets (update first!)
kubectl apply -f api-hub-secrets.yaml

# 4. Deploy API Hub
kubectl apply -f api-hub-deployment.yaml
kubectl apply -f api-hub-service.yaml

# 5. Deploy PM Agent
kubectl apply -f pm-agent-deployment.yaml

# 6. Verify deployment
kubectl get pods -n agentic-agile
kubectl get services -n agentic-agile
```

## 🔍 Monitoring & Health Checks

### Health Endpoints
- API Hub: `GET /health`
- PM Agent: `GET /health` (port 8000)

### Monitoring Commands

```bash
# Check pod status
kubectl get pods -n agentic-agile

# Check service endpoints
kubectl get endpoints -n agentic-agile

# View logs
kubectl logs -f deployment/agentic-agile-api -n agentic-agile
kubectl logs -f deployment/pm-agent -n agentic-agile

# Check resource usage
kubectl top pods -n agentic-agile
```

## 🔒 Security Features

### Implemented Security Measures
- Non-root containers
- Read-only root filesystem (where possible)
- Resource limits and requests
- Network policies (recommended)
- Secrets management

### Additional Security Recommendations

```yaml
# Network Policy (create network-policy.yaml)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
spec:
  podSelector:
    matchLabels:
      app: agentic-agile-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: pm-agent
    ports:
    - protocol: TCP
      port: 8000
```

## 📊 Scaling

### Horizontal Pod Autoscaling

```bash
# Create HPA for API Hub
kubectl autoscale deployment agentic-agile-api \
  --cpu-percent=70 \
  --min=3 \
  --max=10 \
  -n agentic-agile

# Create HPA for PM Agent
kubectl autoscale deployment pm-agent \
  --cpu-percent=80 \
  --min=2 \
  --max=5 \
  -n agentic-agile
```

### Manual Scaling

```bash
# Scale API Hub
kubectl scale deployment agentic-agile-api --replicas=5 -n agentic-agile

# Scale PM Agent
kubectl scale deployment pm-agent --replicas=3 -n agentic-agile
```

## 🔄 Updates & Rollouts

### Rolling Updates

```bash
# Update image
kubectl set image deployment/agentic-agile-api \
  api=agentic-agile-api:v1.1.0 \
  -n agentic-agile

# Monitor rollout
kubectl rollout status deployment/agentic-agile-api -n agentic-agile

# Rollback if needed
kubectl rollout undo deployment/agentic-agile-api -n agentic-agile
```

## 🗑️ Cleanup

```bash
# Delete all resources
kubectl delete namespace agentic-agile

# Or delete individually
kubectl delete -k .
```

## ☁️ Cloud-Specific Deployments

### AWS EKS
```bash
# Use AWS Load Balancer Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/v2_4_7_full.yaml
```

### Google GKE
```bash
# Enable Workload Identity
gcloud container clusters update CLUSTER_NAME \
  --workload-pool=PROJECT_ID.svc.id.goog
```

### Azure AKS
```bash
# Enable Azure CNI
az aks update \
  --resource-group RESOURCE_GROUP \
  --name CLUSTER_NAME \
  --network-plugin azure
```

## 🐛 Troubleshooting

### Common Issues

1. **Pods not starting**
   ```bash
   kubectl describe pod <pod-name> -n agentic-agile
   kubectl logs <pod-name> -n agentic-agile
   ```

2. **Services not accessible**
   ```bash
   kubectl get endpoints -n agentic-agile
   kubectl describe service <service-name> -n agentic-agile
   ```

3. **Resource issues**
   ```bash
   kubectl top pods -n agentic-agile
   kubectl describe node <node-name>
   ```

### Debug Commands

```bash
# Port forward for local access
kubectl port-forward svc/agentic-agile-api-service 8080:80 -n agentic-agile

# Exec into container
kubectl exec -it <pod-name> -n agentic-agile -- /bin/bash

# Check events
kubectl get events -n agentic-agile --sort-by='.lastTimestamp'
```

## 📚 Additional Resources

- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [Production Checklist](https://kubernetes.io/docs/tasks/administer-cluster/cluster-management/)

## 🤝 Support

For deployment issues:
1. Check the troubleshooting section above
2. Review pod logs and events
3. Verify configuration and secrets
4. Check resource availability 