
# Documentación del Proceso de Cálculo y Actualización de Datos Meteorológicos

## Introducción

Este documento describe el flujo de trabajo implementado para el procesamiento de datos meteorológicos, incluyendo la creación de tablas, inserción de datos ficticios, cálculo de deltas de temperatura (horaria y diaria) y exportación de datos. Se incluyen detalles sobre las tablas involucradas (`weather_data` y `weather_data_fahrenheit`) y las transformaciones realizadas.

---

## Estructura del Proyecto

El proyecto está organizado en tres archivos principales:

1. **`main.py`:** Contiene el flujo principal que orquesta el proceso.
2. **`core.py`:** Define funciones fundamentales como la conexión a la base de datos, creación de tablas, y generación de datos ficticios.
3. **`weather_data_transformations.py`:** Contiene funciones relacionadas con transformaciones de datos, como la creación de tablas en Fahrenheit y el cálculo de deltas de temperatura.

---

## Detalle del Proceso

### **1. Conexión y Creación de Tablas**

#### Archivo: `core.py`

* **Conexión a la Base de Datos**:
  La función `connect_to_db` establece la conexión a una base de datos SQLite ubicada en `../database/weather_data.db`.
* **Creación de la Tabla** `weather_data`:
  La tabla almacena datos meteorológicos en grados Celsius y se crea mediante la función `<span>create_weather_table</span>`.
  **Estructura de la Tabla:**
  * `id`: Clave primaria.
  * `localidad,` `pais`: Información geográfica.
  * `temperatura`: Temperatura en grados Celsius.
  * `fecha_y_hora`: Marca temporal.
  * Otros campos incluyen `cobertura_nubes`, `indice_uv`, `presion_atmosferica` y `velocidad_viento`.

### **2. Generación de Datos Ficticios**

#### Archivo: `core.py`

* La función `insert_dummy_data_with_faker` genera datos aleatorios utilizando la biblioteca Faker.
* Se simulan datos para diferentes localidades con condiciones meteorológicas variadas.

### 3. Creación y Población de `weather_data_fahrenheit`

#### Archivo: `weather_data_transformations.py`

* **Creación de la Tabla**:
  La función `create_weather_data_fahrenheit_table` define una tabla que almacena los mismos datos que `weather_data`, pero convierte la temperatura a grados Fahrenheit.
  **Conversión de Temperatura**: Fahrenheit = Celsius * 1.8 + 32
* **Población de la Tabla**:
  La función `populate_weather_data_fahrenheit` transfiere datos desde `weather_data`, aplicando la conversión.

### **4. Adición de Columnas para Deltas de Temperatura**

#### Archivo: `weather_data_transformations.py`

* La función `add_temperature_delta_columns` añade las siguientes columnas a ambas tablas:
  * `delta_temperatura_horaria`: Diferencia entre temperaturas en registros horarios consecutivos.
  * `delta_temperatura_diaria`: Diferencia entre temperaturas en registros diarios consecutivos.

### **5. Cálculo de Deltas de Temperatura**

#### Archivo: `weather_data_transformations.py`

* La función `calculate_temperature_deltas` realiza los cálculos:
  * Utiliza tablas temporales con el calculo de los deltas.
  * Actualiza ambas tablas (`weather_data` y `weather_data_fahrenheit`) con los resultados.

---

## Exportación de Datos

#### Archivo: `main.py`

* **Exportación de Tablas**:
  Las tablas `weather_data` y `weather_data_fahrenheit` se exportan a archivos CSV en la carpeta `../database_data/`
* **Exportación de Esquemas**:
  Se exportan los esquemas de las tablas en formato CSV, utilizando la instrucción `PRAGMA table_info`.

---

## Ejecución del Flujo Principal

#### Archivo: `main.py`

El flujo principal realiza las siguientes acciones:

1. Conecta a la base de datos.
2. Crea y llena las tablas `weather_data` y `weather_data_fahrenheit`.
3. Agrega y calcula las columnas de delta de temperatura.
4. Exporta los datos y esquemas de las tablas.

**Comando de Ejecución:**

```
python main.py
```

---

## Estructura Final de Tablas

### `weather_data`

| Campo                     | Tipo    | Descripción                                    |
| ------------------------- | ------- | ----------------------------------------------- |
| id                        | INTEGER | Clave primaria.                                 |
| localidad                 | TEXT    | Localidad de la observación.                   |
| pais                      | TEXT    | País de la localidad (por defecto "Colombia"). |
| temperatura               | REAL    | Temperatura en grados Celsius.                  |
| delta_temperatura_horaria | REAL    | Diferencia de temperatura horaria.              |
| delta_temperatura_diaria  | REAL    | Diferencia de temperatura diaria.               |

### `weather_data_fahrenheit`

| Campo                     | Tipo    | Descripción                       |
| ------------------------- | ------- | ---------------------------------- |
| id                        | INTEGER | Clave primaria.                    |
| localidad                 | TEXT    | Localidad de la observación.      |
| pais                      | TEXT    | País de la localidad.             |
| temperatura_fahrenheit    | REAL    | Temperatura en grados Fahrenheit.  |
| delta_temperatura_horaria | REAL    | Diferencia de temperatura horaria. |
| delta_temperatura_diaria  | REAL    | Diferencia de temperatura diaria.  |

---

## Log de Proceso

Los logs se almacenan en `../logs/punto_3.log` y documentan cada etapa del flujo, incluyendo errores.

---

## Conclusión

El proceso implementado garantiza que ambas tablas contengan datos completos, con cálculos precisos de deltas de temperatura, y que los resultados sean exportados para su análisis posterior.
