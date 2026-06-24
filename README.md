# 🚀 AI-Powered Infrastructure Monitoring Platform

Enterprise-grade infrastructure observability platform inspired by Datadog and New Relic.

Monitor servers, APIs, logs, and system health in real-time while leveraging AI-powered Root Cause Analysis, Risk Prediction, Recommendations, and Infrastructure Intelligence.

Built with Django, React, TypeScript, PostgreSQL, Redis, Celery, OpenAI, and Gemini.

---

## 🎯 Highlights

* Agent-Based Monitoring Architecture
* Real-Time Telemetry Collection
* AI Root Cause Analysis
* AI Recommendations Engine
* Infrastructure Risk Prediction
* Incident Management
* Alert Correlation
* AI Operations Assistant
* Cookie-Based Authentication
* Workspace Isolation

---

## 🏗 Architecture

```text
Applications / Servers
          │
          ▼
   Telemetry Agent
      (agent.exe)
          │
          ▼
      Django API
          │
          ▼
   AI Analytics Engine
          │
          ▼
    React Dashboard
```

---

## ✨ Features

### Infrastructure Monitoring

* CPU Monitoring
* Memory Monitoring
* Disk Monitoring
* Network Monitoring
* Process Monitoring
* Service Health Tracking

### Telemetry Agent

* Log Monitoring
* API Monitoring
* Heartbeat Generation
* Event Batching
* Secure Transmission

### Alerting & Incidents

* Rule-Based Alerts
* Alert Correlation
* Severity Classification
* Incident Lifecycle Management

### AI Operations

* Root Cause Analysis
* Recommendations Engine
* Risk Prediction
* Infrastructure Insights
* Trend Analysis
* AI Chat Assistant

---

## 🛠 Tech Stack

### Backend

* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery

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

## 🚀 Available Scripts

- **dev** — `npm run dev`
- **build** — `npm run build`
- **lint** — `npm run lint`
- **preview** — `npm run preview`

---

## 📁 Project Structure

```
.
├── Backend
│   ├── Infra
│   │   ├── Dockerfile
│   │   ├── Infra
│   │   ├── manage.py
│   │   ├── monitoring   
│   │   └── requirements.txt
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── telemetry-agent
│       └── monitoring-agent.zip
├── Frontend
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── public
│   ├── src
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
└── requirements.txt
```

---

## ⚡ Quick Start

### Backend

```bash
pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

### Frontend

```bash
npm install

npm run dev
```

### Redis

```bash
redis-server
```

---

## 📡 Agent Installation

Deploy monitoring in under two minutes.

### 1. Download Agent

Download:

```text
monitoring-agent.zip
```

from the dashboard.

### 2. Extract Package

Extract on the target machine.

### 3. Configure API Key into JSON file

```env
API_KEY=your_workspace_api_key
```

### 4. Launch Agent

```bash
agent.exe
```

The agent immediately begins collecting telemetry and transmitting monitoring events to the platform.

---

## 📦 Build Agent Executable

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

## 🤖 AI Capabilities

### Root Cause Analysis

Identifies probable causes behind infrastructure incidents.

### Recommendations Engine

Generates remediation suggestions based on detected issues.

### Risk Prediction

Predicts infrastructure risks using telemetry patterns.

### Infrastructure Insights

Creates operational summaries and intelligence reports.

### AI Operations Assistant

Interactive assistant capable of answering questions regarding:

* Incidents
* Alerts
* RCA
* Risks
* Infrastructure Health
* Trends
* Recommendations

---

## 📈 Project Status

### Completed

* Authentication System
* Workspace Management
* Telemetry Agent
* Event Ingestion Pipeline
* Alert Engine
* Incident Management
* AI Root Cause Analysis
* AI Recommendations
* AI Risk Prediction
* AI Insights
* AI Operations Assistant
* Cookie-Based Authentication
* API Documentation

### Planned

* Advanced Analytics Dashboard
* OpenTelemetry Integration
* Kubernetes Monitoring
* Production Deployment
* Multi-Tenant SaaS Support

---

## 📄 License

Built for educational, research, portfolio, and learning purposes.
