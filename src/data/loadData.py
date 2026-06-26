from pathlib import Path
import pandas as pd

from .clean_sales_data import clean_sales_data
from .build_daily_sales_grid import build_daily_sales_grid
from .filter_items import filter_items_by_min_history
from preprocessing import load_product_aliases, normalize_products

DEFAULT_MIN_DAYS_PER_ITEM = 30
DEFAULT_FILENAME = "starkebab_portmall_2025-2026.csv"
ALIASES_DIRECTORY = "aliases"


def load_data(
    filename: str = DEFAULT_FILENAME,
    min_days_per_item: int = DEFAULT_MIN_DAYS_PER_ITEM,
    aliases_filename: str | None = None,
) -> pd.DataFrame:
    """
    Load raw client sales data and return a cleaned daily time series.
    """
    base_dir = Path(__file__).resolve().parents[2]
    file_path = base_dir / "data" / "raw" /filename

    df = pd.read_csv(file_path)

    df = clean_sales_data(df)
    # Each sales export gets its own reviewed alias file. The normalisation
    # code remains reusable and no restaurant's menu rules affect another's.
    aliases_filename = aliases_filename or f"{file_path.stem}.csv"
    aliases_path = base_dir / "data" / ALIASES_DIRECTORY / aliases_filename
    aliases = load_product_aliases(aliases_path) if aliases_path.exists() else {}
    df = normalize_products(df, aliases=aliases)
    # Alias replacement can make formerly separate rows share one day/item.
    # Aggregate them before creating the continuous daily sales grid.
    df = clean_sales_data(df)
    df = build_daily_sales_grid(df)
    df = filter_items_by_min_history(df, min_days_per_item=min_days_per_item)

    return df
