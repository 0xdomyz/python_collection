from custom_matrix import CustomMatrix


def calculate2(left: CustomMatrix, right: CustomMatrix):
    res = left**2 - right * 2 + 2
    return res


def calculate3(left: CustomMatrix, right: CustomMatrix):
    res = left * 2 - right
    return res
