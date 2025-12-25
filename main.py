import pandas as pd
import argparse
from pathlib import Path

OUT_DIR = "results"

# 2 years of data = 24 months, skips partial datasets
MONTHS = 24


def monthly_ohlc(g):
    g = g.sort_values('date').set_index('date')
    m = g.resample('MS').agg({
        'open': 'first',
        'close': 'last', 
        'high': 'max',
        'low': 'min'
    }).reset_index()
    
    #  monthly close indicators
    c = m['close']
    m['SMA_10'] = c.rolling(10).mean()
    m['SMA_20'] = c.rolling(20).mean()
    m['EMA_10'] = c.ewm(span=10, adjust=False).mean()
    m['EMA_20'] = c.ewm(span=20, adjust=False).mean()
    return m


def run(path, out_dir=OUT_DIR):
    df = pd.read_csv(path, parse_dates=['date'])
    print(f"loaded {len(df)} rows")
    
    Path(out_dir).mkdir(exist_ok=True)
    
    for ticker, g in df.groupby('ticker'):
        m = monthly_ohlc(g)
        
        if m.shape[0] != MONTHS:
            print(f"skipping {ticker}, only {m.shape[0]} months")
            continue
        
        m['date'] = m['date'].dt.strftime('%Y-%m')
        out = f"{out_dir}/result_{ticker}.csv"
        m.to_csv(out, index=False)
        print(f"  {ticker}")
    
    print("done")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('input')
    p.add_argument('--out', default=OUT_DIR)
    args = p.parse_args()
    run(args.input, args.out)
