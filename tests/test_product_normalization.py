"""Regression tests for restaurant-neutral menu-name normalisation."""

import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from preprocessing import build_product_mapping, clean_product_name, normalize_products


class ProductNormalizationTests(unittest.TestCase):
    def test_cleanup_groups_formatting_variants_without_an_alias(self):
        names = ["Spicy Wrap", "spicy wrap *", "Spicy_Wrap"]

        mapping = build_product_mapping(names)

        self.assertEqual({mapping[name] for name in names}, {"Spicy Wrap"})

    def test_cleanup_handles_accents_without_changing_the_display_name(self):
        names = ["Caf\u00e9 Cr\u00e8me", "cafe creme_"]

        mapping = build_product_mapping(names)

        self.assertEqual({mapping[name] for name in names}, {"Caf\u00e9 Cr\u00e8me"})
        self.assertEqual(clean_product_name("Caf\u00e9 Cr\u00e8me"), "cafe creme")

    def test_semantic_aliases_are_explicit_and_opt_in(self):
        names = ["Chicken Wings BBQ", "BBQ Wings Kg"]
        aliases = {"BBQ Wings Kg": "Chicken Wings BBQ"}

        mapping = build_product_mapping(names, aliases=aliases)

        self.assertEqual(mapping["Chicken Wings BBQ"], "Chicken Wings BBQ")
        self.assertEqual(mapping["BBQ Wings Kg"], "Chicken Wings BBQ")

    def test_normalization_preserves_total_sales(self):
        sales = pd.DataFrame(
            {
                "menu_item_id": ["Veggie Bowl", "Veggie Bowl *", "Plant Bowl Kg"],
                "quantity_sold": [2, 3, 4],
            }
        )

        normalized = normalize_products(
            sales,
            aliases={"Plant Bowl Kg": "Veggie Bowl"},
        )

        self.assertEqual(normalized["menu_item_id"].tolist(), ["Veggie Bowl"] * 3)
        self.assertEqual(normalized["quantity_sold"].sum(), 9)


if __name__ == "__main__":
    unittest.main()
