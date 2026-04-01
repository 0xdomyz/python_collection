# %%
def make_bin_expression(
    col: str,
    bins: list[float],
    n_indent_tabs: int = 0,
    labels: list[str] = None,
    right: bool = False,
) -> str:
    """Build a SQL CASE WHEN binning expression."""
    if not bins:
        return ""

    if labels is not None and len(labels) != len(bins) + 1:
        raise ValueError("labels must have len(bins) + 1 elements")

    indent = "    " * n_indent_tabs
    bounds = [None, *bins, None]
    lines: list[str] = []

    for i, (lower, upper) in enumerate(zip(bounds, bounds[1:])):
        if lower is None:
            if right:
                condition = f"{col} <= {upper}"
                default_label = f"(-Inf, {upper}]"
            else:
                condition = f"{col} < {upper}"
                default_label = f"[-Inf, {upper})"
        elif upper is None:
            if right:
                condition = f"{col} > {lower}"
                default_label = f"({lower}, Inf]"
            else:
                condition = f"{col} >= {lower}"
                default_label = f"[{lower}, Inf)"
        else:
            if right:
                condition = f"{col} > {lower} and {col} <= {upper}"
                default_label = f"({lower}, {upper}]"
            else:
                condition = f"{col} >= {lower} and {col} < {upper}"
                default_label = f"[{lower}, {upper})"

        label = labels[i] if labels is not None else default_label

        if i == 0:
            lines.append(f"when {condition} then '{label}'")
        else:
            lines.append(f"{indent}when {condition} then '{label}'")

    return "\n".join(lines)


# %%
qry = f"""
    case
        {make_bin_expression(
            'expo',
            bins = ['-100e6', ], 
            n_indent_tabs=2, 
            right=True
        )}
    end as col_bin
"""
print(qry)
# %%
qry = f"""
    case
        {make_bin_expression(
            'expo',
            bins = ['-100e6', '-10e6', '-1e6', '0'], 
            labels=['01 100m+', '02 10m-100m', '03 1m-10m', '04 0-1m', '05 0+'],
            n_indent_tabs=2, 
            right=True
        )}
    end as col_bin
"""
print(qry)

# %%
qry = f"""
    case
        {make_bin_expression(
            'expo',
            bins = [], 
            labels=['01 100m+',],
            n_indent_tabs=2, 
            right=True
        )}
    end as col_bin
"""
print(qry)
# %%
try:
    qry = f"""
        case
            {make_bin_expression(
                'expo',
                bins = [1], 
                labels=['01 100m+', '02 10m-100m', '03 1m-10m', '04 0-1m', '05 0+'],
                n_indent_tabs=2, 
                right=True
            )}
        end as col_bin
    """
    print(qry)
except ValueError as e:
    print(f"Error: {e}")
