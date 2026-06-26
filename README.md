Project ML

## Product-name normalisation

Sales exports can contain multiple POS names for one product. Before the daily
time series is built, the app removes harmless formatting differences such as
trailing `*` and `_`, then aggregates sales into one product.

For names that are genuinely different strings but mean the same product, add
one row to `data/product_aliases.csv`:

```csv
source_name,canonical_name
Aripioare pui BBQ Kg,Aripioare BBQ
```

Keep the canonical name exactly as it should appear in the forecast. Review
these mappings with the restaurant: automatic fuzzy matching is deliberately
not used because incorrectly combining two menu products would corrupt the
forecast and ingredient plan.
