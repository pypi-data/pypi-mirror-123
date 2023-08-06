from jh_utils.data.pandas.sql import get_sql_table
from sqlalchemy import inspect

def get_top_rows(table, schema, engine, n=1):
    return get_sql_table(f'select * from {schema}.{table} dc limit {n}',engine)

def create_table_structure(pandas_df, table_name, engine, schema, index = False, if_exists = 'append'):
    pandas_df.to_sql(name = table_name,
                    con = engine, 
                    schema=schema, index=index, if_exists = if_exists)
    delete_table(table_name, schema, engine)

def get_schemas(engine):
    insp = inspect(engine)
    return insp.get_schema_names()

def create_schema(schema_name, engine):
    if not engine.dialect.has_schema(engine, schema_name):
        engine.execute(sa.schema.CreateSchema(schema_name))
    else:
        return 'Already exists'

def get_tables(schema, engine):
    insp = inspect(engine)
    return insp.get_table_names(schema)

def drop_table(table, schema, engine):
    conn = engine.connect()
    conn.execute(f'DROP TABLE IF EXISTS {schema}.{table};')
    conn.close()

def delete_table(table_name, schema, engine):
    conn = engine.connect()
    conn.execute(f'DELETE FROM {schema}.{table_name}')
    conn.close()

def drop_schema(schema, engine):
    conn = engine.connect()
    conn.execute(f'DROP SCHEMA {schema}')
    conn.close()