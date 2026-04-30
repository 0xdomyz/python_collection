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
n_obs = sas.sasdata("baseball", "sashelp").obs()
n_obs
# %%
# shape
sd = sas.sasdata("heart", "sashelp")
_shape = (sd.obs(), len(sd.columnInfo()))
print(_shape)
# %%
# top
df_h1 = sas.sasdata("cars", "sashelp").head(1)
print(df_h1.T.to_string())
# %%
# shapehead
sd = sas.sasdata("heart", "sashelp")
_shape, df_h = (sd.obs(), len(sd.columnInfo())), sd.head()
print(_shape)
df_h
# %%
# info
df_info = sas.sasdata("baseball", "sashelp").columnInfo()
df_info
# %%
# col
df_info = sas.sasdata("baseball", "sashelp").columnInfo()
cols = df_info["Variable"].tolist()
[c for c in cols if "salary" in c.lower()]
# %%
# valc
sas.submitLST(
    f"""
proc sql;
create table _tmp as
    select
        division,
        count(1) as n
    from sashelp.baseball
    where salary > 200
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
proc print data=sashelp.baseball (obs=5);
run;
""",
    method="listonly",
)
# %%
sas.submitLST(
    f"""
proc sql;
create table tbl as
    select
        a.*,
        weight * 2 as weight2
    from sashelp.heart a
    where height > 5
    ;
quit;
""",
    method="listonly",
)
df_h1 = sas.sasdata(f"tbl", "work").head(1)
print(df_h1.T.to_string())
# %%
# runlog
sas.submitLST(
    f"""
proc print data=sashelp.heart (obs=5);
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
        deathcause,
        weight_status,
        count(1) as n
    from sashelp.heart
    where smoking > 0
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
# baseball salary
sas.submitLST(
    f"""
title;
proc univariate data=sashelp.heart;
    var smoking;
    histogram smoking / normal;
run;
""",
    method="listonly",
)
# %%
# freq
# cars origin
sas.submitLST(
    f"""
title;
proc freq data=sashelp.heart;
    tables weight_status * deathcause / chisq;
run;
""",
    method="listonly",
)

# %%
# logi
# heart height to predict status Alive or Dead
sas.submitLST(
    f"""
proc logistic data=sashelp.heart plots(only)=roc;
    where status in ('Alive','Dead');
    class weight_status (ref='Normal');
    model status(event='Dead') = smoking weight_status;
    output out=work._pred p=phat;
run;
""",
    method="listonly",
)
# %%
# sfa
# baseball salary to predict division East vs West
sas.submitLST(
    f"""
proc rank
    data=sashelp.heart(where=(status in ('Alive','Dead')))
    out=_tmp_h_dec
    groups=10;
    var smoking;
    ranks decile0;
run;

proc sql;
create table _tmp_rates as
select
    case
        when missing(decile0) then 'NA'
        else strip(put(decile0, 2.))
    end as decile,
    count(*) as n,
    mean(status='Dead') as rate
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
        a.smoking_status,
        b.weight_status,
        count(1) as n
    from sashelp.heart a
    left join sashelp.heart b
    on
        a.smoking_status = b.smoking_status and
        a.weight_status = b.weight_status
    where
        a.height > 1
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
sas.submitLST(f"proc sql;drop table _tmp;quit;", method="listonly")
# %%
# write
sas.df2sd(df, "_tmp", "work")
# %%
# ctbl
sas.submitLST(f"proc sql;drop table _tmp;quit;", method="listonly")

sas.submitLST(
    f"""
proc sql;
create table _tmp as
    select
        a.weight_status,
        b.smoking_status,
        count(1) as n
    from sashelp.heart a
    left join sashelp.heart b
    on
        a.weight_status = b.weight_status and
        a.smoking_status = b.smoking_status
    where
        a.weight > 1
    group by 1,2
    order by 1,2
    ;
quit;
""",
    method="listonly",
)

sas.sasdata(f"_tmp".split(".")[1], f"_tmp".split(".")[0]).obs()
# %%
# errors
print(f"{sas.saslog().count('ERROR') = }")
# %%
# log
print(sas.lastlog())
