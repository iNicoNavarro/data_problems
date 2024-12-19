import sqlite3
import logging

logger = logging.getLogger()


def create_weather_data_fahrenheit_table(conn):

    try:
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS weather_data_fahrenheit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            localidad TEXT NOT NULL,
            pais TEXT NOT NULL,
            temperatura_fahrenheit REAL NOT NULL,
            fecha_y_hora DATE NOT NULL,
            cobertura_nubes TEXT,
            indice_uv REAL,
            presion_atmosferica REAL,
            velocidad_viento REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        logger.info("Table 'weather_data_fahrenheit' created successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error creating table 'weather_data_fahrenheit': {e}")


def populate_weather_data_fahrenheit(conn):

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO weather_data_fahrenheit (
            localidad, pais, temperatura_fahrenheit, fecha_y_hora, cobertura_nubes,
            indice_uv, presion_atmosferica, velocidad_viento
        )
        SELECT
            localidad,
            pais,
            temperatura * 1.8 + 32 AS temperatura_fahrenheit,
            DATE(fecha_y_hora) AS fecha,
            cobertura_nubes,
            indice_uv,
            presion_atmosferica,
            velocidad_viento
        FROM weather_data;
        """
        cursor.execute(query)
        conn.commit()
        logger.info("Data successfully populated into 'weather_data_fahrenheit'.")
    except sqlite3.Error as e:
        logger.error(f"Error populating 'weather_data_fahrenheit': {e}")


def add_temperature_delta_columns(conn):

    try:
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE weather_data ADD COLUMN delta_temperatura_horaria REAL;")
        cursor.execute("ALTER TABLE weather_data ADD COLUMN delta_temperatura_diaria REAL;")
        cursor.execute("ALTER TABLE weather_data_fahrenheit ADD COLUMN delta_temperatura_horaria REAL;")
        cursor.execute("ALTER TABLE weather_data_fahrenheit ADD COLUMN delta_temperatura_diaria REAL;")
        conn.commit()
        logger.info("Delta columns added successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error adding delta columns: {e}")


def calculate_temperature_deltas(connection):
    """
    Calculate temperature deltas and update the tables.
    """
    try:
        cursor = connection.cursor()

        # Calcular deltas horarios
        cursor.execute("""
        CREATE TEMP TABLE IF NOT EXISTS DeltaHourly AS
        SELECT 
            id, 
            temperatura - LAG(temperatura) OVER (
                PARTITION BY localidad ORDER BY fecha_y_hora
            ) AS delta_horaria
        FROM weather_data;
        """)

        cursor.execute("""
        UPDATE weather_data
        SET delta_temperatura_horaria = (
            SELECT delta_horaria
            FROM DeltaHourly
            WHERE DeltaHourly.id = weather_data.id
        );
        """)

        cursor.execute("""
        UPDATE weather_data_fahrenheit
        SET delta_temperatura_horaria = (
            SELECT delta_horaria
            FROM DeltaHourly
            WHERE DeltaHourly.id = weather_data_fahrenheit.id
        );
        """)

        # Calcular deltas diarios
        cursor.execute("""
        CREATE TEMP TABLE IF NOT EXISTS DeltaDaily AS
        SELECT 
            id, 
            temperatura - LAG(temperatura) OVER (
                PARTITION BY localidad ORDER BY DATE(fecha_y_hora)
            ) AS delta_diaria
        FROM weather_data;
        """)

        cursor.execute("""
        UPDATE weather_data
        SET delta_temperatura_diaria = (
            SELECT delta_diaria
            FROM DeltaDaily
            WHERE DeltaDaily.id = weather_data.id
        );
        """)

        cursor.execute("""
        UPDATE weather_data_fahrenheit
        SET delta_temperatura_diaria = (
            SELECT delta_diaria
            FROM DeltaDaily
            WHERE DeltaDaily.id = weather_data_fahrenheit.id
        );
        """)

        connection.commit()
        logger.info("Temperature deltas calculated and updated successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error calculating temperature deltas: {e}")
