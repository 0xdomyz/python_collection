# Snippets Organization Plan

## Current State

**`snippets_stats.json`** — pandas + plot snippets (~25 snippets, prefixes like `pstr`, `grp*`, `valc`, `info`, `loc`, `readcsv`, etc.)

**`snippets_db.json`** — three flavors mixed together:
- Generic SQLAlchemy (`db*` prefix)
- Teradata-specific (`tdsetup` only, then reuses `db*`)
- DuckDB (`ddb*` prefix)

**`snippets_saspy.json`** — SAS via saspy (`sas*` prefix, ~20 snippets, most complete and consistent)

**`test_snippets_saspy.py`** — materialized examples, one `# %%` cell per snippet

---

## The ~10 Canonical Operations

Across all three there's a clear shared vocabulary:

| Operation | Pandas | Teradata | SAS |
|---|---|---|---|
| **setup** | `iana` / `istats` | `tdsetup` | `sassetup` |
| **head** | `phstr` / `shapephstr` | `dbhead` | `sasdatahead` |
| **top1 (transposed)** | `df.head(1).T` | `dbtop` | `sastop1` |
| **schema / info** | `info` | `dbcol` | `saspcontent` |
| **filter / query** | `loc` / `qry` | `dbqry` | `sasqry` |
| **value counts / freq** | `valc` | *(missing)* | `saspfreqdf` |
| **group + agg** | `grpargs` / `grpdict` | `dbgrp` | `sasgrp` / `saspsumdf` |
| **join** | `pd.merge` *(missing snippet)* | `dbouter` | `sasjoin` |
| **create temp** | *(df is the temp)* | `dbctbl` | `sasqry` (create table _tmp) |
| **drop temp** | *(not applicable)* | `dbdrop` | `sasdrop` |
| **count** | `len(df)` | `dbcount1` | *(missing)* |
| **error / log check** | *(not applicable)* | *(not applicable)* | `saserrorcount` / `saslastlog` |

---

## Proposed Organization

### 1. Consistent prefix scheme per library

Right now `snippets_db.json` mixes generic `db*` and teradata `td*`. Suggest splitting into dedicated files and aligning prefixes:

```
snippets_pd.json     → pd_head, pd_top1, pd_info, pd_valc, pd_grp, pd_join ...
snippets_td.json     → td_setup, td_head, td_top1, td_schema, td_qry, td_grp, td_join ...
snippets_sas.json    → sas* (already consistent)
snippets_ddb.json    → ddb* (already has its own prefix)
```

### 2. One `test_snippets_<lib>.py` per library, same structure

Each file covers all ~10 ops in the same order using a standard dataset:
- `titanic` for pandas / duckdb
- `sashelp.cars` for SAS
- `dbc.columns` or a known table for Teradata

```
test_snippets_pd.py    ← needs to be created
test_snippets_td.py    ← needs to be created
test_snippets_sas.py   ← already exists (test_snippets_saspy.py)
```

### 3. Workflow

```
real usage code
    → strip to minimal example
    → add as # %% cell in test_snippets_<lib>.py   (materialized proof it works)
    → parameterize → add to snippets_<lib>.json     (the snippet)
```

---

## Gaps to Fill

| Library | Missing |
|---|---|
| **Pandas** | `pd_join` snippet, `pd_top1` (transposed head), standard dataset setup for titanic |
| **Teradata** | `td_freq` (value counts equivalent), schema dump equivalent to `saspcontent` |
| **SAS** | `sascount` (row count without creating temp table) |
| **`snippets_db.json`** | Teradata snippets buried alongside SQLAlchemy and DuckDB — split into separate files |

---

## Next Steps

1. Create `test_snippets_pd.py` covering all 10 ops with `titanic` dataset
2. Split `snippets_db.json` into `snippets_td.json` and `snippets_ddb.json` with aligned prefixes
3. Fill the identified gaps in each snippet file
