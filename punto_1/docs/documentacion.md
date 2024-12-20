# Documentación del Punto 1: Procesamiento y Carga de Datos de Ofertas Iniciales

## Descripción General

El objetivo del Punto 1 fue procesar datos provenientes de un archivo de texto («OFEI1204.txt»), estructurarlos, almacenarlos en un formato eficiente (Parquet) y cargarlos en una base de datos SQLite para su posterior consulta y análisis. El flujo se desarrolló siguiendo buenas prácticas de ingeniería de software, incluyendo modularización, manejo de logs, y separación de responsabilidades.

---

## Estructura del Repositorio

```
project/
|-- punto_1/
    |-- database/
    |   |-- ofertas.db  # Base de datos SQLite
    |
    |-- docs/  # Documentación
    |
    |-- logs/
    |   |-- punto_1.log  # Logs del proceso
    |
    |-- processed_data/
    |   |-- punto_1_data.parquet  # Archivo Parquet
    |   |-- punto_1_data.csv  # Exportación a CSV
    |
    |-- raw_data/
    |   |-- OFEI1204.txt  # Archivo fuente
    |
    |-- sources/
        |-- core.py  # Lógica del procesamiento y conexión a SQLite
        |-- main.py  # Script principal
```

---

## Flujo de Trabajo

### 1. Lectura y Filtrado del Archivo de Texto

El archivo de texto («OFEI1204.txt») contiene información de ofertas iniciales organizadas por agentes. Se realizó un proceso de filtrado para extraer únicamente los registros del tipo `D`, que representan los datos relevantes.

**Pasos:**

* Leer el archivo utilizando codificaciones `utf-8` o `latin-1` en caso de error.
* Identificar las líneas que contienen el prefijo `AGENTE` para registrar el agente actual.
* Extraer y transformar las líneas relevantes en un diccionario estructurado.

### 2. Guardado en Formato Parquet

Los datos procesados se transformaron en un DataFrame de Pandas y se guardaron en formato Parquet. Esto asegura un almacenamiento compacto y eficiente para futuras operaciones.

### 3. Carga en SQLite

Los datos procesados se cargaron en una base de datos SQLite bajo la tabla `ofertas` El esquema incluye columnas que representan las 24 horas del día para almacenar los valores de las ofertas horarias.

**Pasos:**

1. Conectar a la base de datos SQLite.
2. Crear la tabla `ofertas` con las columnas necesarias.
3. Insertar los registros procesados.

### 4. Exportación a CSV

La tabla `ofertas` se exportó a un archivo CSV para facilitar su revisión y entrega.

---

## Archivos Principales

### **main.py**

El script principal orquesta todo el flujo de trabajo:

1. Llama a las funciones modulares para procesar, guardar y cargar los datos.
2. Maneja errores y genera logs.

### **core.py**

Contiene las funciones modulares:

* **Lectura y filtrado:** Lectura del archivo, identificación de agentes y procesamiento de registros tipo `D`.
* **Persistencia:** Guardado en formato Parquet y carga en SQLite.
* **Exportación:** Generación de CSV a partir de la tabla SQL.

---

## Tabla `ofertas`

### Esquema

| Campo   | Tipo | Descripción                         |
| ------- | ---- | ------------------------------------ |
| id      | INT  | Identificador único (autoincrement) |
| agent   | TEXT | Nombre del agente                    |
| name    | TEXT | Nombre de la oferta                  |
| type    | TEXT | Tipo de registro (solo `D`)        |
| HORA_1  | REAL | Valor de la primera hora             |
| ...     | ...  | ...                                  |
| HORA_24 | REAL | Valor de la última hora             |

---

## Manejo de Logs

El sistema utiliza `logging` para registrar eventos importantes durante la ejecución. Los logs se guardan en `../logs/punto_1.log` y contienen detalles sobre:

* Inicio y fin del proceso.
* Lectura de archivos y detección de agentes.
* Errores y advertencias.
* Información sobre la inserción de registros y la exportación de datos.

Ejemplo de log:

```
2024-12-20 10:00:00 - INFO - Archivo leído exitosamente con utf-8: ../raw_data/OFEI1204.txt
2024-12-20 10:05:00 - INFO - Total de registros procesados: 250
2024-12-20 10:10:00 - INFO - Tabla `ofertas` creada exitosamente.
2024-12-20 10:15:00 - INFO - 250 registros insertados en la tabla `ofertas`.
```

---

## Resultados

* **Archivo Parquet:**`../processed_data/punto_1_data.parquet`
* **Archivo CSV:**`../processed_data/punto_1_data.csv`
* **Base de datos SQLite:**`../database/ofertas.db`
* **Logs:**`../logs/punto_1.log`

---

## Conexión a la Base de Datos

Para conectarse a la base de datos desde otro entorno:

1. Asegúrate de que el archivo `ofertas.db` esté accesible.
2. Usa cualquier herramienta compatible con SQLite.
3. Ejemplo de conexión con Python:

```
import sqlite3

conn = sqlite3.connect("../database/ofertas.db")
query = "SELECT * FROM ofertas"

cursor = conn.cursor()
for row in cursor.execute(query):
    print(row)

conn.close()
```

---

## Conclusión

El proceso del Punto 1 estableció una base sólida para el manejo de datos: desde la ingesta y procesamiento inicial, hasta el almacenamiento estructurado y su disponibilidad para consultas SQL. Esta solución modular permite escalar y adaptarse fácilmente a nuevos requerimientos.
