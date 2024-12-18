import os
import logging
import sqlite3
import pandas as pd


log_file_path = "../logs/punto_1.log"
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


def read_file(file_path):
    """
    Lee un archivo y devuelve una lista de líneas, manejando la codificación.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            logger.info(f"Archivo leído exitosamente con utf-8: {file_path}")
            return file.readlines()
    except UnicodeDecodeError:
        logger.warning(f"Error con utf-8. Intentando leer con latin-1: {file_path}")
        with open(file_path, "r", encoding="latin-1") as file:
            return file.readlines()
        

def parse_line(line, current_agent):
    """
    Parsea una línea para obtener datos si es un registro válido.
    Devuelve un diccionario con los valores procesados o None.
    """
    line = line.strip()
    if line.startswith("AGENTE:"):
        current_agent = line.split(":")[1].strip()
        logger.info(f"Agente encontrado: {current_agent}")
        return current_agent, None

    elif line and current_agent:
        parts = line.split(",")
        name = parts[0].strip()
        type_record = parts[1].strip()

        if type_record == "D":
            try:
                values = [float(v.strip()) for v in parts[2:]]
                return current_agent, {
                    "agent": current_agent,
                    "name": name,
                    "type": type_record,
                    "values": values
                }
            except ValueError:
                logger.error(f"Error al procesar valores en línea: {line}")
    return current_agent, None


def filter_and_process_data(file_path):
    """
    Lee el archivo, filtra y procesa los registros tipo 'D'.
    Devuelve una lista de diccionarios con los datos.
    """
    lines = read_file(file_path)
    data = []
    current_agent = None

    for line in lines:
        current_agent, record = parse_line(line, current_agent)
        if record:  
            data.append(record)
    logger.info(f"Total de registros procesados: {len(data)}")
    return data


def save_processed_data(data, output_path):
    """
    Convierte los datos procesados en un DataFrame y los guarda como CSV.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = pd.DataFrame(data)

    values_df = pd.DataFrame(
        df["values"].tolist(), 
        columns=[f"HORA_{i+1}" for i in range(24)]
    )
    df = pd.concat([df.drop(columns=["values"]), values_df], axis=1)

    df.to_parquet(output_path, index=False)
    logger.info(f"Datos procesados guardados en: {output_path}")


def load_parquet_data(input_path):
    """
    Carga un archivo Parquet y lo devuelve como un DataFrame.
    """
    if os.path.exists(input_path):
        logger.info(f"Leyendo datos desde el archivo Parquet: {input_path}")
        return pd.read_parquet(input_path)
    else:
        logger.error(f"El archivo no existe: {input_path}")
        return None
    

def prepare_for_sql(df):
    """
    Estructura los datos en un formato adecuado para la base de datos.
    Devuelve una lista de tuplas (o registros).
    """
    columns = ["agent", "name", "type"] + [f"HORA_{i+1}" for i in range(24)]
    logger.info(f"Estructurando datos para la base de datos con columnas: {columns}")
    
    records = [tuple(row) for row in df[columns].to_numpy()]
    return columns, records


def connect_to_db(db_path="database/ofertas.db"):
    """
    Crea una conexión a la base de datos SQLite.
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    logger.info(f"Conectado a la base de datos: {db_path}")
    return conn


def create_table(conn):
    """
    Crea la tabla `ofertas` en la base de datos.
    """
    cursor = conn.cursor()

    columns = ["agent TEXT", "name TEXT", "type TEXT"]
    columns += [f"HORA_{i+1} REAL" for i in range(24)]
    columns_str = ", ".join(columns)

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS ofertas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {columns_str}
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    logger.info("Tabla `ofertas` creada exitosamente.")


def insert_data(conn, records):
    """
    Inserta los registros en la tabla `ofertas`.
    """
    cursor = conn.cursor()

    placeholders = ", ".join(["?"] * len(records[0]))
    insert_query = f"INSERT INTO ofertas ({', '.join(['agent', 'name', 'type'] + [f'HORA_{i+1}' for i in range(24)])}) VALUES ({placeholders})"

    cursor.executemany(insert_query, records)
    conn.commit()
    logger.info(f"{len(records)} registros insertados en la tabla `ofertas`.")


def export_table_to_csv(conn, output_path="processed_data/ofertas_table.csv"):
    """
    Exporta la tabla `ofertas` a un archivo CSV.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    query = "SELECT * FROM ofertas"
    df = pd.read_sql_query(query, conn)
    df.to_csv(output_path, index=False)
    logger.info(f"Tabla exportada a CSV: {output_path}")