from pathlib import Path
import pandas as pd

from .clean_sales_data import clean_sales_data
from .build_daily_sales_grid import build_daily_sales_grid
from .filter_items import filter_items_by_min_history

DEFAULT_MIN_DAYS_PER_ITEM = 30
DEFAULT_FILENAME = "starkebab_portmall_2025-2026.csv"


def load_data(filename: str = DEFAULT_FILENAME, 
              min_days_per_item: int = DEFAULT_MIN_DAYS_PER_ITEM,) -> pd.DataFrame:
    """
    Load raw client sales data and return a cleaned daily time series.
    """
    base_dir = Path(__file__).resolve().parents[2]
    file_path = base_dir / "data" / "raw" /filename

    df = pd.read_csv(file_path)

    df = clean_sales_data(df)
    df = build_daily_sales_grid(df)
    df = filter_items_by_min_history(df, min_days_per_item=min_days_per_item)

    return df