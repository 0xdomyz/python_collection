# %%
import saspy

sas = saspy.SASsession()
# %%
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
print(f"{sas.saslog().count('ERROR') = }")
# %%
sas.submitLST(f"proc print data = sashelp.cars (obs=5);run;")
# %%
sas.sasdata("cars", "sashelp").head()
# %%
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
sas.submitLST(f"proc sql;drop table _tmp;run;", method="listonly")
# %%
sas.submitLST(
    rf"""
%let myvar=myvalue;
libname mylib 'C:\temp';
""",
    method="listonly",
)
# %%
print(sas.lastlog())
# %%
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
sas.submitLST(
    f"""
PROC CONTENTS DATA=sashelp.cars OUT=_tmp;
run;
"""
)
df = sas.sasdata("_tmp", "work").to_df()
df
# %%
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
sas.submitLST(
    f"proc sql (inobs=1); create table _tmp as select * from sashelp.cars; quit;"
)
print(sas.sasdata("_tmp", "work").to_df().T.to_string())
# %%
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
