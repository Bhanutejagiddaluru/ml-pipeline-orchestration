import pandas as pd
from pathlib import Path

def featurize(in_csv, out_dir='artifacts/featurize'):
    df = pd.read_csv(in_csv, parse_dates=['timestamp']).sort_values('timestamp')
    for lag in [1,7]:
        df[f'lag_{lag}']=df['value'].shift(lag)
    df['roll7']=df['value'].rolling(7, min_periods=1).mean()
    df=df.dropna().reset_index(drop=True)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    out_csv=Path(out_dir)/'features.csv'; df.to_csv(out_csv, index=False)
    return str(out_csv)
