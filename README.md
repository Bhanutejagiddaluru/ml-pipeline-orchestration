# ML Pipeline Orchestration — Kubeflow & Airflow (End-to-End)

This repo demonstrates an **end-to-end ML pipeline** implemented in **two orchestration styles**:

1) **Kubeflow Pipelines** — portable, Kubernetes-native, with componentized steps  
2) **Apache Airflow** — DAG-based orchestration for batch pipelines

> Reference: Kubeflow Pipelines: https://github.com/kubeflow/pipelines

## 📦 What’s Included
- **Data**: `data/retail_sales_small.csv` (toy time series)
- **Reusable components**: `src/` (ingest, featurize, train, evaluate, register)
- **Kubeflow**: components + `pipelines/kfp_forecasting_pipeline.py` (builds a pipeline with caching & artifacts)
- **Airflow**: `airflow/dags/forecasting_dag.py` DAG with task dependencies
- **API**: `api/main.py` FastAPI endpoint for model inference (simple pickle model demo)
- **Docker**: `docker/component.Dockerfile` & `docker/api.Dockerfile`
- **K8s Manifests**: `manifests/api-deployment.yaml` & `manifests/api-service.yaml`

## 🧱 Pipeline Steps
1. Ingest → Featurize → Train → Evaluate → Register → Serve

## 🛠 Tech
Kubeflow Pipelines (kfp) • Apache Airflow • Python • scikit-learn • Pandas/Numpy • FastAPI • Docker • Kubernetes

## 🔧 Install
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
