# convert int to fixed length string
def int2str(i, length):
    s = str(i)
    if len(s) > length:
        raise ValueError("length is too short")
    return "0" * (length - len(s)) + s


# usage
print(int2str(123, 5))
print(int2str(123, 3))
print(int2str(0, 2))
print(int2str(1, 2))
print(int2str(9, 2))
print(int2str(10, 2))
print(int2str(15, 2))
