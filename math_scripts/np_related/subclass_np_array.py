# subclass numpy.ndarray
# have additional attributes: datetime
############################

import datetime
from typing import Any

import numpy as np
from scipy.stats import norm


class MyArray(np.ndarray):
    def __new__(cls, input_array: np.ndarray, datetime: datetime.datetime = None):
        obj = np.asarray(input_array).view(cls)
        obj.datetime = datetime
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.datetime = getattr(obj, "datetime", None)

    def __array_ufunc__(
        self,
        ufunc: np.ufunc,
        method,
        *inputs: Any,
        **kwargs: Any,
    ) -> Any:
        args = []
        for i, input_ in enumerate(inputs):
            if isinstance(input_, MyArray):
                args.append(input_.view(np.ndarray))
            else:
                args.append(input_)

        results = super().__array_ufunc__(ufunc, method, *args, **kwargs)
        if results is NotImplemented:
            return NotImplemented

        if method == "at":
            if isinstance(inputs[0], MyArray):
                inputs[0].datetime = self.datetime
            return

        if ufunc.nout == 1:
            results = (results,)

        results = tuple(np.asarray(result).view(MyArray) for result in results)
        if results and isinstance(results[0], MyArray):
            results[0].datetime = self.datetime

        return results[0] if len(results) == 1 else results

    def __repr__(self) -> str:
        return super().__repr__() + f"\ndatetime={self.datetime}"

    def __str__(self) -> str:
        return super().__str__() + f"\ndatetime={self.datetime}"

    def calc(self):
        res = norm.cdf(self)
        return self.__class__(res, datetime=self.datetime)


mat = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) * 0.1
mat

MyArray(mat)
ma = MyArray(mat, datetime=datetime.datetime.now())
ma

ma[:-1]

ma.calc()

ma + ma

ma * 2

ma[0, 0]

ma + mat
