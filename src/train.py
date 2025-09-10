import pandas as pd, joblib, json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from pathlib import Path

def train(features_csv, out_dir='artifacts/train'):
    df=pd.read_csv(features_csv, parse_dates=['timestamp'])
    X=df[['lag_1','lag_7','roll7']].values; y=df['value'].values
    Xtr,Xval,ytr,yval=train_test_split(X,y,test_size=0.2,shuffle=False)
    m=RandomForestRegressor(n_estimators=200,random_state=42).fit(Xtr,ytr)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    joblib.dump(m, Path(out_dir)/'model.pkl')
    yhat=m.predict(Xval); rmse=float(mean_squared_error(yval,yhat,squared=False))
    Path(out_dir).joinpath('metrics.json').write_text(json.dumps({'rmse':rmse}, indent=2))
    return str(Path(out_dir)/'model.pkl')
