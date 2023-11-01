import pandas as pd
import psycopg2
from config import config

from models import Device


def to_excel(devices: list[Device]):
    columns = list(map(lambda x: x, Device.__annotations__))
    data = {column: [device.__getattribute__(column) for device in devices] for column in columns}
    df = pd.DataFrame(data)
    df.to_excel(config["excel_output_path"])


def __db_conn():
    return psycopg2.connect(
        database=config["database"],
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=int(config["port"])
    )


def clear_table():
    with __db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS public.phones (
                    id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
                    title text NOT NULL,
                    price text NOT NULL,
                    old_price text NULL,
                    discount text NULL,
                    count_lost text NULL,
                    rating text NULL,
                    count_rating text NULL,
                    cover text NOT NULL,
                    url text NOT NULL);
                """
            )
            cur.execute("TRUNCATE table public.phones")
            conn.commit()


def to_db(devices: list[Device]):
    with __db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS public.phones (
                    id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
                    title text NOT NULL,
                    price text NOT NULL,
                    old_price text NULL,
                    discount text NULL,
                    count_lost text NULL,
                    rating text NULL,
                    count_rating text NULL,
                    cover text NOT NULL,
                    url text NOT NULL);
                """
            )
            for device in devices:
                params = tuple(device.__getattribute__(i) for i in device.__annotations__)
                cur.execute(
                    "INSERT INTO phones "
                    "(title, price, old_price, discount, count_lost, rating, count_rating, cover, url) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    params
                )
            conn.commit()
