# example of itertools
import itertools

# count
for i in itertools.count(10, 2):
    if i == 20:
        break
    else:
        print(i)

# cycle
count = 0
for i in itertools.cycle("AB"):
    if count > 7:
        break
    print(i)
    count += 1

# repeat
for i in itertools.repeat(10, 4):
    print(i)

# accumulate
nums = [1, 5, 2, 6, 3, 2]
print(list(itertools.accumulate(nums)))

# chain
print(list(itertools.chain("AB", "CD")))

# compress
selectors = [True, False, True]

print(list(itertools.compress("ABCD", selectors)))

# dropwhile
print(list(itertools.dropwhile(lambda x: x < 5, nums)))

# accumulate for str
print(list(itertools.accumulate("ABCD", lambda acc, x: acc + x)))

# accumulate with operator
import operator

items = [1, 2, 3, 4]
print(list(itertools.accumulate(items, operator.mul)))

# combinations
items = ["A", "B", "C"]
for i in range(1, len(items) + 1):
    print(list(itertools.combinations(items, i)))

# accumulate for str items into lists
items = ["A", "B", "C"]
result = [["A"], ["A", "B"], ["A", "B", "C"]]

result = []
for i in range(len(items)):
    result.append(items[: i + 1])
print(result)


# accumulate items
def accumulate_items(items):
    result = []
    for i in range(len(items)):
        result.append(items[: i + 1])
    return result


items = ["A", "B", "C"]
accumulate_items(items)
accumulate_items([1, 2, 3, 4])
accumulate_items(["asdfasd", "asdfasdf", "asdfasdfasdf"])

# list
##############
lst = [1, 2, 3, 4, 5]

# find out position of 3
lst.index(3)
