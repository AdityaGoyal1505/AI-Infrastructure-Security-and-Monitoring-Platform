# AI-Powered Infrastructure Monitoring Platform

## Overview

An enterprise-grade Infrastructure Monitoring Platform inspired by Datadog and New Relic, built using Django, React, TypeScript, PostgreSQL, Redis, Celery, and AI-powered analytics.

The platform provides real-time monitoring, incident detection, alerting, root cause analysis, risk prediction, anomaly detection, AI recommendations, and an intelligent operations assistant.

Unlike traditional academic monitoring projects, this platform includes a deployable Telemetry Agent, AI-driven analytics pipelines, automated incident management, and infrastructure intelligence capabilities.

---

# Key Features

## Infrastructure Monitoring

* Real-time system monitoring
* CPU monitoring
* Memory monitoring
* Disk monitoring
* Network monitoring
* Process monitoring
* Service monitoring

## Telemetry Agent

* Log monitoring
* API monitoring
* Heartbeat monitoring
* Process monitoring
* Metric collection
* Event batching
* Secure backend communication
* Standalone executable deployment

## Alerting Engine

* Rule-based alert generation
* Severity classification
* Alert lifecycle management
* Alert correlation

## Incident Management

* Automated incident creation
* Incident tracking
* Incident resolution workflow
* Incident timeline

## AI Engine

* Root Cause Analysis (RCA)
* Infrastructure Risk Prediction
* AI Recommendations
* AI Insights Generation
* Anomaly Detection
* Trend Analysis
* AI Operations Assistant

## Security

* JWT Authentication
* HttpOnly Cookie Authentication
* Refresh Token Rotation
* Workspace Isolation

---

# Technology Stack

## Backend

* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* Simple JWT

## Frontend

* React
* TypeScript
* Vite
* Axios
* CSS

## AI

* OpenAI (Analytics Engine)
* Gemini (Operations Assistant)

## Monitoring Agent

* Python
* psutil
* requests
* watchdog

---

# System Architecture

Applications / Servers

↓

Telemetry Agent

↓

Django API

↓

Monitoring Pipeline

↓

AI Analytics Engine

↓

React Dashboard

---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd project
```

---

# Backend Setup

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate Environment

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment

Create .env file

```env
SECRET_KEY=your_secret_key

DEBUG=True

DATABASE_URL=postgresql://user:password@localhost:5432/database

OPENAI_API_KEY=your_openai_key

GEMINI_API_KEY=your_gemini_key

ACCESS_TOKEN_LIFETIME_MINUTES=60

REFRESH_TOKEN_LIFETIME_DAYS=7
```

## Run Migrations

```bash
python manage.py migrate
```

## Start Backend

```bash
python manage.py runserver
```

---

# Frontend Setup

## Install Dependencies

```bash
npm install
```

## Start Frontend

```bash
npm run dev
```

---

# Redis Setup

Start Redis server

```bash
redis-server
```

---

# Telemetry Agent Setup

The platform includes a deployable Telemetry Agent responsible for collecting telemetry from monitored systems.

## Agent Responsibilities

* System metrics collection
* Process monitoring
* Log monitoring
* API monitoring
* Heartbeat generation
* Event batching
* Secure event transmission

---

# Agent Installation

## Step 1 — Download Agent

Download:

```text
monitoring-agent.zip
```

from the dashboard.

---

## Step 2 — Extract ZIP

Extract the package on the target server.

Example:

```text
C:\MonitoringAgent
```

or

```text
/opt/monitoring-agent
```

---

## Step 3 — Configure API Key

Copy the Workspace API Key from the platform dashboard.

Paste it into:

```env
config.json
```

```env
API_KEY=your_workspace_api_key
```

---

## Step 4 — Run Agent

Windows

```bash
agent.exe
```

Linux

```bash
./agent
```

The agent will automatically:

* Connect to backend
* Authenticate workspace
* Collect telemetry
* Send events
* Generate heartbeats

---

# Building Agent Executable

For production deployment:

```bash
pyinstaller --onefile agent.py
```

Generated executable:

```text
dist/
└── agent.exe
└── config.json
```

---

# Running Complete Platform

## Terminal 1

```bash
redis-server
```

## Terminal 2

```bash
python manage.py runserver
```

## Terminal 3

```bash
npm run dev
```

## Terminal 4

```bash
agent.exe
```

---

# AI Capabilities

## Root Cause Analysis

Identifies probable causes behind infrastructure incidents.

## AI Recommendations

Provides remediation suggestions based on detected issues.

## Risk Prediction

Predicts infrastructure risk using telemetry patterns.

## AI Insights

Generates operational summaries and infrastructure intelligence.

## AI Operations Assistant

Interactive assistant capable of answering questions regarding:

* Incidents
* Alerts
* RCA
* Infrastructure health
* Trends
* Risks

---

# Current Development Status

### Completed

* Authentication System
* Workspace Management
* Telemetry Agent
* Event Ingestion Pipeline
* Alert Engine
* Incident Management
* Root Cause Analysis
* Recommendations Engine
* Risk Prediction
* AI Insights
* AI Chat Assistant
* Cookie-Based Authentication
* API Documentation

### In Progress

* Advanced Analytics Dashboard
* Production Deployment
* OpenTelemetry Integration
* Multi-Agent Monitoring

---

# Future Enhancements

* Kubernetes Monitoring
* OpenTelemetry Support
* Distributed Tracing
* Multi-Tenant SaaS Deployment
* Slack Integration
* Microsoft Teams Integration
* Email Alerting
* Grafana Integration
* Predictive Capacity Planning

---

# License

This project is intended for educational, research, and portfolio purposes.
