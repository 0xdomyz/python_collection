"""
Spec
---------

metacharacters, escape with \
    \^$.|?*+()[{

Non-printable characters
    \t\r\n\a\e\f\v\
    \r\n
    \n
    \uFFFF
    \xA9

Character classes
    [abc]	any of a, b, or c
    [^abc]	not a, b, or c
    [a-g]	character between a & g
    [0-9a-fA-F] hexadecimal digit

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

Anchors
    ^       - Beginning of a String
    $       - End of a String

Alternation
    |       - Either Or
    (cat | dog) food
    cat | dog food

Repetition
    *       - 0 or More
    +       - 1 or More
    ?       - 0 or One
    {3}     - Exact Number
    {3,4}   - Range of Numbers (Minimum, Maximum)
    \b[1-9][0-9]{2,4}\b

Greedy and lazy repetition
    <.+> 
    <.+?> 
    <[^<>]+>

Grouping and capturing
    ( )     - Group
    Set(Value)?
    Set(?:Value)?
    \0

Backreferences
    ([abc])=\1

Named groups and backreferences
    (?<mygroup>[abc])=\k<mygroup>

Unicode prop
    \p{L}

Lookaround
    q(?=u)	positive lookahead
    u(?!q)	negative lookahead
    (?<=a)b
    (?<!a)b

"""

#https://docs.python.org/3/library/re.html#regular-expression-examples


import re

def camel_to_snake(name:str)->str:
    """
    Examples
    ---------------
    >>> camel_to_snake('CamelCaseName')
    'camel_case_name'
    """
    #pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def camel_to_snake(name):
    """
    Examples
    ---------------
    >>> camel_to_snake('camel2_camel2_case')
    'camel2_camel2_case'
    >>> camel_to_snake('getHTTPResponseCode')
    'get_http_response_code'
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def to_snake_case(name):
    """
    Examples
    ---------------
    >>> camel_to_snake('camel2_camel2__case')
    'camel2_camel2__case'
    >>> camel_to_snake('getHTTPResponseCode')
    'get_http_response_code'
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()

def snake_to_camel(name:str)->str:
    """
    Examples
    -----------
    >>> snake_to_camel('snake_case_name')
    'SnakeCaseName'
    """
    return ''.join(word.title() for word in name.split('_'))



