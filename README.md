Project ML

## Product-name normalisation

Sales exports can contain multiple POS names for one product. Before the daily
time series is built, the app removes harmless formatting differences such as
trailing `*` and `_`, then aggregates sales into one product.

For names that are genuinely different strings but mean the same product, add
one row to an alias file named after the sales export. For example, the
`starkebab_portmall_2025-2026.csv` export uses
`data/aliases/starkebab_portmall_2025-2026.csv`:

```csv
source_name,canonical_name
Aripioare pui BBQ Kg,Aripioare BBQ
```

Keep the canonical name exactly as it should appear in the forecast. Review
these mappings with the restaurant: automatic fuzzy matching is deliberately
not used because incorrectly combining two menu products would corrupt the
forecast. Alias files are client-specific; the cleanup code itself only makes
safe, reusable formatting changes.

## Forecast exclusions

Modifier rows (`cu ...`, `fără ...`) and standalone sauces (`Sos ...`) are
removed from every forecast automatically. To omit other POS-only rows for one
restaurant, create `data/exclusions/<sales-export-name>.csv` with a
`product_name` column. These exclusions are client-specific, just like aliases.
