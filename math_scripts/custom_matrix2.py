import custom_matrix2_support
import numpy as np
import openpyxl
import pandas as pd
from custom_matrix import CustomMatrix


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
        res = custom_matrix2_support.calculate2(self, other)
        return self.__class__(res.matrix, info=self.info)

    def calculate3(self, other):
        if not isinstance(other, CustomMatrix):
            raise TypeError(
                f"cannot calculate3 with a {type(other)} object. "
                "Try converting it to a CustomMatrix first."
            )
        res = custom_matrix2_support.calculate3(self, other)
        return self.__class__(res.matrix, info=self.info)

    def to_excel_with_color_scale(self) -> openpyxl.Workbook:
        df = self.to_dataframe()
        wb = custom_matrix2_support.to_excel_with_color_scale(df)
        return wb


def calculate(matrix):
    res = matrix**2
    return res


if __name__ == "__main__":
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

    # to excel
    wb = cm.to_excel_with_color_scale()
    wb.save("test.xlsx")
