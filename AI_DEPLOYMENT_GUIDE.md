# 🚀 Shikshak Mitra AI - Advanced Deployment Guide

## 🏗️ Production-Ready AI Infrastructure

### Cloud Architecture Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                        Load Balancer (AWS ALB)                  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────┼───────────────────────────────────────────┐
│                 API Gateway                                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │CV Service│   │NLP Service│  │ML Service│
   │(GPU Pods)│   │(CPU Pods) │  │(TPU Pods)│
   └─────────┘   └─────────┘   └─────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
              ┌───────▼───────┐
              │  Message Queue │
              │    (Redis)     │
              └───────┬───────┘
                      │
              ┌───────▼───────┐
              │   Database    │
              │ (PostgreSQL)  │
              └───────────────┘
```

## 🐳 Docker Configuration

### Multi-Stage AI Service Dockerfile
```dockerfile
# AI Service Dockerfile
FROM nvidia/cuda:11.8-devel-ubuntu20.04 as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    opencv-python \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# AI Models stage
FROM base as ai-models
WORKDIR /app/models

# Download pre-trained models
RUN wget https://github.com/ultralytics/yolov8/releases/download/v8.0.0/yolov8n.pt
RUN wget https://huggingface.co/bert-base-uncased/resolve/main/pytorch_model.bin

# Production stage
FROM base as production
WORKDIR /app

COPY --from=ai-models /app/models ./models
COPY src/ ./src/
COPY config/ ./config/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose for Development
```yaml
version: '3.8'

services:
  # AI Computer Vision Service
  cv-service:
    build:
      context: ./AI_Video_Analyzer
      dockerfile: Dockerfile.cv
    ports:
      - "8001:8000"
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - MODEL_PATH=/app/models/yolov8n.pt
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  # NLP Service
  nlp-service:
    build:
      context: ./AI_Voice_Analysis
      dockerfile: Dockerfile.nlp
    ports:
      - "8002:8000"
    environment:
      - TRANSFORMERS_CACHE=/app/cache
      - MODEL_NAME=bert-base-uncased
    volumes:
      - ./cache:/app/cache

  # RAG System
  rag-service:
    build:
      context: ./RAG_System
      dockerfile: Dockerfile
    ports:
      - "8003:8000"
    environment:
      - VECTOR_DB_PATH=/app/data/vector_db
      - EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
    volumes:
      - ./knowledge_base:/app/knowledge_base

  # Redis for caching and message queue
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # PostgreSQL for persistent data
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: shikshak_ai
      POSTGRES_USER: ai_user
      POSTGRES_PASSWORD: secure_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Monitoring with Prometheus
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

  # Grafana for visualization
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  redis_data:
  postgres_data:
  grafana_data:
```

## ☸️ Kubernetes Deployment

### AI Service Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-cv-service
  labels:
    app: ai-cv-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-cv-service
  template:
    metadata:
      labels:
        app: ai-cv-service
    spec:
      containers:
      - name: cv-service
        image: shikshak-ai/cv-service:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
            nvidia.com/gpu: 1
          limits:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: 1
        env:
        - name: MODEL_PATH
          value: "/app/models/yolov8n.pt"
        - name: REDIS_URL
          value: "redis://redis-service:6379"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: ai-cv-service
spec:
  selector:
    app: ai-cv-service
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
```

### Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-cv-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-cv-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: inference_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
```

## 🌐 AWS Infrastructure as Code (Terraform)

### Main Infrastructure
```hcl
# main.tf
provider "aws" {
  region = var.aws_region
}

# EKS Cluster for AI Services
module "eks" {
  source = "terraform-aws-modules/eks/aws"
  
  cluster_name    = "shikshak-ai-cluster"
  cluster_version = "1.27"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  # GPU Node Group for CV/ML workloads
  eks_managed_node_groups = {
    gpu_nodes = {
      min_size     = 2
      max_size     = 10
      desired_size = 3
      
      instance_types = ["p3.2xlarge", "p3.8xlarge"]
      
      k8s_labels = {
        workload = "gpu-intensive"
      }
      
      taints = {
        gpu = {
          key    = "nvidia.com/gpu"
          value  = "true"
          effect = "NO_SCHEDULE"
        }
      }
    }
    
    cpu_nodes = {
      min_size     = 3
      max_size     = 20
      desired_size = 5
      
      instance_types = ["c5.2xlarge", "c5.4xlarge"]
      
      k8s_labels = {
        workload = "cpu-intensive"
      }
    }
  }
}

# RDS for persistent data
resource "aws_db_instance" "ai_database" {
  identifier = "shikshak-ai-db"
  
  engine         = "postgres"
  engine_version = "15.3"
  instance_class = "db.r6g.xlarge"
  
  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_type         = "gp3"
  storage_encrypted    = true
  
  db_name  = "shikshak_ai"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = false
  final_snapshot_identifier = "shikshak-ai-final-snapshot"
  
  tags = {
    Name = "Shikshak AI Database"
  }
}

# ElastiCache Redis for caching
resource "aws_elasticache_replication_group" "ai_cache" {
  replication_group_id       = "shikshak-ai-cache"
  description                = "Redis cluster for AI caching"
  
  node_type                  = "cache.r6g.large"
  port                       = 6379
  parameter_group_name       = "default.redis7"
  
  num_cache_clusters         = 3
  automatic_failover_enabled = true
  multi_az_enabled          = true
  
  subnet_group_name = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.redis.id]
  
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  
  tags = {
    Name = "Shikshak AI Cache"
  }
}

# S3 for model storage and data lake
resource "aws_s3_bucket" "ai_models" {
  bucket = "shikshak-ai-models-${random_id.bucket_suffix.hex}"
  
  tags = {
    Name = "AI Models Storage"
  }
}

resource "aws_s3_bucket_versioning" "ai_models" {
  bucket = aws_s3_bucket.ai_models.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "ai_models" {
  bucket = aws_s3_bucket.ai_models.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# CloudFront for global content delivery
resource "aws_cloudfront_distribution" "ai_api" {
  origin {
    domain_name = aws_lb.main.dns_name
    origin_id   = "ALB-${aws_lb.main.name}"
    
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }
  
  enabled = true
  
  default_cache_behavior {
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "ALB-${aws_lb.main.name}"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
    
    forwarded_values {
      query_string = true
      headers      = ["Authorization", "Content-Type"]
      
      cookies {
        forward = "none"
      }
    }
  }
  
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  
  viewer_certificate {
    cloudfront_default_certificate = true
  }
  
  tags = {
    Name = "Shikshak AI CDN"
  }
}
```

## 📊 Monitoring and Observability

### Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "ai_alerts.yml"

scrape_configs:
  - job_name: 'ai-cv-service'
    static_configs:
      - targets: ['cv-service:8000']
    metrics_path: /metrics
    scrape_interval: 10s

  - job_name: 'ai-nlp-service'
    static_configs:
      - targets: ['nlp-service:8000']
    metrics_path: /metrics
    scrape_interval: 10s

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

### AI-Specific Alerts
```yaml
# ai_alerts.yml
groups:
- name: ai_model_performance
  rules:
  - alert: ModelAccuracyDrop
    expr: ai_model_accuracy < 0.90
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "AI model accuracy dropped below 90%"
      description: "Model {{ $labels.model_name }} accuracy is {{ $value }}"

  - alert: HighInferenceLatency
    expr: ai_inference_duration_seconds > 0.1
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "High AI inference latency detected"
      description: "Inference latency is {{ $value }}s for {{ $labels.model_name }}"

  - alert: GPUMemoryHigh
    expr: nvidia_gpu_memory_used_bytes / nvidia_gpu_memory_total_bytes > 0.9
    for: 1m
    labels:
      severity: warning
    annotations:
      summary: "GPU memory usage is high"
      description: "GPU {{ $labels.gpu }} memory usage is {{ $value | humanizePercentage }}"
```

## 🔧 CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/ai-deploy.yml
name: AI Model Deployment

on:
  push:
    branches: [main]
    paths: ['AI_Video_Analyzer/**', 'RAG_System/**']

jobs:
  test-models:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run model tests
      run: |
        pytest tests/test_cv_models.py --cov=src/
        pytest tests/test_nlp_models.py --cov=src/
    
    - name: Model validation
      run: |
        python scripts/validate_models.py

  build-and-deploy:
    needs: test-models
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-west-2
    
    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1
    
    - name: Build and push CV service
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        ECR_REPOSITORY: shikshak-ai/cv-service
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG ./AI_Video_Analyzer
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
    
    - name: Deploy to EKS
      run: |
        aws eks update-kubeconfig --name shikshak-ai-cluster
        kubectl set image deployment/ai-cv-service cv-service=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        kubectl rollout status deployment/ai-cv-service
```

## 🚀 Quick Deployment Commands

### Local Development
```bash
# Start all AI services locally
docker-compose up -d

# Check service health
curl http://localhost:8001/health  # CV Service
curl http://localhost:8002/health  # NLP Service
curl http://localhost:8003/health  # RAG Service

# View logs
docker-compose logs -f cv-service
```

### Production Deployment
```bash
# Deploy to AWS EKS
terraform init
terraform plan -var-file="production.tfvars"
terraform apply

# Deploy Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n shikshak-ai
kubectl get services -n shikshak-ai
```

### Monitoring Setup
```bash
# Install monitoring stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts

helm install prometheus prometheus-community/kube-prometheus-stack
helm install grafana grafana/grafana

# Access Grafana dashboard
kubectl port-forward svc/grafana 3000:80
```

## 📈 Performance Optimization

### GPU Optimization
```python
# CUDA optimization for PyTorch models
import torch

# Enable mixed precision training
scaler = torch.cuda.amp.GradScaler()

# Optimize memory usage
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.deterministic = False

# Use TensorRT for inference optimization
import torch_tensorrt

optimized_model = torch_tensorrt.compile(
    model,
    inputs=[torch.randn(1, 3, 224, 224).cuda()],
    enabled_precisions={torch.float, torch.half}
)
```

### Model Quantization
```python
# Post-training quantization
import torch.quantization as quantization

# Prepare model for quantization
model.qconfig = quantization.get_default_qconfig('fbgemm')
quantization.prepare(model, inplace=True)

# Calibrate with representative data
with torch.no_grad():
    for data in calibration_loader:
        model(data)

# Convert to quantized model
quantized_model = quantization.convert(model, inplace=False)
```

---

**🎯 Ready for Production Deployment!**

This comprehensive deployment guide ensures your Shikshak Mitra AI system is production-ready with enterprise-grade infrastructure, monitoring, and scalability.