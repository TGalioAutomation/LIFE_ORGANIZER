# 🚀 LIFE ORGANIZER - Production Deployment Guide

This guide covers deploying the Life Organizer application to production environments.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Web Server    │    │    Database     │
│    (Nginx)      │────│   (Gunicorn)    │────│  (PostgreSQL)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │   Django App    │              │
         │              │ (Life Organizer)│              │
         │              └─────────────────┘              │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Static Files  │    │   Media Files   │    │   Redis Cache   │
│   (CDN/S3)      │    │   (S3/Local)    │    │  (Sessions)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🐳 Docker Deployment

### 1. Create Dockerfile for Backend

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "life_organizer_project.wsgi:application"]
```

### 2. Create Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: life_organizer
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@db:5432/life_organizer
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/var/www/static
      - media_volume:/var/www/media
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### 3. Nginx Configuration

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream django {
        server web:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        client_max_body_size 100M;

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /var/www/static/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        location /media/ {
            alias /var/www/media/;
            expires 7d;
        }
    }
}
```

## ☁️ Cloud Deployment Options

### 1. AWS Deployment

#### Using AWS ECS with Fargate

```yaml
# ecs-task-definition.json
{
  "family": "life-organizer",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "life-organizer-web",
      "image": "your-account.dkr.ecr.region.amazonaws.com/life-organizer:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://user:pass@rds-endpoint:5432/life_organizer"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/life-organizer",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### Infrastructure as Code (Terraform)

```hcl
# main.tf
provider "aws" {
  region = "us-west-2"
}

# VPC and Networking
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "life-organizer-vpc"
  }
}

# RDS Database
resource "aws_db_instance" "postgres" {
  identifier     = "life-organizer-db"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_encrypted     = true
  
  db_name  = "life_organizer"
  username = "postgres"
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = true
  
  tags = {
    Name = "life-organizer-db"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "life-organizer"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "life-organizer-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets           = aws_subnet.public[*].id
  
  enable_deletion_protection = false
  
  tags = {
    Name = "life-organizer-alb"
  }
}
```

### 2. Google Cloud Platform (GCP)

#### Using Cloud Run

```yaml
# cloudbuild.yaml
steps:
  # Build the container image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/life-organizer:$COMMIT_SHA', './backend']
  
  # Push the container image to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/life-organizer:$COMMIT_SHA']
  
  # Deploy container image to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'life-organizer'
      - '--image'
      - 'gcr.io/$PROJECT_ID/life-organizer:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
```

### 3. Heroku Deployment

```yaml
# heroku.yml
build:
  docker:
    web: backend/Dockerfile
release:
  image: web
  command:
    - python manage.py migrate
    - python manage.py collectstatic --noinput
run:
  web: gunicorn --bind 0.0.0.0:$PORT life_organizer_project.wsgi:application
```

## 🔧 Production Configuration

### 1. Environment Variables

```bash
# .env.production
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:pass@host:5432/life_organizer
REDIS_URL=redis://redis-host:6379/0

# AWS S3 (for static/media files)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=life-organizer-static
AWS_S3_REGION_NAME=us-west-2

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Monitoring
SENTRY_DSN=https://your-sentry-dsn
```

### 2. Production Settings

```python
# backend/life_organizer_project/settings/production.py
from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Static files (AWS S3)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Security
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/life_organizer.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 📊 Monitoring and Maintenance

### 1. Health Checks

```python
# backend/life_organizer_project/health.py
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis

def health_check(request):
    """Health check endpoint for load balancers"""
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check Redis
        cache.set('health_check', 'ok', 10)
        cache.get('health_check')
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'ok',
            'cache': 'ok'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)
```

### 2. Monitoring with Prometheus

```python
# requirements.txt
django-prometheus==2.3.1

# settings.py
INSTALLED_APPS = [
    'django_prometheus',
    # ... other apps
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    # ... other middleware
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]
```

### 3. Backup Strategy

```bash
#!/bin/bash
# backup.sh - Database backup script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="life_organizer"

# Create backup
pg_dump $DATABASE_URL > $BACKUP_DIR/backup_$DATE.sql

# Upload to S3
aws s3 cp $BACKUP_DIR/backup_$DATE.sql s3://your-backup-bucket/

# Clean old backups (keep last 30 days)
find $BACKUP_DIR -name "backup_*.sql" -mtime +30 -delete
```

## 🔐 Security Checklist

- [ ] Use HTTPS everywhere
- [ ] Set up proper CORS origins
- [ ] Enable Django security middleware
- [ ] Use environment variables for secrets
- [ ] Set up database connection encryption
- [ ] Configure proper file upload limits
- [ ] Enable rate limiting
- [ ] Set up monitoring and alerting
- [ ] Regular security updates
- [ ] Database backups and recovery testing

## 📈 Performance Optimization

### 1. Database Optimization
- Use database indexes on frequently queried fields
- Implement database connection pooling
- Use read replicas for analytics queries
- Regular database maintenance and optimization

### 2. Caching Strategy
- Redis for session storage and caching
- CDN for static files
- Database query caching
- API response caching

### 3. Application Optimization
- Use Django's select_related and prefetch_related
- Implement pagination for large datasets
- Optimize serializers for performance
- Use background tasks for heavy operations

This deployment guide provides a comprehensive approach to deploying the Life Organizer application in production environments with proper security, monitoring, and scalability considerations.
