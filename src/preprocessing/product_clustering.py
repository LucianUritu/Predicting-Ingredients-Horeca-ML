import re
from difflib import SequenceMatcher

import pandas as pd


def token_sort_ratio(left: str, right: str) -> float:
    """Return a 0-100 similarity score after sorting each name's words.

    This mirrors the comparison style formerly supplied by ``rapidfuzz`` while
    keeping product normalization runnable on a plain Streamlit deployment.
    """
    sorted_left = " ".join(sorted(left.split()))
    sorted_right = " ".join(sorted(right.split()))
    return SequenceMatcher(None, sorted_left, sorted_right).ratio() * 100

def clean_product_name(name: str) -> str:
    name = str(name).lower()
    name = re.sub(r"[*_()\[\]{}\-]", " ", name)
    name = re.sub(r"\s+", " ", name).strip()

    return name

def choose_canonical_name(cluster: list[str]) -> str:
    """
    Choose the shortest name as canonical.
    Usually removes noisy variants like '*', '_personal', etc.
    """

    return min(cluster, key=len)

def cluster_product_names(product_names, threshold: int = 85):
    clusters = []

    for raw_name in product_names:
        cleaned_name = clean_product_name(raw_name)
        matched = False

        for cluster in clusters:
            representative = cluster[0]

            score = token_sort_ratio(cleaned_name, representative)

            if score >= threshold:
                cluster.append(cleaned_name)
                matched = True
                break

        if not matched:
            clusters.append([cleaned_name])

    return clusters


def build_product_mapping(product_names, threshold: int = 85) -> dict:
    """
    Returns:
    {
        raw_name: canonical_name
    }
    """

    clusters = cluster_product_names(product_names, threshold)

    cleaned_to_canonical = {}

    for cluster in clusters:
        canonical = choose_canonical_name(cluster)

        for name in cluster:
            cleaned_to_canonical[name] = canonical

    raw_to_canonical = {}

    for raw_name in product_names:
        cleaned = clean_product_name(raw_name)
        raw_to_canonical[raw_name] = cleaned_to_canonical.get(cleaned, cleaned)

    return raw_to_canonical


def normalize_products(
    df: pd.DataFrame,
    product_col: str = "menu_item_id",
    threshold: int = 85
) -> pd.DataFrame:
    df = df.copy()

    product_names = df[product_col].dropna().unique()

    mapping = build_product_mapping(product_names, threshold)

    df["canonical_product_name"] = df[product_col].map(mapping)

    return df
