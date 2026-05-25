/* Step 1: Simulate data */
data df;
    call streaminit(42);
    do i = 1 to 1000;
        x = rand("Normal", 50, 10);
        target = rand("Bernoulli", 0.4);
        output;
    end;
    drop i;
run;

/* Step 2: Manual binning */
data df;
    set df;
    if 0 <= x < 40 then x_bin = 1;
    else if 40 <= x < 50 then x_bin = 2;
    else if 50 <= x < 60 then x_bin = 3;
    else if 60 <= x < 100 then x_bin = 4;
    else x_bin = .;
run;

proc sql;
    select x_bin, count(*) as n
    from df
    group by x_bin
    order by x_bin;
quit;

/* Step 3: Calculate WoE and IV */
proc sql;
    create table bin_stats as
    select x_bin,
           sum(target=0) as good,
           sum(target=1) as bad
    from df
    group by x_bin;
quit;

proc sql noprint;
    select sum(good), sum(bad) into :total_good, :total_bad from bin_stats;
quit;

data woe_iv;
    set bin_stats;
    dist_good = good / &total_good.;
    dist_bad  = bad  / &total_bad.;
    woe = log((dist_good + 1e-6) / (dist_bad + 1e-6));
    iv = (dist_good - dist_bad) * woe;
run;

proc sql;
    select * from woe_iv;
quit;

proc sql;
    select sum(iv) as IV from woe_iv;
quit;

/* Step 4: Map WoE values */
proc sql;
    create table df_woe as
    select a.*, b.woe as x_woe
    from df as a
    left join woe_iv as b
    on a.x_bin = b.x_bin;
quit;

proc sql inobs=5;
    select * from df_woe;
quit;

/* Step 5: Logistic regression */
proc logistic data=df_woe desc;
    model target = x_woe;
    output out=preds p=prob;
run;

/* Step 6: ROC Curve */
/* Sort by predicted probability descending */
proc sort data=preds;
    by descending prob;
run;

/* Calculate cumulative TPR and FPR */
/* Calculate total positives and negatives */
proc sql noprint;
    select sum(target), count(*)-sum(target)
    into :total_pos, :total_neg
    from preds;
quit;

/* Calculate cumulative TPR and FPR */
data roc_points;
    set preds;
    retain tp fp 0;
    if target = 1 then tp + 1;
    else fp + 1;
    tpr = tp / &total_pos.;
    fpr = fp / &total_neg.;
    keep tpr fpr;
run;

/* Plot ROC curve */
proc sgplot data=roc_points;
    series x=fpr y=tpr / markers;
    lineparm x=0 y=0 slope=1 / transparency=0.5;
    xaxis label="False Positive Rate";
    yaxis label="True Positive Rate";
    title "Manual ROC Curve (WoE Binned)";
run;