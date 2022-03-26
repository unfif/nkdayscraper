# %%%
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.future import select
# from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import TEXT
import settings
from pprint import pprint

engine = create_engine(settings.DATABASE_URL, echo=False, future=True)
inspector = inspect(engine)
tables = inspector.get_table_names()

# %%
# for table in tables:
#     with Session(engine, future=True) as session:
#         columns = inspector.get_columns(table)
#         for column in columns:
#             if isinstance(column['type'], TEXT):
#                 query = f"select * from {table} where {column['name']} = ' ' "
#                 records = session.execute(text(query))
#                 for record in records:
#                     pprint(dict(record))

with engine.connect() as conn:
    for table in tables:
        query = select('*').select_from(text(table))
        columns = inspector.get_columns(table)
        for column in columns:
            if isinstance(column['type'], TEXT) and column['name'] not in ['courseinfo2']:
                records = conn.execute(
                    query.filter(text(f"{column['name']} = '' "))
                )
                for record in records:
                    pprint(dict(record))

print('done.')
# %%
