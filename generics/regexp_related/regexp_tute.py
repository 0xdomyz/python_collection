# Spec
# ---------

import re

"""
metacharacters, escape with \
    \^$.|?*+()[{
"""

metacharacters = r"abc\^$.|?*+()[{123"

re.findall(r"\^", metacharacters)
re.findall(r"\\", metacharacters)
re.findall(r"\.", metacharacters)
re.findall(r"\$", metacharacters)

"""
Non-printable characters
    \t\r\n\a\e\f\v\
    \r\n
    \n
    \uFFFF
    \xA9
"""

"""
Character classes
    [abc]	any of a, b, or c
    [^abc]	not a, b, or c
    [a-g]	character between a & g
    [0-9a-fA-F] hexadecimal digit
"""

alphabet = "abcdefghijklmnopqrstuvwxyz"

re.findall("[abc]", alphabet)
re.findall("[^abc]", alphabet)
re.findall("[a-g]", alphabet)
re.findall("[0-9a-fA-F]", "0123456789abcdefABCDEF")

"""
Shorthand character classes
    .	any character except line break
    \d      - Digit (0-9)
    \D      - Not a Digit (0-9)
    \w      - Word Character (a-z, A-Z, 0-9, _)
    \W      - Not a Word Character
    \s      - Whitespace (space, tab, newline)
    \S      - Not Whitespace (space, tab, newline)
    \b      - Word Boundary
    \B      - Not a Word Boundary
"""

re.findall(r"\d", "fa34q")
re.findall(r"\D", "fa34q")
re.findall(r"\w", "1!, . rA3")
re.findall(r"\W", "1!, . rA3")
re.findall(r"\s", "1!, . rA3")
re.findall(r"\S", "1!, . rA3")
# re.findall(r"\b", "apple")
# for m in re.finditer(r"\B", "apple"):
#     print(m.start(), m.end(), m.group())


"""
Anchors
    ^       - Beginning of a String
    $       - End of a String
"""

re.findall(r"^a", "apple")
re.findall(r"e$", "apple")

"""
Alternation
    |       - Either Or
    (cat | dog) food
    cat | dog food
"""

re.findall(r"cat|dog", "cat food")
re.findall(r"cat|dog", "dog food")

"""
Repetition
    *       - 0 or More
    +       - 1 or More
    ?       - 0 or One
    {3}     - Exact Number
    {3,4}   - Range of Numbers (Minimum, Maximum)
    \b[1-9][0-9]{2,4}\b
"""

re.findall(r"ab*", "aababbb")
re.findall(r"ab+", "aababbb")
re.findall(r"ab?", "aababbb")
re.findall(r"ab{3}", "aababbb")
re.findall(r"ab{3,4}", "aababbb")

"""
Greedy and lazy repetition
    <.+> 
    <.+?> 
    <[^<>]+>

Add a ? to a quantifier to make it ungreedy i.e lazy
"""

re.findall(
    r"<.+>", "<html><title>My Title</title></html>"
)  # greedy, as long as possible
re.findall(r"<.+?>", "<html><title>My Title</title></html>")  # lazy, shorter

"""
Grouping and capturing
    ( )     - Group
    Set(Value)?
    Set(?:Value)?
    \0
"""

"""
Backreferences
    ([abc])=\1
"""

"""
Named groups and backreferences
    (?<mygroup>[abc])=\k<mygroup>
"""

"""
Unicode prop
    \p{L}
"""

"""
Lookaround
    q(?=u)	positive lookahead
    u(?!q)	negative lookahead
    (?<=a)b
    (?<!a)b

"""


def camel_to_snake(name: str) -> str:
    """
    Examples
    ---------------
    >>> camel_to_snake('CamelCaseName')
    'camel_case_name'
    >>> camel_to_snake('camelCaseName')
    'camel_case_name'
    >>> camel_to_snake('camel2_camel2_case')
    'camel2_camel2_case'
    >>> camel_to_snake('45rcamel2_camel2_case')
    '45rcamel2_camel2_case'
    >>> camel_to_snake('getHTTPResponseCode')
    'get_h_t_t_p_response_code'
    """
    # pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def camel_to_snake(name: str) -> str:
    """
    Examples
    ---------------
    >>> camel_to_snake('CamelCaseName')
    'camel_case_name'
    >>> camel_to_snake('camelCaseName')
    'camel_case_name'
    >>> camel_to_snake('camel2_camel2_case')
    'camel2_camel2_case'
    >>> camel_to_snake('45rcamel2_camel2_case')
    '45rcamel2_camel2_case'
    >>> camel_to_snake('getHTTPResponseCode')
    'get_http_response_code'
    >>> camel_to_snake('_CamelCaseName')
    '__camel_case_name'
    >>> camel_to_snake('_Camel_CaseName')
    '__camel__case_name'
    >>> camel_to_snake('__CamelCaseName')
    '___camel_case_name'
    """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def to_snake_case(name: str) -> str:
    """
    Examples
    ---------------
    >>> to_snake_case('CamelCaseName')
    'camel_case_name'
    >>> to_snake_case('camelCaseName')
    'camel_case_name'
    >>> to_snake_case('camel2_camel2_case')
    'camel2_camel2_case'
    >>> to_snake_case('45rcamel2_camel2_case')
    '45rcamel2_camel2_case'
    >>> to_snake_case('getHTTPResponseCode')
    'get_http_response_code'
    >>> to_snake_case('_CamelCaseName')
    '_camel_case_name'
    >>> to_snake_case('_Camel_CaseName')
    '_camel_case_name'
    >>> to_snake_case('__CamelCaseName')
    '__camel_case_name'
    """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def snake_to_camel(name: str) -> str:
    """
    Examples
    -----------
    >>> snake_to_camel('snake_case_name')
    'SnakeCaseName'
    >>> snake_to_camel('_snake_case_name')
    'SnakeCaseName'
    >>> snake_to_camel('__snake_case_name')
    'SnakeCaseName'
    """
    return "".join(word.title() for word in name.split("_"))


HREF_RE = re.compile(r'href="(.*?)"')
