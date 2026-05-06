import pandas as pd

GEE_COLOR = "#4C72B0"
GEL_COLOR = "#9467bd"
GROUP_COLORS = {"GEE": GEE_COLOR, "GEL": GEL_COLOR}


def fmt_money(v) -> str:
    """Format triệu VNĐ values: ≥1,000,000 → T, ≥1,000 → B, else raw."""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "—"
    v = float(v)
    sign = "-" if v < 0 else ""
    av = abs(v)
    if av >= 1_000_000:
        return f"{sign}{av / 1_000_000:.1f}T"
    if av >= 1_000:
        return f"{sign}{av / 1_000:.1f}B"
    return f"{sign}{av:,.0f}"
