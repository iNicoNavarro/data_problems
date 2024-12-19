import sqlite3
import os
import logging
import random

from datetime import datetime, timedelta
from faker import Faker

logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), '../logs/punto_3.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def connect_to_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        logging.info(f"Connected to database at {db_path}")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        return None


def create_weather_table(conn):
    try:
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            localidad TEXT NOT NULL,
            pais TEXT NOT NULL DEFAULT 'Colombia',
            temperatura REAL NOT NULL,
            fecha_y_hora DATETIME NOT NULL,
            cobertura_nubes TEXT CHECK(cobertura_nubes IN ('Mínima', 'Parcial', 'Total')),
            indice_uv REAL,
            presion_atmosferica REAL,
            velocidad_viento REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        logging.info("Table 'weather_data' created successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error creating table: {e}")


def determine_cobertura_nubes(temperatura, velocidad_viento):
    if temperatura > 28 and velocidad_viento < 5:
        return 'Mínima'
    elif 20 <= temperatura <= 28 and 5 <= velocidad_viento <= 10:
        return 'Parcial'
    else:
        return 'Total'


def insert_dummy_data_with_faker(conn, num_records=100):
    try:
        fake = Faker("es_CO") 
        cursor = conn.cursor()
        localidades = [
            'El Poblado', 
            'Laureles', 
            'Belen', 
            'Robledo', 
            'Castilla', 
            'Buenos Aires', 
            'Aranjuez'
        ]

        start_date = datetime(2024, 1, 1)
        dummy_data = []
        locality_date_map = {locality: start_date for locality in localidades}

        for i in range(num_records):
            localidad = random.choice(localidades)
            temperatura = round(random.uniform(15.0, 35.0), 1)
            velocidad_viento = round(random.uniform(0.0, 15.0), 1)
            cobertura_nubes = determine_cobertura_nubes(temperatura, velocidad_viento)
            fecha_y_hora = locality_date_map[localidad]
            locality_date_map[localidad] += timedelta(days=1)

            dummy_data.append((
                random.choice(localidades), #fake.city(),
                "Colombia",
                temperatura,
                fecha_y_hora.strftime("%Y-%m-%d %H:%M:%S"),
                cobertura_nubes,
                round(random.uniform(0.0, 11.0), 1),
                round(random.uniform(1000.0, 1025.0), 1),
                velocidad_viento
            ))

        insert_query = """
        INSERT INTO weather_data (
            localidad, pais, temperatura, fecha_y_hora, cobertura_nubes,
            indice_uv, presion_atmosferica, velocidad_viento
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor.executemany(insert_query, dummy_data)
        conn.commit()
        logging.info(f"{num_records} dummy records inserted successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error inserting dummy data: {e}")


def close_connection(conn):
    try:
        conn.close()
        logging.info("Database connection closed.")
    except sqlite3.Error as e:
        logging.error(f"Error closing the database connection: {e}")
