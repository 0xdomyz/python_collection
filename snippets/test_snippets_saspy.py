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
shape = (sd.obs(), len(sd.columnInfo()))
print(shape)

# %%
# shapehead
sd = sas.sasdata("cars", "sashelp")
shape = (sd.obs(), len(sd.columnInfo()))
df_h = sd.head()
print(shape)
df_h

# %%
# top
df_h1 = sas.sasdata("cars", "sashelp").head(1)
print(df_h1.T.to_string())

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
# run
sas.submitLST(
    f"""
proc print data=sashelp.cars (obs=5);
run;
"""
)

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


# %%
# errors
print(f"{sas.saslog().count('ERROR') = }")

# %%
# log
print(sas.lastlog())
