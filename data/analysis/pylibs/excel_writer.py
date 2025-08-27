import functools
from pathlib import Path
import openpyxl
import pandas as pd
from loguru import logger
import io
from openpyxl.drawing.image import Image as XLImage

logger.remove()

VERSION = "2025.08.27.00"


def ref_from_rc(row, col):
    return openpyxl.utils.get_column_letter(col) + str(row)


def _supply_temp_context_if_called_outside_cm(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        self: ExcelWriter = args[0]

        # enter temp context if not run within a context manager
        if self.writer is None or self.writer._status != "open":
            # logger.debug("ExcelWriter is not open, opening it now for this method.")
            self.__enter__(mode=("a" if self._has_added_items else None))
            try:
                res = func(*args, **kwargs)
            finally:
                self.__exit__(None, None, None)
        else:
            res = func(*args, **kwargs)

        return res

    return new_func


def _pre_and_post_proc_for_item_addition(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        self: ExcelWriter = args[0]

        # move cursor
        _valid_locations = ["down", "right", None]
        if "location" not in kwargs or kwargs["location"] is None:
            if not self._cursor_ready_to_write:
                self.move_cursor(down=True)
        elif kwargs["location"] not in _valid_locations:
            raise ValueError(
                f"Invalid location {kwargs['location']}. Must be one of {_valid_locations}."
            )
        elif kwargs["location"] == "down":
            self.move_cursor(down=True)
        elif kwargs["location"] == "right":
            self.move_cursor(right=True)
        else:
            raise Exception("Program logic error - this should not happen.")

        # log and run
        logger.debug(
            f"Writing item on {self.sheet_name} at R{self.cur_row}, C{self.cur_col}"
        )

        res = func(*args, **kwargs)

        # set status flags
        self._has_added_items = True
        self._cursor_ready_to_write = False

        return res

    return new_func


class ExcelWriter(object):
    def __init__(
        self,
        file_path: Path,
        mode: str = "w",
        sheet_name: str = "Sheet",
        cur_row: int = 1,
        cur_col: int = 1,
        distance_bw_contents: int = 2,
    ):
        self.file_path = file_path
        self.writer = None
        self.mode = mode

        # custom attributes
        self.sheet_name = sheet_name
        self.cur_row = cur_row
        self.cur_col = cur_col
        self.distance_bw_contents = distance_bw_contents

        # hardcoded attributes
        self.start_row = 1
        self.start_col = 1
        self.rows_per_inch = 5  # 6inch, 30 rows
        self.cols_per_inch = 1.6  # 12inch, 19 cols

        self._content_set_sizes = []  # a set is a row of contents
        self._cursor_ready_to_write = True
        self._has_added_items = False

    def __repr__(self):
        return (
            f"ExcelWriter("
            f"file_path='{self.file_path}',"
            f"mode = {self.mode},"
            f"sheet_name={self.sheet_name}),"
            f"cur_row={self.cur_row},"
            f"cur_col={self.cur_col},"
            f"distance_bw_contents={self.distance_bw_contents},"
            f")"
        )

    def __enter__(self, mode: str = None):
        """
        ways to enter:
        1. obj as context manager
        2. manually first entry
        3. manually subsequent entries

        mode in cases:
        1. can be w or a
        2. can be w or a
        3. must be a

        reset_cursor in cases:
        1. either
        2. False
        3. False
        """
        mode = mode or self.mode

        if not self.file_path.exists():
            mode = "w"
            logger.debug(f"File {self.file_path} does not exist, force mode w.")

        logger.debug(f"Enter ExcelWriter: {mode = }")
        self.writer = pd.ExcelWriter(
            self.file_path,
            engine="openpyxl",
            mode=mode,
            if_sheet_exists="overlay" if mode == "a" else None,
        )
        self.writer._status = "open"  # inplant
        self.switch_to_sheet(
            self.sheet_name, create_if_not_exists=True, reset_cursor=False
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logger.debug("Exit ExcelWriter")
        self.writer.close()
        self.writer._status = "closed"

    def _make_new_sheet(self, sheet_name: str):
        logger.debug(f"Creating new sheet: {sheet_name}")
        assert (
            sheet_name not in self.writer.book.sheetnames
        ), f"Sheet {sheet_name} already exists in the workbook."
        self.ws = self.writer.book.create_sheet(sheet_name)
        return self

    @_supply_temp_context_if_called_outside_cm
    def switch_to_sheet(
        self,
        sheet_name: str,
        create_if_not_exists: bool = False,
        reset_cursor: bool = True,
    ):
        if create_if_not_exists and sheet_name not in self.writer.book.sheetnames:
            # logger.debug(f"Sheet {sheet_name} does not exist, creating it.")
            self._make_new_sheet(sheet_name)

        logger.debug(f"Switching to sheet: {sheet_name}")
        assert (
            sheet_name in self.writer.book.sheetnames
        ), f"Sheet {sheet_name} does not exist in the workbook."
        self.ws = self.writer.sheets[sheet_name]
        self.sheet_name = sheet_name
        if reset_cursor:
            self.move_cursor(reset=True)
        return self

    def move_cursor(
        self,
        reset: bool = False,
        down: bool = False,
        right: bool = False,
        row: int = None,
        col: int = None,
    ):
        if reset:
            self.cur_row = self.start_row
            self.cur_col = self.start_col
            self._content_set_sizes = []  # reset if move to a new sheet
        elif down and right:
            raise ValueError("Cannot move cursor down and right at the same time.")
        elif down:
            if self._content_set_sizes:
                max_height = max(size[0] for size in self._content_set_sizes)
                self.cur_row += max_height + self.distance_bw_contents
                self.cur_col = self.start_col
                self._content_set_sizes = []  # reset after moving down
        elif right:
            if self._content_set_sizes:
                last_width = self._content_set_sizes[-1][1]
                self.cur_col += last_width + self.distance_bw_contents
        elif row is not None or col is not None:
            self.cur_row += row if row is not None else 0
            self.cur_col += col if col is not None else 0
        else:
            raise ValueError("Must specify one of the movements.")

        self._cursor_ready_to_write = True
        return self

    @_pre_and_post_proc_for_item_addition
    @_supply_temp_context_if_called_outside_cm
    def write_df(
        self,
        df: pd.DataFrame,
        title: str = None,
        index=True,
        location: str = None,
        **kwargs,
    ):
        if isinstance(df, pd.DataFrame):
            df_height, df_width = df.shape
        elif isinstance(df, type(pd.DataFrame().style)):
            df_height, df_width = df.data.shape
        else:
            raise ValueError("df must be a DataFrame or Styler")

        self.ws.cell(
            row=self.cur_row, column=self.cur_col, value=title if title else ""
        )
        df.to_excel(
            self.writer,
            sheet_name=self.sheet_name,
            index=index,
            startrow=self.cur_row + 1 - 1,  # 1 for title, -1 for 0-based index
            startcol=self.cur_col,  # table starts at + 1 more col from startcol
            **kwargs,
        )

        self._content_set_sizes.append((df_height + 1, df_width + index + 1))
        return self

    @_pre_and_post_proc_for_item_addition
    @_supply_temp_context_if_called_outside_cm
    def write_fig(self, fig, title: str = None, location: str = None, **kwargs):
        def fig_to_img(fig):
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            img = XLImage(buf)
            return img

        fig_height = int(fig.get_size_inches()[1] * self.rows_per_inch)
        fig_width = int(fig.get_size_inches()[0] * self.cols_per_inch)

        self.ws.cell(
            row=self.cur_row, column=self.cur_col, value=title if title else ""
        )
        self.ws.add_image(
            fig_to_img(fig),
            ref_from_rc(self.cur_row + 1, self.cur_col + 1),  # 1 col just for titles
        )
        self._content_set_sizes.append((fig_height + 1, fig_width + 1))
        return self

    @_supply_temp_context_if_called_outside_cm
    def auto_fit_column_width(self, max_width: int = 150):
        for column in self.ws.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
                if max_length > max_width:
                    max_length = max_width
                    break
            adjusted_width = max_length + 2
            self.ws.column_dimensions[column[0].column_letter].width = adjusted_width
        return self
