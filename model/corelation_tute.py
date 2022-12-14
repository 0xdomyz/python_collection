# example of spearman correlation
from numpy.random import rand
from scipy.stats import kendalltau, pearsonr, somersd, spearmanr

# generate two independent random variables
data1 = 5 * rand(100) + 50
data2 = 5 * rand(100) + 50

# calculate spearman's correlation
coef, p = spearmanr(data1, data2)
print("Spearmans correlation: %.3f" % coef)
# calculate pearson correlation
coef, p = pearsonr(data1, data2)
print("Pearsons correlation: %.3f" % coef)
# calculate kendall's correlation
coef, p = kendalltau(data1, data2)
print("Kendalls correlation: %.3f" % coef)
# calculate somers' d correlation
_ = somersd(data1, data2)
print("Somersd correlation: %.3f" % _.statistic)
