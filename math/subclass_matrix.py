import numpy as np


# CustomMatrix class, represented by a numpy 2D array (matrix)
class CustomMatrix(object):
    # constructor from a numpy 2D array
    def __init__(self, matrix: np.ndarray):
        matrix = matrix.copy()
        self.check_matrix(matrix)
        self.matrix = self.invariant(matrix)

    # check if the input is a numpy 2D array
    def check_matrix(self, matrix: np.ndarray):
        if not isinstance(matrix, np.ndarray):
            raise TypeError(f"Input matrix is not a numpy array, but {type(matrix)}")
        if matrix.ndim != 2:
            raise TypeError(f"Input matrix is not a 2D array, but {matrix.ndim}D")

    # copy
    def copy(self):
        return self.__class__(self.matrix)

    # clean the input matrix
    #   fill na with 0
    def invariant(self, matrix: np.ndarray):
        return np.nan_to_num(matrix)

    # display the matrix
    #  use the __str__ method
    def __repr__(self):
        return self.__str__()

    # display the matrix
    #   "CustomMatrix"
    #   dimensions
    #   top 5 rows and columns if the matrix is large
    #   the whole matrix if the matrix is small
    def __str__(self):
        payload = f"CustomMatrix: {self.matrix.shape}"
        if self.matrix.size > 25:
            payload += "\nTop 5 rows and columns:"
            payload += f"\n{self.matrix[:5, :5]}"
        else:
            payload += f"\n{self.matrix}"
        return payload

    # allow indexing
    def __getitem__(self, key):
        return self.matrix[key]

    # allow setting values
    def __setitem__(self, key, value):
        self.matrix[key] = value

    # allow adding and subtracting
    def __add__(self, other):
        return self._dispatch_to_add(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self._dispatch_to_add(-other)

    def __rsub__(self, other):
        # other - self
        return (-self).__add__(other)

    # unary minus
    def __neg__(self):
        return CustomMatrix(-self.matrix)

    # dispatch to the correct add method
    # depending on the type of the other object
    def _dispatch_to_add(self, other):
        if isinstance(other, CustomMatrix):
            if self.matrix.shape != other.matrix.shape:
                raise ValueError(
                    f"Matrices have different shapes: {self.matrix.shape} and {other.matrix.shape}"
                )
            return CustomMatrix(self.matrix + other.matrix)
        elif isinstance(other, np.ndarray):
            other = CustomMatrix(other)
            return self._dispatch_to_add(other)
        elif isinstance(other, (int, float)):
            return CustomMatrix(self.matrix + other)
        else:
            raise TypeError(
                f"Cannot add a CustomMatrix to a {type(other)} object. Try converting it to a CustomMatrix first."
            )

    # allow multiplying to a scalar
    def __mul__(self, other):
        return CustomMatrix(self.matrix * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    # allow dividing by a scalar
    def __truediv__(self, other):
        return CustomMatrix(self.matrix / other)


if __name__ == "__main__":
    # dirty one
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, np.nan]])
    print(CustomMatrix(m))

    # small one
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(CustomMatrix(m))

    # large one
    m = np.random.rand(100, 100)
    print(CustomMatrix(m))

    # clean one
    # also as invariant for testing
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    cm = CustomMatrix(m)
    print(cm)
    cm

    # indexing
    print(cm[0, 0])

    assert cm[0, 0] == 1

    # setting and copying
    cm2 = cm.copy()
    cm2[0, 0] = 10
    print(cm2[0, 0])

    assert cm2[0, 0] == 10

    # adding and subtracting
    cm2 = cm * 2
    print(cm + cm2)
    print(cm - cm2)

    assert (cm + cm2)[0, 0] == 3
    assert (cm - cm2)[0, 0] == -1

    # adding a scalar
    print(cm + 1)
    print(2 + cm)

    assert (cm + 1)[0, 0] == 2
    assert (2 + cm)[0, 0] == 3

    # multiplying by a scalar
    print(cm * 2)
    print(-3 * cm)

    assert (cm * 2)[0, 0] == 2
    assert (-3 * cm)[0, 0] == -3

    # dividing by a scalar
    print(cm / 2)

    assert (cm / 2)[0, 0] == 0.5

    # unary minus
    print(-cm)

    assert (-cm)[0, 0] == -1

    # average of 3 matrices
    cm2 = CustomMatrix(m) * 2
    cm3 = CustomMatrix(m) - 1
    cm_avg = (cm + cm2 + cm3) / 3
    print(cm_avg)

    assert cm_avg[0, 1] == (2 + 4 + 1) / 3

    # sum from a list of matrices
    cm_sum = sum([cm, cm2, cm3])
    print(cm_sum)

    # adding a numpy array
    m2 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) * 2
    print(cm + m2)

    assert (cm + m2)[0, 0] == 3

    # shape mismatch
    m2 = np.array([[1, 2, 3], [4, 5, 6]])
    try:
        cm + m2
    except ValueError as e:
        print(e)

    # type mismatch
    try:
        cm + "a"
    except TypeError as e:
        print(e)

    # subclassing
    class CustomMatrix2(CustomMatrix):
        def __init__(self, matrix, info=None):
            super().__init__(matrix)
            self.info = "no info" if info is None else info

        def __str__(self):
            parent_str = super().__str__()
            # replace the class name
            res = parent_str.replace("CustomMatrix", "CustomMatrix2")
            # add the info
            res += f"\n{self.info}"
            return res

        def _combine_potential_infos(self, other):
            # if both are CustomMatrix2 and both have info and info differ, give "no info"
            if hasattr(self, "info") and hasattr(other, "info"):
                if self.info != other.info:
                    info = "no info"
                else:
                    info = self.info
            else:
                info = self.info
            return info

        def __add__(self, other):
            res = super().__add__(other)
            info = self._combine_potential_infos(other)
            return CustomMatrix2(res.matrix, info=info)

        def __radd__(self, other):
            return self.__add__(other)

        def calculate(self):
            res = self * 2
            return CustomMatrix2(res.matrix, info=self.info)

        def calculate2(self, other):
            if not isinstance(other, CustomMatrix):
                raise TypeError(
                    f"cannot calculate2 with a {type(other)} object. Try converting it to a CustomMatrix first."
                )
            res = self * 2 - other
            return CustomMatrix2(res.matrix, info=self.info)

    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    prnt = CustomMatrix(m)
    cm = CustomMatrix2(m, info="cm")
    cm2 = CustomMatrix2(m * 2, info="cm2")
    cm3 = CustomMatrix2(m * 3)

    # print
    cm
    cm2
    cm3

    # overriding method
    cm + cm2

    # parent method
    (cm * 2)

    # new method
    cm.calculate()

    # new method with binary operator
    cm.calculate2(cm2)
    cm.calculate2(cm3)
    cm3.calculate2(prnt)
