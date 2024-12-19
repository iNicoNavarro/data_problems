# main.py
import os
import logging
from core import (
    load_master_data,
    filter_master_data,
    load_ddec_data,
    merge_datasets,
    calculate_horizontal_sum,
    save_results
)


def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler("../logs/punto_2.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

def main():
    logger = configure_logging()
    try:
        logger.info("Inicio del proceso.")

        raw_data_path = "../raw_data"
        processed_data_path = "../processed_data"

        master_data_file = os.path.join(raw_data_path, "Datos Maestros VF.xlsx")
        ddec_file = os.path.join(raw_data_path, "dDEC1204.txt")
        output_file = os.path.join(processed_data_path, "filtered_results.csv")

        master_data = load_master_data(
            file_path=master_data_file
        )
        # print(master_data)
        # print(master_data.columns)

        filtered_master_data = filter_master_data(
            master_data=master_data
        )
        # print(filtered_master_data)
        ddec_data = load_ddec_data(
            file_path=ddec_file
        )
        # print(ddec_data)
        merged_data = merge_datasets(
            master_data=filtered_master_data, 
            ddec_data=ddec_data
        )
        # print(merged_data)

        result_data = calculate_horizontal_sum(
            data=merged_data
        )

        # print(result_data)

        save_results(
            data=result_data, 
            output_file=output_file
        )

        logger.info(f"Proceso completado. Archivo generado en: {output_file}")

    except Exception as e:
        logger.error(f"Error en el proceso: {e}")


if __name__ == "__main__":
    main()
