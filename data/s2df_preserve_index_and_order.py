import datetime
import functools

import pandas as pd

times = pd.Series(
    [
        datetime.datetime(year=2022, month=10, day=12),
        datetime.datetime(year=2022, month=10, day=1),
        datetime.datetime(year=2022, month=10, day=13),
    ]
)
times.index = [0, 3, 0]


def s2df_preserve_index_and_order():
    """
    Require func to have:

    - signature: output_df = func(input_series)
    - input and output first col same except for name.

    Examples
    ------------
    debug::

        input_series = times
    """

    def decorate(func):
        @functools.wraps(func)
        def new_func(input_series):
            input_series = input_series.copy()

            original_index = input_series.index

            input_series = input_series.reset_index(drop=True).sort_values()

            sorted_standard_index = input_series.index

            input_series = input_series.reset_index(drop=True)

            output_df = func(input_series)

            pd.testing.assert_series_equal(
                input_series, output_df.iloc[:, 0], check_names=False
            )

            output_df.index = sorted_standard_index
            output_df = output_df.sort_index()

            output_df.index = original_index

            return output_df

        return new_func

    return decorate


import duckdb


@s2df_preserve_index_and_order()
def left_join(s):
    df = pd.DataFrame(dict(col=s))
    res = duckdb.connect().execute("select * from df where 1=1 order by col").df()
    return res


if __name__ == "__main__":
    left_join(times)
