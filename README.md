# URL Metrics Service

This Python service periodically checks two external URLs for availability and response time, exposing these metrics in Prometheus format via a simple HTTP server.

---

## Features

- Checks URLs `https://httpstat.us/503` and `https://httpstat.us/200`
- Reports:
  - URL up status (`1` for up, `0` for down)
  - Response time in milliseconds
- Exposes metrics at `/metrics` endpoint in Prometheus format
- Dockerized for easy deployment
- Helm chart included for Kubernetes deployment

---

## Prerequisites

- Docker
- Kubernetes cluster (Docker Desktop with Kubernetes enabled works)
- Helm 3
- Python 3.13 (for local runs)

---

## Install dependencies

  - pip install -r requirements.txt in vscode terminal or similar IDE

## Clone the repo

  ```
   cd "folder path where you want the repo to be downloaded"
   git clone https://github.com/GeorgiGabrilov/InfraTaskProject.git
  ```
 
## Deploy to Kubernetes with Helm 

  ``` 
   navigate to the folder where zip file was extracted and open a terminal and paste the helm install command
   "helm install url-metrics-app ./url-metrics-app -f ./url-metrics-app/values.yaml"
 

  Open http://localhost:30080/metrics in your browser to check the metrics
 
  Remove helm with this command in vscode terminal
  "helm uninstall url-metrics-app" 
