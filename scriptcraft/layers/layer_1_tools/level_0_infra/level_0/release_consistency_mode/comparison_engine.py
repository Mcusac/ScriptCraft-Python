"""
Core comparison engine.
"""

import pandas as pd


def build_pivot(df_old, df_new, label_old, label_new, drop_release=False):
    if drop_release:
        df_old = df_old.drop(columns=["Release"], errors="ignore")
        df_new = df_new.drop(columns=["Release"], errors="ignore")

    df_old = df_old.copy().assign(Release=label_old)
    df_new = df_new.copy().assign(Release=label_new)

    combined = pd.concat([df_old, df_new], ignore_index=True)

    return combined.pivot_table(
        index=["Med_ID", "Visit_ID"],
        columns="Release",
        aggfunc="first",
    )


def diff_block(pivot, old, new):
    a = pivot.xs(old, axis=1, level="Release")
    b = pivot.xs(new, axis=1, level="Release")

    mask = a.ne(b) & ~(a.isna() & b.isna())
    return pivot[mask.any(axis=1)]


def diff_filtered(pivot, old, new):
    pivot = pivot.copy()
    pivot.columns = [f"{c}_{r}" for c, r in pivot.columns]

    masks = []

    for col in pivot.columns:
        if not col.endswith(f"_{old}"):
            continue

        base = col.replace(f"_{old}", "")
        c_old = f"{base}_{old}"
        c_new = f"{base}_{new}"

        if c_old in pivot.columns and c_new in pivot.columns:
            masks.append((pivot[c_old] != pivot[c_new]) &
                         ~(pivot[c_old].isna() & pivot[c_new].isna()))

    if not masks:
        return pivot.iloc[[]]

    final = masks[0]
    for m in masks[1:]:
        final |= m

    return pivot[final]