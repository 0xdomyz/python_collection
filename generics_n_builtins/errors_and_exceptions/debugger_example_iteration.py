### Guided tour of debugger actions using iteration and function calls.


def transform(x):
    return x * 2  # 5: inspect call stack, then step out


def process_list(
    values,
):  # 3: keep stepping over to meet next comment, then keep stepping over
    total = 0
    for v in values:
        if v % 2 == 0:
            total += transform(v)  # 4: Step into
        else:
            total += v
    return total


data = [1, 2, 3]
result = process_list(data)  # 1: Breakpoint to start, 2: Step into
print(result)
