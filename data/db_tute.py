"""
https://www.sqlitetutorial.net/wp-content/uploads/2018/03/chinook.zip
"""

from dwopt import db

d = db("sqlite:///chinook.db")


d.list_tables()


d.qry("albums").top()

col1 = "AlbumId"
col2 = "ArtistId"
group_by = (
    f"select {col1}, count(distinct {col2}) distinct_{col2} from albums group by {col1}"
)
d.qry(f"({group_by})").valc(f"distinct_{col2}")

d.qry("artists").top()
d.qry("customers").top()
d.qry("employees").top()
d.qry("genres").top()
d.qry("invoices").top()
d.qry("invoice_items").top()
d.qry("media_types").top()
d.qry("playlists").top()
d.qry("playlist_track").top()
d.qry("tracks").top()



class Tbl:

    def __init__(self, base=None):
        self._base = base
        self._nmes = list()
        self._cols = list()
        self._joins = list()
        self._withs = list()
        self._sql = ""

    def _make_sql(self):
        with_sql = ""
        for nme, block in zip(self._nmes, self._withs):
            if with_sql == "":
                with_sql = f"with {nme} as (\n{block}\n)"
            else:
                with_sql =  with_sql + f", {nme} as (\n{block}\n)"
        select_sql = ""
        base_sql = ""
        join_sql = ""


    def add_invoice_info(self, columns="n_items"):
        return self

    def add_customer_info(self, columns="name"):
        return self

(
    Tbl("invoices")
    .add_customer_info()
    .add_invoice_info()
)

