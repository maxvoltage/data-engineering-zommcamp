import pandas as pd
from sqlalchemy import create_engine
import click
import os

@click.command()
@click.option('--pg-user', envvar='POSTGRES_USER', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', envvar='POSTGRES_PASSWORD', default='password', help='PostgreSQL password')
@click.option('--pg-host', envvar='POSTGRES_HOST', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', envvar='POSTGRES_PORT', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', envvar='POSTGRES_DB', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='zones', help='Target table name')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/'
    url = prefix + 'taxi_zone_lookup.csv'

    print(f"Downloading data from {url}...")
    
    # Read the CSV file directly from the URL
    # This file is small (~265 rows), so no need for chunking
    df = pd.read_csv(url)

    # Create the connection engine
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    print(f"Connecting to database {pg_db} at {pg_host}:{pg_port}...")
    
    # Insert data into the database
    # "replace" ensures that if we run it twice, we don't duplicate rows
    print(f"Inserting data into table '{target_table}'...")
    df.to_sql(name=target_table, con=engine, if_exists='replace', index=False)

    print("Success! Data ingested.")

if __name__ == "__main__":
    run()
