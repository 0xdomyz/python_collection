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
