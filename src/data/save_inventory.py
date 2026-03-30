from pathlib import Path
import pandas as pd

def save_inventory(df):
    
    base_dir = Path(__file__).resolve().parents[2]
    file_path = base_dir / "data" / "raw" / "inventory.csv"
    
    df.to_csv(file_path, index=False)

