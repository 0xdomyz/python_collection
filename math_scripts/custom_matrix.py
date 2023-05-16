import numpy as np
import pandas as pd


class CustomMatrix(object):
    """
    CustomMatrix is a wrapper around numpy array or matrix
    With some additional functionalities:
        - clean data
        - display the matrix
        - from and to pandas DataFrame, to csv
        - dispatch operations to numpy, so that can be used in numpy operations,
            similar to numpy array or matrix
        - to be used as a base class for more specialized matrixes, with more
            functionalities

    """

    # invariant: matrix is a numpy array or matrix
    def __init__(self, matrix: np.ndarray | np.matrix | int | float):
        if isinstance(matrix, np.matrix):
            matrix = self.clean_array(matrix)
        elif isinstance(matrix, np.ndarray):
            if matrix.ndim > 2:
                raise TypeError(
                    f"Input array is not a 1D or 2D array, but {matrix.ndim}D"
                )
            matrix = self.clean_array(matrix)
        elif isinstance(matrix, int):
            matrix = np.array([matrix])
            matrix = self.clean_array(matrix)
        elif isinstance(matrix, float):
            matrix = np.array([matrix])
            matrix = self.clean_array(matrix)
        else:
            raise TypeError(
                "Input matrix is not a numpy array or matrix or int or float, "
                f"but {type(matrix)}"
            )
        self.matrix = matrix

    # initialize from a pandas DataFrame
    # require all numeric
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Input is not a pandas DataFrame, but {type(df)}")
        if not df.select_dtypes(include=np.number).columns.equals(df.columns):
            raise TypeError("Not all columns are numeric")

        # convert to numpy array, each row in df becomes rows in the matrix
        matrix = df.to_numpy()  # .T
        return cls(matrix)

    def to_dataframe(self):
        return pd.DataFrame(self.matrix)

    def to_csv(self, path, **kwargs):
        self.to_dataframe().to_csv(path, **kwargs)

    # initialize list of mat from a pandas dataframe with a column of label that
    #  will be used as the index for matrixes
    @classmethod
    def from_dataframe_with_label(cls, df: pd.DataFrame, label: str):
        labels = np.sort(df[label].unique())
        df_list = [df[df[label] == l].drop(columns=label).copy() for l in labels]
        matrixes = [cls.from_dataframe(df) for df in df_list]
        return matrixes

    # copy
    def copy(self):
        return self.__class__(self.matrix)

    # clean the input matrix
    #   fill all sorts of nan, NA, None with 0
    #   convert to float
    def clean_array(self, matrix):
        matrix = matrix.copy()
        matrix = np.where(matrix == None, 0, matrix)
        matrix = matrix.astype(float)
        matrix = np.nan_to_num(matrix)
        return matrix

    # display the matrix
    #  use the __str__ method
    def __repr__(self):
        return self.__str__()

    # display the matrix
    #   "CustomMatrix"
    #   dimensions
    #   5 rows and columns if the matrix is large
    #   the whole matrix if the matrix is small
    def __str__(self):
        if self.ndim == 1:
            payload = f"CustomMatrix: {self.shape[0]}"
            payload += f"\n{self.matrix}"
        else:
            payload = f"CustomMatrix: {self.shape}"
            row, col = self.shape
            if row > 5 or col > 5:
                payload += ", Top 5 rows and columns:"
                payload += f"\n{self.matrix[:5, :5]}"
            else:
                payload += f"\n{self.matrix}"

        return payload

    # despatch various operations to numpy
    def _dispatch_to_numpy(self, other, method):
        if isinstance(other, CustomMatrix):
            return self.__class__(method(self.matrix, other.matrix))
        elif isinstance(other, np.ndarray):
            res = method(self.matrix, other)
            return self.__class__(res)
        elif isinstance(other, (int, float)):
            return self.__class__(method(self.matrix, other))
        else:
            raise TypeError(
                f"Cannot operate on a CustomMatrix and a {type(other)} object. "
                "Try converting it to a CustomMatrix first."
            )

    # some magical methods
    def __getitem__(self, key):
        res = self.matrix[key]
        if isinstance(res, np.ndarray):
            res = self.__class__(res)
        return res

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def __len__(self):
        return len(self.matrix)

    def __and__(self, other):
        return self._dispatch_to_numpy(other, np.logical_and)

    def __or__(self, other):
        return self._dispatch_to_numpy(other, np.logical_or)

    def __le__(self, other):
        return self._dispatch_to_numpy(other, np.less_equal)

    def __lt__(self, other):
        return self._dispatch_to_numpy(other, np.less)

    def __ge__(self, other):
        return self._dispatch_to_numpy(other, np.greater_equal)

    def __gt__(self, other):
        return self._dispatch_to_numpy(other, np.greater)

    def __eq__(self, other):
        return self._dispatch_to_numpy(other, np.equal)

    # some numpy methods

    def sum(self, axis=None):
        return self.matrix.sum(axis=axis)

    def flatten(self):
        return self.matrix.flatten()

    @property
    def shape(self):
        return self.matrix.shape

    @property
    def size(self):
        return self.matrix.size

    @property
    def ndim(self):
        return self.matrix.ndim

    @property
    def T(self):
        return self.__class__(self.matrix.T)

    def reshape(self, *args, **kwargs):
        return self.__class__(self.matrix.reshape(*args, **kwargs))

    def mean(self, axis=None):
        return self.matrix.mean(axis=axis)

    def std(self, axis=None):
        return self.matrix.std(axis=axis)

    def min(self, axis=None):
        return self.matrix.min(axis=axis)

    def max(self, axis=None):
        return self.matrix.max(axis=axis)

    def median(self, axis=None):
        return np.median(self.matrix, axis=axis)

    def count_nonzero(self, axis=None):
        return np.count_nonzero(self.matrix, axis=axis)

    def row_all_zero(self):
        if self.ndim == 1:
            axis = 0
        else:
            axis = 1
        return np.all(self.matrix == 0, axis=axis)

    # some numpy methods that return a CustomMatrix: todo

    # allow adding and subtracting
    def __add__(self, other):
        # return self._dispatch_to_add(other)
        return self._dispatch_to_numpy(other, np.add)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self._dispatch_to_numpy(other, np.subtract)

    def __rsub__(self, other):
        # other - self
        return (-self).__add__(other)

    # unary minus
    def __neg__(self):
        return self._dispatch_to_numpy(-1, np.multiply)

    # allow multiplying to a scalar
    def __mul__(self, other):
        return self._dispatch_to_numpy(other, np.multiply)

    def __rmul__(self, other):
        return self.__mul__(other)

    # allow dividing by a scalar
    def __truediv__(self, other):
        return self._dispatch_to_numpy(other, np.divide)

    # power
    def __pow__(self, other):
        return self._dispatch_to_numpy(other, np.power)

    # matrix multiplication
    def __matmul__(self, other):
        return self._dispatch_to_numpy(other, np.matmul)


import custom_matrix_support


class CustomMatrix2(CustomMatrix):
    def __init__(self, matrix, info=None):
        super().__init__(matrix)
        self.info = info

    def __str__(self):
        parent_str = super().__str__()
        # replace the class name
        res = parent_str.replace("CustomMatrix", "CustomMatrix2")
        # add info and others
        res += f"\n{self.info}"
        res += f", non-zeros: {self.count_nonzero()}"
        res += f", all zero rows: {self.row_all_zero().sum()}"
        return res

    @classmethod
    def from_dataframe_with_label(cls, df: pd.DataFrame, label: str):
        res = super().from_dataframe_with_label(df, label)
        labels = np.sort(df[label].unique())
        for i, cm in enumerate(res):
            cm.info = labels[i]
        return res

    def _combine_potential_infos(self, other):
        # if both are CustomMatrix2 and both have info not none
        if isinstance(other, CustomMatrix2) and (
            self.info is not None and hasattr(other, "info") and other.info is not None
        ):
            if self.info != other.info:
                info = None
            else:
                info = self.info
        else:
            info = self.info
        return info

    # override usage of self.__class__

    def __copy__(self):
        return self.__class__(self.matrix, info=self.info)

    def _dispatch_to_numpy(self, other, func):
        info = self._combine_potential_infos(other)
        res = super()._dispatch_to_numpy(other, func)
        return self.__class__(res.matrix, info=info)

    def __getitem__(self, key):
        res = super().__getitem__(key)
        if isinstance(res, CustomMatrix):
            res = self.__class__(res.matrix, info=self.info)
        return res

    @property
    def T(self):
        return self.__class__(self.matrix.T, info=self.info)

    @property
    def reshape(self, *args, **kwargs):
        return self.__class__(self.matrix.reshape(*args, **kwargs), info=self.info)

    # new methods

    def calculate(self):
        res = calculate(matrix=self)
        return self.__class__(res.matrix, info=self.info)

    def calculate2(self, other):
        if not isinstance(other, CustomMatrix):
            raise TypeError(
                f"cannot calculate2 with a {type(other)} object. "
                "Try converting it to a CustomMatrix first."
            )
        res = custom_matrix_support.calculate2(self, other)
        return self.__class__(res.matrix, info=self.info)

    def calculate3(self, other):
        if not isinstance(other, CustomMatrix):
            raise TypeError(
                f"cannot calculate3 with a {type(other)} object. "
                "Try converting it to a CustomMatrix first."
            )
        res = custom_matrix_support.calculate3(self, other)
        return self.__class__(res.matrix, info=self.info)


def calculate(matrix):
    res = matrix**2
    return res


if __name__ == "__main__":
    # if run interactively
    """
    ::

        python3.11
        from custom_matrix import *
    """

    # dirty one
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, np.nan]])
    print(CustomMatrix(m))

    # small one
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(CustomMatrix(m))

    # large one
    m = np.random.rand(100, 100)
    print(CustomMatrix(m))

    # initialisation from matrix
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, np.nan]])
    cm2 = CustomMatrix(m)
    assert cm2[0, 0] == 1
    cm2

    # initialisation from dataframe
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, np.nan]])
    df = pd.DataFrame(m)
    cm3 = CustomMatrix.from_dataframe(df)
    assert cm3[0, 0] == 1
    cm3

    # to dataframe
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    df = pd.DataFrame(m)
    cm3 = CustomMatrix.from_dataframe(df)
    df2 = cm3.to_dataframe()
    assert df.astype(float).equals(df2.astype(float))

    # to csv
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    df = CustomMatrix(m).to_dataframe()
    df.to_csv("test.csv", index=False)

    # snippet to go from stack of dataframe matrixes to list of CustomMatrix
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, np.nan]])
    df = pd.DataFrame(m)
    df = pd.concat([df, df * 2, df * 3], axis=0)
    dates = pd.date_range("2021-01-01", periods=3)
    # expand the dates by size of the matrixes
    dates_expanded = np.repeat(dates, df.shape[0] / len(dates))
    df["date"] = dates_expanded
    # input
    df
    # list of unique dates
    dates = np.sort(df["date"].unique())
    # list of dataframes, one per date, with date column removed
    df_list = [df[df["date"] == d].copy() for d in dates]
    for d in df_list:
        d.drop("date", axis=1, inplace=True)
    # list of CustomMatrix
    cm_list = [CustomMatrix.from_dataframe(d) for d in df_list]
    for date, cm in zip(dates, cm_list):
        cm.info = date
    # results
    cm_list[0]
    cm_list[1]
    cm_list[2]

    # from df with labels
    lst = CustomMatrix.from_dataframe_with_label(df=df, label="date")
    lst[0]
    lst[1]
    lst[2]

    # from 1d array
    m = np.array([1, 2, 3])
    cm = CustomMatrix(m)
    print(cm)

    # from int or float
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    cm = CustomMatrix(m)
    cm_float = CustomMatrix(1.2)
    cm_float_matrix = CustomMatrix(np.array([[1.2]]))

    cm + cm_float
    cm * cm_float

    cm + cm_float_matrix
    cm * cm_float_matrix

    # clean one
    # also as invariant for testing
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    cm = CustomMatrix(m)
    print(cm)
    cm

    # indexing
    res = cm[0, 0]
    assert res == 1
    assert isinstance(res, np.float64)

    res = cm[0, :]
    assert isinstance(res, CustomMatrix)
    assert res.shape == (3,)

    res = cm[:, 0]
    assert isinstance(res, CustomMatrix)
    assert res.shape == (3,)

    # setting and copying
    cm2 = cm.copy()
    cm2[0, 0] = 10

    assert cm2[0, 0] == 10

    # adding and subtracting
    cm2 = cm * 2

    assert (cm + cm2)[0, 0] == 3
    assert (cm - cm2)[0, 0] == -1

    # adding a scalar
    assert (cm + 1)[0, 0] == 2
    assert (2 + cm)[0, 0] == 3

    # multiplying by a scalar
    assert (cm * 2)[0, 0] == 2
    assert (-3 * cm)[0, 0] == -3

    # dividing by a scalar
    assert (cm / 2)[0, 0] == 0.5

    # mul/divide by array
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    cm = CustomMatrix(m)

    assert (cm / np.array([1, 2, 3]))[0, 1] == 1
    assert (cm / np.array([1, 2, 3]).reshape(-1, 1))[0, 1] == 2

    one_d = cm[:, 0]
    cm
    one_d
    _ = cm / one_d
    assert _[0, 1] == 0.5
    _ = cm / one_d.reshape(-1, 1)
    assert _[0, 1] == 2

    _ = cm * one_d
    assert _[0, 1] == 8
    _ = cm * one_d.reshape(-1, 1)
    assert _[0, 1] == 2

    # power
    assert ((cm**2 == cm * cm) - 1).sum() == 0

    # matrix multiplication
    assert (cm @ cm)[0, 0] == 30
    cm[:, -1] @ cm

    # unary minus
    assert (-cm)[0, 0] == -1

    # average of 3 matrices
    cm2 = CustomMatrix(m) * 2
    cm3 = CustomMatrix(m) - 1
    cm_avg = (cm + cm2 + cm3) / 3

    assert cm_avg[0, 1] == (2 + 4 + 1) / 3

    # sum from a list of matrices
    cm_sum = sum([cm, cm2, cm3])

    assert cm_sum[0, 1] == 2 + 4 + 1

    # adding a numpy array
    m2 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) * 2

    assert (cm + m2)[0, 0] == 3

    # type mismatch
    try:
        cm + "a"
    except TypeError as e:
        msg_part = "Cannot operate on a CustomMatrix and a <class 'str'> object."
        if msg_part not in str(e):
            raise e

    # magic methods: len and or le lt etc
    assert len(cm) == 3
    assert cm < 10
    assert cm <= 10
    assert cm > 0
    assert cm >= 0
    assert cm == cm

    # numpy methods: min, max, mean, sum, median
    assert cm.min() == 1
    assert cm.max() == 9
    assert cm.mean() == 5
    assert (cm.mean(axis=0) == np.array([4, 5, 6])).sum() == 3
    assert (cm.mean(axis=1) == np.array([2, 5, 8])).sum() == 3
    assert cm.sum() == 45
    assert cm.median() == 5
    assert cm.count_nonzero() == 9

    m = np.array([[1, 2, 3], [0, np.nan, None], [7, 8, np.nan]])
    cm = CustomMatrix(m)
    assert cm.count_nonzero() == 5
    assert (cm.row_all_zero() == np.array([False, True, False])).sum() == 3

    # subclassing
    ########################
    m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    prnt = CustomMatrix(m)
    cm = CustomMatrix2(m, info="cm")
    cm2 = CustomMatrix2(m * 2, info="cm2")
    cm_noinfo = CustomMatrix2(m * 3)

    # list of df with labels
    df = pd.DataFrame(
        {
            "a": [1, 1, 2, 2],
            "b": [1, 2, 3, 4],
            "c": [5, 6, 7, 8],
            "label": ["a", "a", "b", "b"],
        }
    )
    df
    cm_list = CustomMatrix2.from_dataframe_with_label(df, "label")
    assert cm_list[0].info == "a"
    assert cm_list[1].info == "b"
    # row number
    assert cm_list[0].shape[0] == 2

    # print
    print(cm)
    print(cm2)
    print(cm_noinfo)

    cm_has_all_zero = CustomMatrix2(np.zeros((3, 3)), info="cm_has_all_zero")
    print(cm_has_all_zero)

    one_d = cm[:, 0]
    print(one_d)

    one_d_has_all_zero = CustomMatrix2(np.zeros((1, 3)), info="one_d_has_all_zero")
    print(one_d_has_all_zero)

    # overriding method
    _ = cm + cm2
    assert _.info is None

    _ = cm + cm_noinfo
    assert _.info == "cm"

    _ = cm + prnt
    assert _.info == "cm"

    _ = cm * 2
    assert _.info == "cm"

    cm == 3
    cm.copy() == cm
    assert cm[0, 1] == 2
    assert cm.T[0, 1] == 4
    assert cm.T.info == "cm"

    # overriding method with right info
    assert (cm + cm2).info is None
    assert (cm + cm_noinfo).info == "cm"

    # new method
    cm.calculate()

    # new method with binary operator
    cm.calculate2(cm2)
    cm.calculate2(cm_noinfo)
    cm_noinfo.calculate2(prnt)

    # another new mthod with binary operator
    cm.calculate3(cm2)
