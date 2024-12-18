import os
import logging
from core import (
    filter_and_process_data,
    save_processed_data,
    export_table_to_csv,
    load_parquet_data,
    prepare_for_sql,
    connect_to_db,
    create_table,
    insert_data,
)

logger = logging.getLogger()


def main():
    """
    Función principal para orquestar el procesamiento y carga de datos.
    """
    file_path = "../raw_data/OFEI1204.txt"
    processed_path = "../processed_data/punto_1_data.parquet"
    db_path = "../database/ofertas.db"
    export_path = "../processed_data/ofertas_table.csv"

    logger.info("Inicio del procesamiento del archivo...")
    try:
        data = filter_and_process_data(
            file_path=file_path
        )
        if data:
            save_processed_data(
                data=data, 
                output_path=processed_path
            )
        
        df = load_parquet_data(
            input_path=processed_path
        )

        if df is not None:
            columns, records = prepare_for_sql(df)
            conn = connect_to_db(db_path)
            create_table(conn)
            insert_data(conn, records)

            export_table_to_csv(conn, export_path)
            logger.info(f"Datos estructurados para la base de datos. Total registros: {len(records)}")
        else:
            logger.warning("No se encontraron datos para procesar en la base de datos.")

    except Exception as e:
        logger.error(f"Error durante el procesamiento: {str(e)}")


if __name__ == "__main__":
    main()