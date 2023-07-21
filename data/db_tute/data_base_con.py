import pandas as pd
import sqlalchemy as alc


# add run method to engine
def run(self, sql):
    with self.begin() as conn:
        res = conn.execute(alc.text(sql))
        if res.returns_rows:
            return pd.DataFrame(res.all(), columns=res.keys())


alc.engine.Engine.run = run

# url

url_base = "dwopt_test:1234@localhost:1521/?service_name=XEPDB1 &encoding=UTF-8&nencoding=UTF-8"

# use just oracle
url = f"oracle://{url_base}"
eng = alc.create_engine(url, echo=True)

eng.dialect.name
eng.dialect.driver

eng.run("select * from dual")


# oracledb
url = f"oracle+oracledb://{url_base}"
bin_path = r"C:\app\User\product\21c\dbhomeXE\bin"
eng = alc.create_engine(url, echo=True, thick_mode = {"lib_dir": bin_path})

eng.dialect.driver

eng.run("select * from dual")



