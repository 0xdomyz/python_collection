# sqlalchemy, connect to oracle db via url

import sqlalchemy as alc
import pandas as pd


# add run method to engine
def run(self, sql):
    with self.begin() as conn:
        res = conn.execute(alc.text(sql))
        if res.returns_rows:
            return pd.DataFrame(res.all(), columns=res.keys())


alc.engine.Engine.run = run


url = "oracle://dwopt_test:1234@localhost:1521/?service_name=XEPDB1 &encoding=UTF-8&nencoding=UTF-8"
