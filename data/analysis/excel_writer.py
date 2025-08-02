from pathlib import Path
import openpyxl
import pandas as pd
from loguru import logger


class ExcelWriter(object):
    def __init__(
        self,
        file_path: Path,
        load=False,
        sheet_name: str = "Sheet",
        cur_row: int = 1,
        cur_col: int = 1,
        distance_bw_tables: int = 2,
    ):
        self.file_path = file_path
        self.load = load
        self.start_row = 1
        self.start_col = 1
        self.cur_row = cur_row
        self.cur_col = cur_col
        self.distance_bw_tables = distance_bw_tables

        if not load:
            self.wb = openpyxl.Workbook()
            self.ws = self.wb.active
            self.sheet_name = self.ws.title
            self._save()
        else:
            self.wb = openpyxl.load_workbook(self.file_path)
            self.ws = self.wb[sheet_name]
            self.sheet_name = sheet_name

    def __repr__(self):
        return (
            f"ExcelWriter(file_path='{self.file_path}', load={self.load},"
            f"sheet_name={self.sheet_name}), cur_row={self.cur_row}, cur_col={self.cur_col},"
            f" distance_bw_tables={self.distance_bw_tables})"
        )

    def _load(self):
        self.wb = openpyxl.load_workbook(self.file_path)

    def _save(self):
        if not self.file_path.parent.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.wb.save(self.file_path)
        return self

    def add_and_switch_to_sheet(self, sheet_name: str):
        self._load()
        assert (
            sheet_name not in self.wb.sheetnames
        ), f"Sheet '{sheet_name}' already exists."
        self.wb.create_sheet(sheet_name)
        self._switch_to_sheet(sheet_name)
        self._save()
        return self

    def _switch_to_sheet(self, sheet_name: str):
        self.sheet_name = sheet_name
        self.cur_row = self.start_row
        self.ws = self.wb[sheet_name]

    def write_df(self, df: pd.DataFrame, title: str = None, index=True):
        self._load()
        logger.debug(f"{self.cur_row=}, {self.cur_col=}")

        with pd.ExcelWriter(
            self.file_path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
        ) as writer:
            writer.sheets[self.sheet_name].cell(
                row=self.cur_row, column=self.cur_col, value=title if title else ""
            )
            self.cur_row += 1
            df.to_excel(
                writer,
                sheet_name=self.sheet_name,
                index=index,
                startrow=self.cur_row - 1,
                startcol=self.cur_col - 1,
            )
        self.cur_row += df.shape[0] + self.distance_bw_tables
        return self
