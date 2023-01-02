# list of string formats
# https://docs.python.org/3/library/string.html#format-string-syntax


# format number
######################

f"abc {1+2} def"

# format number with 2 decimal places
f"abc {1+2:.2f} def"

# format number with 2 decimal places and 10 spaces
f"abc {1+2:10.2f} def"

# left align
f"abc {1+2:<10.2f} def"

# right align
f"abc {1+2:>10.2f} def"

# center align
f"abc {1+2:^10.2f} def"

# fill with 0
f"abc {1+2:010.2f} def"
[f"{i:02}" for i in range(20)]

# thousands separator
f"abc {1+2*1000:,.2f} def"

# scientific notation
f"abc {1+2*1000:.2e} def"

# rounding to 1 decimal place
f"abc {1.03+2*10:.1f} def"

# rounding to 2 significant figures
f"abc {1.03+2*10:.2g} def"

# percentage
f"abc {1.03+2*10:.2%} def"

# alpha numeric
######################

# format string with 10 spaces
f"abc {1+2:10s} def"

# left align
f"abc {1+2:<10s} def"

# right align
f"abc {1+2:>10s} def"

# template string
######################

# template string
from string import Template

t = Template("abc $x def")
t.substitute(x=1 + 2)

# template string with 2 decimal places
t = Template("abc $x:.2f def")
t.substitute(x=1 + 2)

# multiple substitutions
t = Template("abc $x def $y")
subs = {"x": 1 + 2, "y": 3 + 4}

t.substitute(subs)

# substitute a list
t = Template("abc $x def $y")
subs = [1 + 2, 3 + 4]

t.substitute(x=subs[0], y=subs[1])
