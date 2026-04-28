# %% [markdown]
# ## pre-test
# ####################################################################################################
# %%
import saspy

sas = saspy.SASsession()
# %%
for i in dir(sas.sasdata("cars", "sashelp")):
    if not i.startswith("_"):
        print(i)

# %% [markdown]
# ## snippets
# ####################################################################################################

# %%
# setup
import saspy

sas = saspy.SASsession()
sas


# %%
# setupcfg
import saspy  # isort: skip
from pathlib import Path  # isort: skip

print(Path(saspy.SAScfg).as_posix())

# %%
sas.submitLST(
    rf"""
%let myvar=myvalue;
libname mylib 'C:\temp';
""",
    method="listonly",
)

# %%
# head
df_h = sas.sasdata("cars", "sashelp").head()
df_h

# %%
sas.submitLST(f"proc print data=sashelp.cars (obs=5);run;", method="listonly")

# %%
# count
n_obs = sas.sasdata("cars", "sashelp").obs()
n_obs

# %%
# shape
sd = sas.sasdata("cars", "sashelp")
_shape = (sd.obs(), len(sd.columnInfo()))
print(_shape)


# %%
# top
df_h1 = sas.sasdata("cars", "sashelp").head(1)
print(df_h1.T.to_string())

# %%
# shapehead
sd = sas.sasdata("cars", "sashelp")
_shape, df_h = (sd.obs(), len(sd.columnInfo())), sd.head()
print(_shape)
df_h

# %%
# info
df_info = sas.sasdata("cars", "sashelp").columnInfo()
df_info

# %%
# col
df_info = sas.sasdata("cars", "sashelp").columnInfo()
cols = df_info["Variable"].tolist()
[c for c in cols if "cylin" in c.lower()]

# %%
# valc
sas.submitLST(
    f"""
proc freq data=sashelp.cars noprint;
    tables Origin / missing out=_tmp;
run;
""",
    method="listonly",
)
df = sas.sasdata("_tmp", "work").to_df()
df.columns = df.columns.str.lower()
df

# %%
sas.submitLST(
    f"""
proc sql;
create table _tmp as
    select
        origin,
        count(1) as n
    from sashelp.cars
    where msrp > 20000
    group by 1
    order by 1;
quit;
""",
    method="listonly",
)
df = sas.sasdata("_tmp", "work").to_df()
df


# %%
# run
sas.submitLST(f"""
proc print data=sashelp.cars (obs=5);
run;
""")

# %%
sas.submitLST(
    f"""
proc print data=sashelp.cars (obs=5);
run;
""",
    method="listandlog",
)

# %%
# grp

# %%
sas.submitLST(
    f"""
proc sort data=sashelp.cars out=_sorted;
    by Origin;

proc summary data=_sorted;
    by Origin;
    var MSRP;
    output out=_tmp
        mean(MSRP) = mean_MSRP
    ;
run;
""",
    method="listonly",
)
df = sas.sasdata("_tmp", "work").to_df()
df

# %%
# uni
sas.submitLST(
    f"""
title;
proc univariate data=sashelp.baseball;
    var salary;
    histogram salary / lognormal;
run;
""",
    method="listorlog",
)

# %%
# logi
sas.submitLST(
    """
proc logistic data=sashelp.heart plots(only)=roc;
    where status in ('Alive','Dead');
    model status(event='Dead') = height;
    output out=work._pred p=phat;
run;
""",
    method="listonly",
)

# %%
# sfa
sas.submitLST(
    f"""
proc rank
    data=sashelp.baseball(where=(division in ('East','West')))
    out=_tmp_h_dec
    groups=10;
    var salary;
    ranks decile0;
run;

proc sql;
create table _tmp_rates as
select
    case
        when missing(decile0) then 'NA'
        else strip(put(decile0 + 1, 2.))
    end as decile,
    count(*) as n,
    mean(division='East') as rate
from _tmp_h_dec
group by decile0
order by decile;
quit;

proc sgplot data=_tmp_rates;
    vbarparm category=decile response=n / datalabel transparency=0.15;
    series x=decile y=rate / y2axis markers lineattrs=(thickness=2);
    yaxis  label='Volume';
    y2axis label='Rate' values=(0 to 1 by 0.1);
    xaxis  label='Decile' integer;
run;
    """,
    method="listonly",
)

# %%
# qry
sas.submitLST(
    f"""
proc sql;
create table _tmp as
    select
        a.make,
        b.type,
        count(1) as n
    from sashelp.cars a
    left join sashelp.cars b
    on
        a.make = b.make and
        a.type = b.type
    where
        a.origin = 'USA'
    group by 1,2
    order by 1,2
    ;
quit;
""",
    method="listonly",
)

df = sas.sasdata("_tmp", "work").to_df()
df


# %%
# drop
sas.submitLST(f"proc sql;drop table work._tmp;quit;", method="listonly")

# %%
# write
sas.df2sd(df, "_tmp", "work")

# %%
# ctbl
sas.submitLST(f"proc sql;drop table work._tmp;quit;", method="listonly")

sas.submitLST(
    f"""
proc sql;
create table _tmp as
    select
        a.make,
        b.type,
        count(1) as n
    from sashelp.cars a
    left join sashelp.cars b
    on
        a.make = b.make and
        a.type = b.type
    where
        a.origin = 'USA'
    group by 1,2
    order by 1,2
    ;
quit;
""",
    method="listonly",
)

sas.sasdata("_tmp", "work").obs()


# %%
# join
sas.submitLST(
    f"""
proc sql;
create table _tmp as
    select
        a.make,
        b.model,
        b.make as make2
    from sashelp.cars a
    left join sashelp.cars b
    on
        a.make = b.make and
        a.model = b.model
    where
        a.make = 'Ford'
    ;
quit;
""",
    method="listonly",
)

sas.sasdata("_tmp", "work").obs()


# %%
# errors
print(f"{sas.saslog().count('ERROR') = }")

# %%
# log
print(sas.lastlog())
