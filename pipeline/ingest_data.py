import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine
import click

@click.command()
@click.option('--pg-user', envvar='POSTGRES_USER', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', envvar='POSTGRES_PASSWORD', default='password', help='PostgreSQL password')
@click.option('--pg-host', envvar='POSTGRES_HOST', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', envvar='POSTGRES_PORT', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', envvar='POSTGRES_DB', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'

    df = pd.read_csv(prefix + 'yellow_tripdata_2021-01.csv.gz', nrows=100)

    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }

    parse_dates = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"
    ]

    engine = create_engine(
                f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
            )

    df_iter= pd.read_csv(
        prefix + 'yellow_tripdata_2021-01.csv.gz',
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000
    )


    print(df_iter)
    print(next(df_iter))


    first = True

    for df_chunk in tqdm(df_iter):

        if first:
            # Create table schema (no data)
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists="replace"
            )
            first = False
            print("Table created")

        # Insert chunk
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )

        print("Inserted:", len(df_chunk))
        



if __name__ == "__main__":
    run()


