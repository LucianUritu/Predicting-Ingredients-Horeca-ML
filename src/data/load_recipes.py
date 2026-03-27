import pandas as pd
from pathlib import Path

def load_recipes():
    base_dir = Path(__file__).resolve().parents[2]
    file_path = base_dir / "data" / "raw" / "recipes.csv"
    
    df = pd.read_csv(file_path)

    return df