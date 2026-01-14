from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

def get_postgres_engine(pg_url: str):
    engine = create_engine(pg_url, echo=False, future=True)
    return engine

def load_orders_postgres(engine):
    # Імпорт orders.sql у PostgreSQL (одноразово (або перезапис), якщо таблиця ще не існує)
    try:
         engine.execute(open("orders.sql", "r").read())
    except Exception as e:
        print(f"Error executing orders.sql: {e}")

    query = '''
            SELECT *
            FROM orders;
            -- LIMIT 5;
            '''
    df = pd.read_sql(query, con=engine)
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['order_amount'] = pd.to_numeric(df['order_amount'], errors='coerce')
    return df

