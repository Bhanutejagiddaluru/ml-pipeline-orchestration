from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import joblib, pandas as pd

app=FastAPI(title='Forecast API (RF demo)')
class PredictIn(BaseModel): history: list[float]

def load_model():
    p=Path('artifacts/registry/model.pkl')
    if not p.exists(): raise RuntimeError('No registered model found. Run pipeline first.')
    return joblib.load(p)

@app.get('/health')
def health(): return {'status':'ok'}

@app.post('/predict')
def predict(inp: PredictIn):
    s=pd.Series(inp.history); lag1=s.iloc[-1]; lag7=s.iloc[-7] if len(s)>=7 else lag1; roll7=s.tail(7).mean()
    X=[[lag1,lag7,roll7]]; m=load_model(); yhat=float(m.predict(X)[0]); return {'prediction': yhat}
