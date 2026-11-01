# %%
import os

import pandas as pd
import sqlalchemy as sa


# add run method to engine
def run(self: sa.engine.Engine, sql:str, ops_error_lines:int = 2) -> pd.DataFrame | None:
    with self.begin() as conn:
        try: 
            res = conn.execute(sa.text(sql))
        except sa.exc.OperationalError as e:
            useful_lines = str(e).split('\n')[0:ops_error_lines]
            cln_lines = []
            for line in useful_lines:
                cln_line = '\n'.join(line[i:i+80] for i in range(0, len(line), 80))
                cln_lines.append(cln_line)
            report = '\n'.join(cln_lines)
            raise Exception(f"SQL execution failed:\n{report}") from None
        
        if res.returns_rows:
            return pd.DataFrame(res.all(), columns=res.keys())

sa.engine.Engine.run = run

connection_string = f"teradatasql://{os.environ['TERADATA_USER']}:{os.environ['TERADATA_PASSWORD']}@{os.environ['TERADATA_HOST']}"
eng = sa.create_engine(connection_string)
eng.run(f"select * from dbc.dbcinfo where infokey = 'Version'")
# %%

# Teradata query for table constraints and indexes
qry = f"""
SELECT 
    d.DatabaseName as table_schema,
    t.TableName as table_name,
    i.ColumnName as column_name,
    i.IndexName as constraint_name,
    CASE 
        WHEN i.UniqueFlag = 'Y' THEN 'UNIQUE'
        WHEN i.IndexType = 'P' THEN 'PRIMARY KEY'
        WHEN i.IndexType = 'S' THEN 'SECONDARY INDEX'
        WHEN i.IndexType = 'J' THEN 'JOIN INDEX'
        ELSE 'INDEX'
    END as constraint_type,
    i.IndexType,
    i.UniqueFlag,
    i.ColumnPosition
FROM DBC.IndicesV i
JOIN DBC.TablesV t ON i.DatabaseName = t.DatabaseName AND i.TableName = t.TableName
JOIN DBC.DatabasesV d ON i.DatabaseName = d.DatabaseName
WHERE i.DatabaseName = 'your_database_name'
    AND i.TableName = 'your_table_name'
    AND t.TableKind = 'T'  -- Only tables, not views
ORDER BY i.IndexName, i.ColumnPosition;
"""

df = eng.run(qry)
df