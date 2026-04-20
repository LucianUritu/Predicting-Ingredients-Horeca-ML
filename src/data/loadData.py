from pathlib import Path
import pandas as pd

def load_data():
    base_dir = Path(__file__).resolve().parents[2]
    file_path = base_dir / "data" / "raw" / "starkebab_portmall_2025-2026.csv"
    
    df = pd.read_csv(file_path, parse_dates=["sales_date"])

    return df