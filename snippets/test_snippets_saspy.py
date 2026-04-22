# %% [markdown]
# ## test
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
# head
df_h = sas.sasdata("cars", "sashelp").head()
df_h

# %%
# count
n_obs = sas.sasdata("cars", "sashelp").obs()
n_obs

# %% [markdown]
# ## unprocessed
# ####################################################################################################

# %%
# run
sas.submitLST(
    f"""
proc print data=sashelp.cars (obs=5);
run;
"""
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
# errorcount
print(f"{sas.saslog().count('ERROR') = }")
# %%
# print
sas.submitLST(f"proc print data = sashelp.cars (obs=5);run;")
# %%
# ctbl
sas.submitLST(
    f"""
proc sql;
create table _tmp as
    select
        *
    from sashelp.cars
    where Length > 220
    ;
quit;
""",
    method="listonly",
)
df = sas.sasdata("_tmp", "work").to_df()
df
# %%
# drop
sas.submitLST(f"proc sql;drop table _tmp;run;", method="listonly")
# %%
# let
sas.submitLST(
    rf"""
%let myvar=myvalue;
libname mylib 'C:\temp';
""",
    method="listonly",
)
# %%
# log
print(sas.lastlog())
# %%
# freq
sas.submitLST(
    f"""
proc freq data=sashelp.cars noprint;
    tables Origin / missing out=_tmp;
run;
"""
)
df = sas.sasdata("_tmp", "work").to_df()
df.columns = df.columns.str.lower()
df
# %%
# stat
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
"""
)
df = sas.sasdata("_tmp", "work").to_df()
df
# %%
# info
sas.submitLST(
    f"""
PROC CONTENTS DATA=sashelp.cars OUT=_tmp;
run;
"""
)
df = sas.sasdata("_tmp", "work").to_df()
df
# %%
# qry
sas.submitLST(
    f"""
proc sql;
create table _tmp as
    select
        Origin,
        Type,
        count(1) as n
    from sashelp.cars
    where Origin = 'USA'
    group by 1,2
    order by 1,2
    ;
quit;
"""
)
df = sas.sasdata("_tmp", "work").to_df()
df
# %%
# top
sas.submitLST(
    f"proc sql inobs=1; create table _tmp as select * from sashelp.cars; quit;",
    method="listonly",
)
print(sas.sasdata("_tmp", "work").to_df().T.to_string())

# %%
# join
sas.submitLST(
    f"""
proc sql;
create table _tmp as
    select
        a.*,
        b.*
    from sashelp.cars a
    left join sashelp.cars b
    on
        a.Make = b.Make and
        a.Type = b.Type
    where
        a.Origin = 'USA'
    group by 1,2
    order by 1,2
    ;
quit;
"""
)
df = sas.sasdata("_tmp", "work").to_df()
df
df
