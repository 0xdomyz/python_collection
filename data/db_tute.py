
class Tbl:
    """
    """

    def __init__(self, base=None):
        self._base = base
        self._nmes = list()
        self._cols = list()
        self._joins = list()
        self._withs = list()
        self._aliases = list()
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

    def run():
        # 1 make uuid temp
        #   check
        #   delete original
        #   make original again
        # 2 make new one with specified name
        pass

    def add_info(self, keys: list(str), cols, nme_maps: dict(str,str)):
        # 1 sql, fields, joins
        # 2 sql, fields, joins, withs
        pass


if __name__ == "__main__":

    run_exploration = False

    if run_exploration:
        from dwopt import db
        #data from `here <https://www.sqlitetutorial.net/wp-content/uploads/2018/03/chinook.zip>`_
        d = db("sqlite:///data/chinook.db")
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
    else:
        t = Tbl("invoices")
        t.add_info()
        print(t.sql)
        # select
        #     x.id,
        #     z.col
        # from tbl1 x
        # join part1 y
        # on x.id = y.id
        # join part2 z
        # on y.id2 = z.id

        t.add_with_info()
        print(t.sql)
        # with part1 as (
        #     select
        #         a.id,
        #         sum(b.col) col
        #     from tbl1 a
        #     join tbl2 b
        #     on a.id = b.id
        #     group by a.id
        # )
        # select
        #     x.id,
        #     y.col
        # from tbl1 x
        # join part1 y
        # on x.id = y.id




