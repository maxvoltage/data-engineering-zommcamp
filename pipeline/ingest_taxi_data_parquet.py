import pyarrow.parquet as pq
import pyarrow as pa
from sqlalchemy import create_engine
import click
import fsspec

@click.command()
@click.option('--color', default='green', help='Taxi color (yellow, green, fhv)')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=11, type=int, help='Month of the data')
@click.option('--url-template', 
              default='https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-{month_str}.parquet',
              help='Template for the URL')
@click.option('--pg-user', envvar='POSTGRES_USER', default='postgres')
@click.option('--pg-pass', envvar='POSTGRES_PASSWORD', default='password')
@click.option('--pg-host', envvar='POSTGRES_HOST', default='localhost')
@click.option('--pg-port', envvar='POSTGRES_PORT', default=5432)
@click.option('--pg-db', envvar='POSTGRES_DB', default='ny_taxi')
def run(color, year, month, url_template, pg_user, pg_pass, pg_host, pg_port, pg_db):
    
    # 1. Construct URL and Table Name
    month_str = str(month).zfill(2)
    url = url_template.format(
        color=color, 
        year=year, 
        month_str=month_str
    )
    
    target_table = f"{color}_taxi_parquet_{year}_{month_str}"
    
    print(f"--- Ingestion Process Started (Pure PyArrow) ---")
    print(f"URL: {url}")
    print(f"Target Table: {target_table}")
    
    # 2. Setup Database Connection
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    # 3. Read Parquet from URL using PyArrow
    try:
        print("Opening remote Parquet file via fsspec...")
        # Since pyarrow doesn't natively speak 'https', we use fsspec
        with fsspec.open(url) as f:
            print("Reading Parquet table into memory...")
            table = pq.read_table(f)
            
            # Convert to Pandas for SQL insertion (standard practice even in PyArrow pipelines)
            # as SQLAlchemy + Pandas is the most stable way to load pg
            df = table.to_pandas()
            
            print(f"Inserting {len(df)} rows into Postgres...")
            # We don't rename columns as requested
            df.to_sql(name=target_table, con=engine, if_exists="replace", index=False)
            
        print(f"Successfully ingested data into {target_table}!")

    except Exception as e:
        print(f"Error during ingestion: {e}")
        exit(1)

if __name__ == "__main__":
    run()
