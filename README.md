# Stock Data Processor - Daily to Monthly Aggregation

A sturdy Python data engineering program that makes stock price daily data into monthly summaries with OHLC aggregation and technical indicators (SMA/EMA) in an efficient way.

## Problem Summary

This project utilizes a 2-year historical dataset of daily stock prices of 10 ticker symbols and does:
1. Resamples data from daily to monthly frequency
2. Calculates OHLC aggregates (Open, High, Low, Close)
3. Computes technical indicators (SMA-10, SMA-20, EMA-10, EMA-20)
4. Partitions results into individual files per stock symbol

## How to Run

### Prerequisites
- Python
- pandas library

### Installation
```bash
pip install pandas
```

### Execution
```bash
python main.py data/output_file.csv
```
### Output
The program produces 10 CSV files in the `results/` directory (for example `result_AAPL.csv`).
Each file is made up of exactly **24 rows** (each row for each month) with the columns:
`date, open, close, high, low, SMA_10, SMA_20, EMA_10, EMA_20`

## Assumptions & Constraint Handling
1.**Monthly Aggregation**:
- `Open` = Price on the first trading day
- `Close` = Price on the last trading day
- `High`/`Low` = Max/Min observed price in the month
- *Note: When determining OHLC, we give priority to actual traded values rather than averages.*

2.**Technical Indicators**:
- `SMA`: Standard simple moving average calculated on monthly close.
- `EMA`: Exponential moving average with `span=N` (is equivalent to `alpha=2/(N+1)`) and `adjust=False` (standard recursive calculation).

3.**Data Quality Enforcements**:
-**24-Month Requirement**: Only tickers with complete data for 24 months are used in the study and tickers with datasets that contain less than 24 months are automatically skipped in data uniformity.
- **Vectorized Operations**: All computations rely on the intrinsic Pandas functions to provide the best level of performance.
