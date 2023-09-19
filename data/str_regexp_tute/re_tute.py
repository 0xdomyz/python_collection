import re


def displaymatch(match: re.Match) -> str:
    """
    Examples
    ------------
    >>> _ = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
    >>> _
    <re.Match object; span=(0, 12), match='Isaac Newton'>
    >>> displaymatch(_)
    "<Match: 'Isaac Newton', groups=('Isaac', 'Newton')>"
    """
    if match is None:
        return None
    return "<Match: %r, groups=%r>" % (match.group(), match.groups())


# validate poker hand
valid = re.compile(r"^[a2-9tjqk]{5}$")  # a pattern that matches a poker hand
displaymatch(valid.match("akt5q"))  # Valid.
displaymatch(valid.match("akt5e"))  # Invalid.
displaymatch(valid.match("akt"))  # Invalid.
displaymatch(valid.match("727ak"))  # Valid.

# detect pair via backreference
pair = re.compile(r".*(.).*\1")
# 0 or more of any, then potential first occurrence,
# then 0 or more of any, then the 2nd occurrence
# making a pair
displaymatch(pair.match("717ak"))  # Pair of 7s.
displaymatch(pair.match("718ak"))  # No pairs.
displaymatch(pair.match("354aa"))  # Pair of aces.
displaymatch(pair.match("aa778"))  # greedy
displaymatch(re.compile(r".*?(.).*?\1").match("aa778"))  # non-greedy

pair.match("717ak").group()  # the whole match
pair.match("717ak").group(1)  # the first group

# https://docs.python.org/3/library/re.html#simulating-scanf
