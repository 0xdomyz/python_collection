import matplotlib.pylab as plt
import seaborn as sns

plt.subplot()
a, (b) = plt.subplots(gridspec_kw={})
b.set_xlabel()
b.set_xticks()
b.set_xticklabels()
b.twinx()
plt.yscale()
b.plot()
b.legend()
b.bar()
plt.subplots_adjust()
plt.close()
