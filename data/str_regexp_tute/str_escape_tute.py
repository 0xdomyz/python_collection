# example to show python string escape sequences
##########################################################

# single quote
print("I'm a single quoted string")

# double quote
print("I'm a double quoted string")

# triple quote
print("""I'm a triple quoted string""")

# triple quote with double quotes
print("""I'm a triple quoted string with "double quotes" inside""")

# triple quote with single quotes
print("""I'm a triple quoted string with 'single quotes' inside""")

# triple quote with double quotes and single quotes
print("""I'm a triple quoted string with "double quotes" and 'single quotes' inside""")

# triple quote with single quotes and double quotes
print("""I'm a triple quoted string with 'single quotes' and "double quotes" inside""")

# triple quote with double quotes and single quotes and backslash
print(
    """I'm a triple quoted string with "double quotes" and 'single quotes' and \\ backslash inside"""
)

# triple quote with single quotes and double quotes and backslash
print(
    """I'm a triple quoted string with 'single quotes' and "double quotes" and \\ backslash inside"""
)

# triple quote with double quotes and single quotes and backslash and newline
print(
    """I'm a triple quoted string with "double quotes" and 'single quotes' and \\ backslash and

newline inside"""
)

# triple quote with single quotes and double quotes and backslash and newline
print(
    """I'm a triple quoted string with 'single quotes' and "double quotes" and \\ backslash and

newline inside"""
)


# example to show python string escape special characters
##########################################################

# backslash
print("I'm a backslash \\ inside a string")

# single quote
print("I'm a single quote ' inside a string")

# double quote
print("I'm a double quote \" inside a string")

# newline
print(
    """I'm a newline

inside a string"""
)
print(
    r"""I'm a newline

inside a string"""
)

# tab
print("I'm a tab \t inside a string")

# carriage return
print("I'm a carriage return \r inside a string")

# backspace
print("I'm a backspace \b inside a string")

# formfeed
print("I'm a formfeed \f inside a string")

# vertical tab
print("I'm a vertical tab \v inside a string")

# bell
print("I'm a bell \a inside a string")

# null
print("I'm a null \0 inside a string")


# example to show python string escape octal characters
##########################################################

# octal 0
print("I'm octal 0 \0 inside a string")

# octal 1
print("I'm octal 1 \1 inside a string")

# octal 2
print("I'm octal 2 \2 inside a string")

# octal 3
print("I'm octal 3 \3 inside a string")

# octal 4
print("I'm octal 4 \4 inside a string")


# example to show python string escape hex characters
##########################################################

# hex 0
print("I'm hex 0 \x00 inside a string")


# example to show python string escape unicode characters
##########################################################

# unicode 0
print("I'm unicode 0 \u0000 inside a string")

# unicode 1
print("I'm unicode 1 \u0001 inside a string")


# example to show python raw string
##########################################################

# raw string
print(r"I'm a raw string \ inside a string")

# raw string with tab
print(r"I'm a raw string \t inside a string")


# example to show python binary string
##########################################################

# binary string
print(b"I'm a binary string \ inside a string")

# binary string with tab
print(b"I'm a binary string \t inside a string")
