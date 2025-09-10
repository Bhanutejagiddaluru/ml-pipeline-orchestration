import pandas as pd, joblib, json
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pathlib import Path

def evaluate(features_csv, model_path, out_dir='artifacts/evaluate'):
    df=pd.read_csv(features_csv, parse_dates=['timestamp'])
    X=df[['lag_1','lag_7','roll7']].values; y=df['value'].values
    m=joblib.load(model_path); yhat=m.predict(X)
    mae=float(mean_absolute_error(y,yhat)); rmse=float(mean_squared_error(y,yhat,squared=False))
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    Path(out_dir).joinpath('metrics.json').write_text(json.dumps({'mae':mae,'rmse':rmse}, indent=2))
    return str(Path(out_dir)/'metrics.json')
