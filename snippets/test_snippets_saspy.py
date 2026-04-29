# %%
# sassetup
import saspy

sas = saspy.SASsession()
sas

# %%
# setupcfg
import saspy  # isort: skip
from pathlib import Path  # isort: skip

print(Path(saspy.SAScfg).as_posix())
# %%
# setuplib
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
sas.submitLST(
    f"""
proc print data=sashelp.cars (obs=5);
run;
""",
    method="listonly",
)
# %%
# runlog
sas.submitLST(
    f"""
proc print data=sashelp.cars (obs=5);
run;
""",
    method="listandlog",
)
# %%
# grp
sas.submitLST(
    f"""
proc sql;
create table _tmp as
    select
        origin,
        type,
        count(1) as n
    from sashelp.cars
    where msrp > 20000
    group by 1,2
    order by 1,2;
quit;
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
    method="listonly",
)
# %%
# freq
sas.submitLST(
    f"""
title;
proc freq data=sashelp.cars;
    tables origin type / chisq;
run;
""",
    method="listonly",
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
