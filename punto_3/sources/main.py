import os
import logging
import pandas as pd
from core import (
    connect_to_db, 
    create_weather_table, 
    insert_dummy_data_with_faker, 
    close_connection
)
from weather_data_transformations import (
    create_weather_data_fahrenheit_table,
    populate_weather_data_fahrenheit,
    add_temperature_delta_columns,
    calculate_temperature_deltas
)

logger = logging.getLogger()


def export_table_to_csv(connection, table_name, export_path):

    try:
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, connection)
        df.to_csv(export_path, index=False)
        logging.info(f"Table '{table_name}' exported to {export_path} successfully.")
    except Exception as e:
        logging.error(f"Failed to export table '{table_name}': {e}")


def export_table_schema(connection, table_name, export_path):

    try:
        query = f"PRAGMA table_info({table_name});"
        df = pd.read_sql_query(query, connection)
        df.to_csv(export_path, index=False)
        logging.info(f"Schema of table '{table_name}' exported to {export_path} successfully.")
    except Exception as e:
        logging.error(f"Failed to export schema for table '{table_name}': {e}")


def main():

    db_path = os.path.join(os.path.dirname(__file__), "../database/weather_data.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    export_dir = os.path.join(os.path.dirname(__file__), "../database_data")
    os.makedirs(export_dir, exist_ok=True)
    connection = connect_to_db(db_path)
    num_records = 200  

    if connection:
        try:
            create_weather_table(connection)
            insert_dummy_data_with_faker(connection, num_records)

            create_weather_data_fahrenheit_table(connection)
            populate_weather_data_fahrenheit(connection)

            add_temperature_delta_columns(connection)
            calculate_temperature_deltas(connection)

            export_table_to_csv(
                connection=connection, 
                table_name="weather_data", 
                export_path=os.path.join(export_dir, "weather_data.csv")
            )
            export_table_schema(
                connection=connection, 
                table_name="weather_data", 
                export_path=os.path.join(export_dir, "weather_data_schema.csv")
            )
            export_table_to_csv(
                connection=connection, 
                table_name="weather_data_fahrenheit", 
                export_path=os.path.join(export_dir, "weather_data_fahrenheit.csv")
            )
            export_table_schema(
                connection=connection, 
                table_name="weather_data_fahrenheit", 
                export_path=os.path.join(export_dir, "weather_data_fahrenheit_schema.csv")
            )
            logging.info("Process completed successfully.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        finally:
            close_connection(connection)


if __name__ == "__main__":
    main()
