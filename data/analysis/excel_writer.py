from pathlib import Path
import openpyxl
import pandas as pd
from loguru import logger
from contextlib import contextmanager

VERSION = "2025.08.02.16"


class ExcelWriter(object):
    def __init__(
        self,
        file_path: Path,
        sheet_name: str = "Sheet",
        cur_row: int = 1,
        cur_col: int = 1,
        distance_bw_tables: int = 2,
        mode: str = None,
    ):
        self.file_path = file_path
        self.mode = mode
        self.sheet_name = sheet_name
        self.start_row = 1
        self.start_col = 1
        self.cur_row = cur_row
        self.cur_col = cur_col
        self.distance_bw_tables = distance_bw_tables

        if not self.file_path.exists():
            if self.mode and self.mode == "a":
                raise ValueError(
                    f"File {self.file_path} does not exist, cannot open in append mode."
                )
            self.mode = "w"

    def __repr__(self):
        return (
            f"ExcelWriter(file_path='{self.file_path}', sheet_name={self.sheet_name}),"
            f" cur_row={self.cur_row}, cur_col={self.cur_col}, distance_bw_tables={self.distance_bw_tables})"
        )

    # @contextmanager
    # def open(self, mode: str = "a"):
    #     self.__enter__(mode)
    #     try:
    #         yield self
    #     finally:
    #         self.__exit__(None, None, None)

    # def close(self):
    #     if hasattr(self, "writer"):
    #         self.writer.close()
    #     else:
    #         logger.warning("ExcelWriter was not opened, nothing to close.")

    def __enter__(self):
        logger.debug(f"Opening ExcelWriter in {self.mode} mode for {self.file_path}")
        self.writer = pd.ExcelWriter(
            self.file_path,
            engine="openpyxl",
            mode=self.mode,
            if_sheet_exists="overlay" if self.mode == "a" else None,
        )
        self.switch_to_existing_or_new_sheet(self.sheet_name)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logger.debug("Exiting ExcelWriter context manager")
        self.writer.close()

    def switch_to_existing_or_new_sheet(self, sheet_name: str):
        logger.debug(f"Switching to sheet: {sheet_name}")
        if sheet_name not in self.writer.book.sheetnames:
            self.writer.book.create_sheet(sheet_name)
        self.ws = self.writer.sheets[sheet_name]
        self.sheet_name = sheet_name
        self.cur_row = self.start_row
        return self

    def write_df(self, df: pd.DataFrame, title: str = None, index=True):
        logger.debug(
            f"Writing {title} on {self.sheet_name} at R{self.cur_row}, C{self.cur_col}"
        )

        self.ws.cell(
            row=self.cur_row, column=self.cur_col, value=title if title else ""
        )
        self.cur_row += 1

        df.to_excel(
            self.writer,
            sheet_name=self.sheet_name,
            index=index,
            startrow=self.cur_row - 1,
            startcol=self.cur_col - 1,
        )

        self.cur_row += df.shape[0] + self.distance_bw_tables
        return self
