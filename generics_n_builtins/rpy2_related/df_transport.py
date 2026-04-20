# %%
# rpy2 intro - simple data analysis demo
# Requires: pip install rpy2 pandas

import numpy as np
import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

# Activate automatic pandas <-> R dataframe conversion
pandas2ri.activate()

# ── 1. Basic R expressions ────────────────────────────────────────────────────
# %%
print(ro.r("R.version.string"))  # confirm R is reachable
print(ro.r("sqrt(144)"))  # simple scalar
print(ro.r("sum(1:100)"))  # vectorised operation

# ── 2. Send a Python DataFrame → R ───────────────────────────────────────────
# %%
df_py = pd.DataFrame(
    {
        "name": ["Alice", "Bob", "Carol", "Dave", "Eve"],
        "age": [25, 30, 35, 28, 22],
        "score": [88.5, 76.0, 92.3, 65.1, 81.7],
        "passed": [True, True, True, False, True],
    }
)

# Convert to an R dataframe and assign it to the R global environment
r_df = pandas2ri.py2rpy(df_py)
ro.globalenv["r_df"] = r_df

print(ro.r("str(r_df)"))  # inspect structure in R
print(ro.r("summary(r_df)"))  # descriptive stats in R

# ── 3. Run R analysis on the dataframe ───────────────────────────────────────
# %%
ro.r(
    """
    # mean / sd of score
    cat("Mean score :", mean(r_df$score), "\n")
    cat("SD   score :", sd(r_df$score),   "\n")

    # correlation between age and score
    cat("Cor(age, score):", cor(r_df$age, r_df$score), "\n")

    # simple linear regression: score ~ age
    model <- lm(score ~ age, data = r_df)
    print(summary(model))
"""
)

# ── 4. Receive an R DataFrame back into Python ───────────────────────────────
# %%
# Create a new dataframe in R (e.g. filtered / transformed result)
ro.r(
    """
    r_result <- r_df[r_df$passed == TRUE, ]
    r_result$grade <- ifelse(r_result$score >= 85, "A", "B")
"""
)

df_back = pandas2ri.rpy2py(ro.globalenv["r_result"])
print(type(df_back))
print(df_back)

# ── 5. Calling built-in R functions directly ─────────────────────────────────
# %%
base = importr("base")
stats = importr("stats")

scores = ro.FloatVector(df_py["score"].tolist())

print("quantiles:", stats.quantile(scores, ro.FloatVector([0.25, 0.5, 0.75])))
print("var      :", base.var(scores))

# ── 6. Using R's ggplot2 to produce a plot (saves to file) ───────────────────
# %%
try:
    ggplot2 = importr("ggplot2")
    ro.globalenv["r_df"] = pandas2ri.py2rpy(df_py)
    ro.r(
        """
        p <- ggplot2::ggplot(r_df, ggplot2::aes(x = age, y = score, colour = passed)) +
             ggplot2::geom_point(size = 3) +
             ggplot2::geom_smooth(method = "lm", se = FALSE) +
             ggplot2::labs(title = "Score vs Age", x = "Age", y = "Score")
        ggplot2::ggsave("score_vs_age.png", plot = p, width = 5, height = 4)
    """
    )
    print("Plot saved to score_vs_age.png")
except Exception as exc:
    print(f"ggplot2 not available or plot failed: {exc}")
