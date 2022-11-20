from math import floor, log10

round_to_n = lambda x, n: round(x, -int(floor(log10(x))) + (n - 1))
