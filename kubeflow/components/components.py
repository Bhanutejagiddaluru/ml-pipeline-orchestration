from kfp.dsl import component

@component(base_image='python:3.11-slim')
def ingest_op(csv_path: str) -> str:
    import pandas as pd; from pathlib import Path
    df=pd.read_csv(csv_path, parse_dates=['timestamp']); out=Path('/tmp/ingest'); out.mkdir(parents=True, exist_ok=True)
    p=out/'data.csv'; df.to_csv(p, index=False); return str(p)

@component(base_image='python:3.11-slim')
def featurize_op(in_csv: str) -> str:
    import pandas as pd; from pathlib import Path
    df=pd.read_csv(in_csv, parse_dates=['timestamp']).sort_values('timestamp')
    for l in [1,7]: df[f'lag_{l}']=df['value'].shift(l)
    df['roll7']=df['value'].rolling(7, min_periods=1).mean(); df=df.dropna().reset_index(drop=True)
    out=Path('/tmp/feats'); out.mkdir(parents=True, exist_ok=True); p=out/'features.csv'; df.to_csv(p, index=False); return str(p)

@component(base_image='python:3.11-slim')
def train_op(features_csv: str) -> str:
    import pandas as pd, joblib; from sklearn.ensemble import RandomForestRegressor; from sklearn.model_selection import train_test_split; from pathlib import Path
    df=pd.read_csv(features_csv); X=df[['lag_1','lag_7','roll7']].values; y=df['value'].values
    Xtr,Xval,ytr,yval=train_test_split(X,y,test_size=0.2,shuffle=False)
    m=RandomForestRegressor(n_estimators=200,random_state=42).fit(Xtr,ytr)
    out=Path('/tmp/model'); out.mkdir(parents=True, exist_ok=True); p=out/'model.pkl'; joblib.dump(m,p); return str(p)

@component(base_image='python:3.11-slim')
def evaluate_op(features_csv: str, model_path: str) -> str:
    import pandas as pd, joblib, json; from sklearn.metrics import mean_absolute_error, mean_squared_error; from pathlib import Path
    df=pd.read_csv(features_csv); X=df[['lag_1','lag_7','roll7']].values; y=df['value'].values
    m=joblib.load(model_path); yhat=m.predict(X); mae=float(mean_absolute_error(y,yhat)); import math; rmse=float(mean_squared_error(y,yhat,squared=False))
    out=Path('/tmp/eval'); out.mkdir(parents=True, exist_ok=True); j=out/'metrics.json'; j.write_text(json.dumps({'mae':mae,'rmse':rmse}, indent=2)); return str(j)

@component(base_image='python:3.11-slim')
def register_op(model_path: str) -> str:
    from pathlib import Path; import shutil
    reg=Path('/tmp/registry'); reg.mkdir(parents=True, exist_ok=True); dst=reg/'model.pkl'; shutil.copy(model_path, dst); return str(dst)
