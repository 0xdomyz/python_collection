
class Tbl:

    def __init__(self, base: str):
        self._base = base#future: allow a base query
        self._join_clause = list()
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

    def add_info(self, keys: list(str), cols, nme_maps: dict(str,str)):
        # 1 sql, fields, joins
        # 2 sql, fields, joins, withs
        pass

    def run():
        # 1 make uuid temp
        #   check
        #   delete original
        #   make original again
        # 2 make new one with specified name
        pass


eg_simple = """
select
    x.trackid,
    x.albumid,
    x.genreid,
    y.title album_title,
    z.name genre_name
from tracks x
left join albums y
on x.albumid = y.albumid
left join genres z
on x.genreid = z.genreid
"""


eg_with = """
with part1 as (
    select
        a.albumid,
        count(distinct b.trackid) n_tracks
    from albums a
    join tracks b
    on a.albumid = b.albumid
    group by a.albumid
)
select
    x.albumid,
    y.n_tracks
from albums x
join part1 y
on x.albumid = y.albumid
"""

"""
simple template

select
    {base fields}
    {fields 1}
    {fields 2}
from {base} {alias base}
{join_clause 1} {alias 1}
{join_clause 2} {alias 2}
"""

{
    "join_clause": """

left join albums {a}
on {base}.albumid = {a}.albumid

    """,
    "alias": "y",
    "fields": """
{a}.title album_title
    """
}

def bind(sql, data):
    new_sql = None
    return new_sql

bind("select {a} from dual", {"a":"x"})


if __name__ == "__main__":

    run_exploration = False

    if run_exploration:
        from dwopt import db
        #data from `here <https://www.sqlitetutorial.net/wp-content/uploads/2018/03/chinook.zip>`_
        #diagram `<https://www.sqlitetutorial.net/sqlite-sample-database/>`_
        d = db("sqlite:///data/chinook.db")
        d.list_tables()
        d.qry("albums").top()

        col1 = "AlbumId"
        col2 = "ArtistId"
        # col1 = "ArtistId"
        # col2 = "AlbumId"
        group_by = (
            f"select {col1}, count(distinct {col2}) distinct_{col2} from albums group by {col1}"
        )
        d.qry(f"({group_by})").valc(f"distinct_{col2}")

        d.qry("albums").top()
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

        q = d.qry(f"({eg_simple})")
        q.len()
        q.head()
        d.qry("tracks").len()

        q = d.qry(f"({eg_with})")
        q.len()
        q.head()
        d.qry("albums").len()


    else:
        t = Tbl("invoices")
        t.add_info()
        print(t.sql)
        t.add_with_info()
        print(t.sql)




