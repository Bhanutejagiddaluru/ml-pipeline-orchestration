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
```
## Extra (Airflow local quickstart)
```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow db init
airflow users create --username admin --firstname a --lastname a --role Admin --email a@a.com --password admin
airflow webserver -p 8080  &
airflow scheduler &
# DAG: forecasting_dag
```
## ▶️ Run the API locally
```bash
uvicorn api.main:app --reload
```
## ☸️ Build & Push Containers
```bash
docker build -t yourrepo/kfp-component -f docker/component.Dockerfile .
docker build -t yourrepo/forecasting-api -f docker/api.Dockerfile .
```
## ☸️Deploy API to K8s
```bash
kubectl apply -f manifests/api-deployment.yaml
kubectl apply -f manifests/api-service.yaml

```


### Includes:

- README.md (how to install & run Kubeflow and Airflow versions)
- requirements.txt (kfp, apache-airflow, sklearn, fastapi, etc.)
- data/retail_sales_small.csv (toy time-series)

#### src/
   - ingest.py, featurize.py, train.py, evaluate.py, register.py (reusable pipeline steps)

- airflow/dags/forecasting_dag.py (end-to-end DAG)
- kubeflow/components/components.py (lightweight components)
- kubeflow/pipelines/kfp_forecasting_pipeline.py (compile with kfp Compiler)
- api/main.py (FastAPI to serve predictions from the registered model)
- docker/component.Dockerfile, docker/api.Dockerfile
- manifests/api-deployment.yaml, manifests/api-service.yaml (K8s deploy service)

### Quick start:
## ☸️Deploy API to K8s
```bash
python -m venv .venv && source .venv/bin/activate

pip install -r requirements.txt

Airflow: init DB, start webserver & scheduler → run forecasting_dag

Kubeflow: compile kfp_forecasting_pipeline.py → upload json in KFP UI/run

After register step creates artifacts/registry/model.pkl:
uvicorn api.main:app --reload → POST to /predict with last 7 values.
```


## Thank You

