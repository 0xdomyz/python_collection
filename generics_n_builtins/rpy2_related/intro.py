# %%
# rpy2 – examples adapted from the official introduction
# https://rpy2.github.io/doc/latest/html/introduction.html
# Requires: pip install rpy2 pandas

# %% [markdown]
# ###
# ── 1. Version / environment check ───────────────────────────────────────────

# %%
import importlib

import rpy2.robjects as robjects

print(importlib.metadata.metadata("rpy2")["version"])
# %%
import rpy2.situation

for row in rpy2.situation.iter_info():
    print(row)

# %% [markdown]
# ###
# ── 2. Importing R packages ───────────────────────────────────────────────────
# %%
from rpy2.robjects.packages import importr

base = importr("base")
# %%
# install
rpy2.robjects.packages.importr("utils").install_packages("stats")

# %%
stats = importr("stats")

# %% [markdown]
# ###
# ── 3. The r instance – getting R objects & evaluating R code ─────────────────
# %%
# get a built-in R constant
res = robjects.r["pi"]
print(f"{type(res) = }")
res[0]

# %%

# define and call an R function inside a code string
robjects.r(
    """
    f <- function(r, verbose = FALSE) {
        if (verbose) cat("calling f().\n")
        2 * pi * r
    }
    f(3)
"""
)
# %%

# retrieve the function into Python and call it
r_f = robjects.globalenv["f"]
print(r_f.r_repr())  # show R source
res = r_f(3)
print(res[0])  # ≈ 18.85

# %% [markdown]
# ###
# ── 4. Interpolating R objects into R code strings ───────────────────────────
# %%
letters = robjects.r["letters"]
rcode = 'paste(%s, collapse="-")' % letters.r_repr()
res = robjects.r(rcode)
print(res[0])  # "a-b-c-…-z"

# %% [markdown]
# ###
# ── 5. Creating R vectors ─────────────────────────────────────────────────────
# %%
str_vec = robjects.StrVector(["abc", "def"])
int_vec = robjects.IntVector([1, 2, 3])
float_vec = robjects.FloatVector([1.1, 2.2, 3.3])

print(str_vec.r_repr())  # c("abc", "def")
print(int_vec.r_repr())  # 1:3
print(float_vec.r_repr())  # c(1.1, 2.2, 3.3)

# R matrix (vector + dim attribute)
v = robjects.FloatVector([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])
m = robjects.r["matrix"](v, nrow=2)
print(m)

# %% [markdown]
# ###
# ── 6. Calling R functions ────────────────────────────────────────────────────
# %%
rsum = robjects.r["sum"]
print(rsum(robjects.IntVector([1, 2, 3]))[0])  # 6

rsort = robjects.r["sort"]
res = rsort(robjects.IntVector([1, 2, 3]), decreasing=True)
print(res.r_repr())  # c(3L, 2L, 1L)

# %% [markdown]
# ###
# ── 7. Linear model (from official tutorial) ──────────────────────────────────
# %%
from rpy2.robjects import FloatVector

ctl = FloatVector([4.17, 5.58, 5.18, 6.11, 4.50, 4.61, 5.17, 4.53, 5.33, 5.14])
trt = FloatVector([4.81, 4.17, 4.41, 3.59, 5.87, 3.83, 6.03, 4.89, 4.32, 4.69])
group = base.gl(2, 10, 20, labels=["Ctl", "Trt"])
weight = ctl + trt

robjects.globalenv["weight"] = weight
robjects.globalenv["group"] = group

lm_D9 = stats.lm("weight ~ group")
print(stats.anova(lm_D9))

# omitting intercept
lm_D90 = stats.lm("weight ~ group - 1")
print(base.summary(lm_D90))

# extract named elements from the lm result
print(lm_D9.rx2("coefficients"))  # rx2 → $  (single element)
print(lm_D9.rx("coefficients"))  # rx  → [  (list element)

# %% [markdown]
# ###

# ── 8. PCA (from official tutorial) ──────────────────────────────────────────
# %%
graphics = importr("graphics")

m = base.matrix(stats.rnorm(100), ncol=5)
pca = stats.princomp(m)
print(base.summary(pca))  # numeric summary; skip interactive plot
pca = stats.princomp(m)
print(base.summary(pca))  # numeric summary; skip interactive plot
