import re
import unicodedata
from collections.abc import Mapping

import pandas as pd

DEFAULT_EXCLUDED_PREFIXES = ("cu ", "fara ", "sos ")


def clean_product_name(name: str) -> str:
    """Normalise harmless POS formatting without changing product meaning.

    This rule is intentionally restaurant-neutral: it handles case, accents,
    whitespace, and stray formatting characters, but never removes food words,
    sizes, promotions, or other business-specific terms.
    """
    name = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode("ascii")
    name = name.casefold()
    name = re.sub(r"[*_()\[\]{}\-]", " ", name)
    name = re.sub(r"\s+", " ", name).strip()

    return name

def load_product_aliases(path) -> dict[str, str]:
    """Load reviewed ``source_name,canonical_name`` mappings from a CSV file."""
    aliases = pd.read_csv(path)
    required_columns = {"source_name", "canonical_name"}
    missing_columns = required_columns - set(aliases.columns)
    if missing_columns:
        raise ValueError(f"Product aliases are missing columns: {missing_columns}")

    return {
        clean_product_name(source): canonical.strip()
        for source, canonical in aliases[["source_name", "canonical_name"]].dropna().itertuples(index=False)
    }


def load_product_exclusions(path) -> set[str]:
    """Load reviewed exact product names to omit from forecasting."""
    exclusions = pd.read_csv(path)
    if "product_name" not in exclusions.columns:
        raise ValueError("Product exclusions are missing the 'product_name' column")

    return {
        clean_product_name(name)
        for name in exclusions["product_name"].dropna()
    }


def filter_forecastable_products(
    df: pd.DataFrame,
    product_col: str = "menu_item_id",
    exclusions: set[str] | None = None,
) -> pd.DataFrame:
    """Remove modifiers and non-menu POS entries before forecasting.

    Prefix rules capture generic modifier/sauce rows. Restaurant-specific
    exclusions provide a safe escape hatch for any other POS-only product.
    """
    exclusions = {clean_product_name(name) for name in (exclusions or set())}
    normalized_names = df[product_col].map(clean_product_name)
    is_modifier_or_sauce = normalized_names.str.startswith(DEFAULT_EXCLUDED_PREFIXES)
    is_explicitly_excluded = normalized_names.isin(exclusions)

    return df.loc[~(is_modifier_or_sauce | is_explicitly_excluded)].copy()


def build_product_mapping(
    product_names,
    aliases: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Map POS names to a safe canonical name.

    Exact matches after formatting cleanup are grouped automatically. Different
    names with the same meaning must be listed in the reviewed alias table;
    this is intentionally safer than fuzzy matching sales items.
    """
    aliases = {clean_product_name(source): canonical for source, canonical in (aliases or {}).items()}
    grouped_names: dict[str, list[str]] = {}

    for raw_name in product_names:
        raw_name = str(raw_name)
        grouped_names.setdefault(clean_product_name(raw_name), []).append(raw_name)

    raw_to_canonical = {}
    for cleaned_name, raw_names in grouped_names.items():
        canonical = aliases.get(cleaned_name)
        if canonical is None:
            # Prefer the shortest original spelling, so ``Aripioare BBQ`` wins
            # over its ``*`` and ``_`` POS variants while retaining display case.
            canonical = min(raw_names, key=lambda name: (len(clean_product_name(name)), len(name), name))

        raw_to_canonical.update({raw_name: canonical for raw_name in raw_names})

    return raw_to_canonical


def normalize_products(
    df: pd.DataFrame,
    product_col: str = "menu_item_id",
    aliases: Mapping[str, str] | None = None,
) -> pd.DataFrame:
    df = df.copy()

    product_names = df[product_col].dropna().unique()

    mapping = build_product_mapping(product_names, aliases=aliases)

    df[product_col] = df[product_col].map(mapping).fillna(df[product_col])

    return df
