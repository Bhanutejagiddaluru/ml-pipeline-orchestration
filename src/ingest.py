import pandas as pd, json
from pathlib import Path

def ingest(csv_path, out_dir='artifacts/ingest'):
    df = pd.read_csv(csv_path, parse_dates=['timestamp'])
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    out_csv = Path(out_dir)/'data.csv'
    df.to_csv(out_csv, index=False)
    Path(out_dir).joinpath('metadata.json').write_text(json.dumps({'rows':len(df),'path':str(out_csv)}))
    return str(out_csv)
