# 🚀 AI-Powered Infrastructure Monitoring Platform

An enterprise-grade Infrastructure Monitoring Platform inspired by Datadog and New Relic, built with Django, React, TypeScript, PostgreSQL, Redis, Celery, OpenAI, and Gemini.

The platform provides real-time infrastructure observability, agent-based telemetry collection, AI-powered Root Cause Analysis, risk prediction, intelligent recommendations, anomaly detection, incident management, and an AI Operations Assistant.

---

# 🎯 Highlights

✅ Agent-Based Monitoring Architecture

✅ Real-Time Telemetry Collection

✅ AI Root Cause Analysis (RCA)

✅ AI Recommendations Engine

✅ Infrastructure Risk Prediction

✅ Anomaly Detection

✅ Incident Management

✅ Alert Correlation

✅ AI Operations Assistant

✅ Cookie-Based Authentication

✅ Workspace Isolation

---

# 🏗 Architecture

```text
┌─────────────────────┐
│ Applications        │
│ APIs                │
│ Servers             │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Telemetry Agent     │
│ (agent.exe)         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Django Backend      │
│ Event Pipeline      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ AI Analytics Engine │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ React Dashboard     │
└─────────────────────┘
```

---

# ✨ Core Capabilities

## Infrastructure Monitoring

Real-time visibility into infrastructure health.

* CPU Monitoring
* Memory Monitoring
* Disk Monitoring
* Network Monitoring
* Process Monitoring
* Service Health Tracking

## Telemetry Collection

Secure agent-based telemetry ingestion.

* Log Monitoring
* API Monitoring
* Heartbeat Monitoring
* System Metrics
* Event Batching
* Secure Event Transmission

## Alerting & Incident Management

Automated incident lifecycle management.

* Rule-Based Alerts
* Alert Correlation
* Severity Classification
* Incident Creation
* Incident Resolution Workflow

## AI Operations

Built-in infrastructure intelligence layer.

* Root Cause Analysis
* AI Recommendations
* Risk Prediction
* AI Insights
* Trend Analysis
* Infrastructure Chat Assistant

---

# 🛠 Technology Stack

### Backend

* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* Simple JWT

### Frontend

* React
* TypeScript
* Vite
* Axios
* CSS

### AI

* OpenAI
* Google Gemini

### Monitoring Agent

* Python
* psutil
* watchdog
* requests

---

# ⚙ Backend Setup

## Clone Repository

```bash
git clone <repository-url>

cd project
```

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment

Create a `.env` file.

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

# 🎨 Frontend Setup

Install dependencies:

```bash
npm install
```

Start frontend:

```bash
npm run dev
```

---

# 🔴 Redis Setup

Start Redis server:

```bash
redis-server
```

---

# 📡 Telemetry Agent

The Telemetry Agent is responsible for collecting telemetry from monitored systems and securely transmitting it to the backend.

### Responsibilities

* Log Monitoring
* API Monitoring
* Process Monitoring
* System Metrics Collection
* Heartbeat Generation
* Event Batching
* Secure Communication

---

# 🚀 Agent Installation

Deploy monitoring in under 2 minutes.

### 1️⃣ Download Agent

Download the latest:

```text
monitoring-agent.zip
```

from the dashboard.

### 2️⃣ Extract Package

Extract the package on the target machine.

Example:

```text
C:\MonitoringAgent
```

or

```text
/opt/monitoring-agent
```

### 3️⃣ Configure Workspace API Key

Copy the generated Workspace API Key from the dashboard.

Add it to:

config.json file

```env
API_KEY=your_workspace_api_key
```

### 4️⃣ Launch Agent

Windows:

```bash
agent.exe
```

Linux:

```bash
./agent
```

The agent immediately begins:

* Collecting system metrics
* Monitoring APIs
* Monitoring logs
* Tracking processes
* Sending telemetry securely

---

# 📦 Building Agent Executable

Generate a standalone executable:

```bash
pyinstaller --onefile agent.py
```

Output:

```text
dist/
└── agent.exe
└── config.json
```

No Python installation is required on monitored machines.

---

# ▶ Running The Complete Platform

### Terminal 1

```bash
redis-server
```

### Terminal 2

```bash
python manage.py runserver
```

### Terminal 3

```bash
npm run dev
```

### Terminal 4

```bash
agent.exe
```

---

# 🤖 AI Capabilities

## Root Cause Analysis

Automatically identifies probable causes behind infrastructure incidents.

## AI Recommendations

Generates actionable remediation suggestions.

## Infrastructure Risk Prediction

Predicts future operational risks using telemetry patterns.

## AI Insights

Creates operational summaries and infrastructure intelligence reports.

## AI Operations Assistant

Ask questions about:

* Incidents
* Alerts
* RCA
* Risks
* Infrastructure Health
* Trends
* Recommendations

---

# 📈 Current Development Status

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
* AI Operations Assistant
* Cookie-Based Authentication
* API Documentation

### Upcoming

* Advanced Analytics Dashboard
* OpenTelemetry Integration
* Kubernetes Monitoring
* Production Deployment
* Multi-Tenant SaaS Support

---

# 📄 License

This project is built for educational, research, portfolio, and learning purposes.
