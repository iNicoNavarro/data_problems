import pandas as pd
import logging
import unicodedata


logger = logging.getLogger()

RENAME_MAP: str = {
    'nombre_visible_agente': 'nombre_visible_agente',
    'agente_ofei': 'agente_ofei',
    'nombre_visible_central': 'nombre_visible_central',
    'central_ddec_dsegdes_dpru': 'central',
    'central_ofei': 'central_ofei',
    'unidad_ofei': 'unidad_ofei',
    'cen_capacidad_efectiva_neta_o_potencia_maxima': 'cen_capacidad_efectiva_neta_o_potencia_maxima',
    'tipo_de_central_hidro_termo_filo_menor': 'tipo_de_central_hidro_termo_filo_menor',
    'precio_de_arranque_par': 'precio_arranque',
    'minimo_tecnico_por_central': 'minimo_tecnico_central',
    'minimo_tenico__por_unidad': 'minimo_tecnico_unidad',
    'inflexibilidad_por_unidad_para_generar_agc_qa': 'inflexibilidad_por_unidad_para_generar_agc_qa',
    'minimo_operativo_por_central_mo_del_ofei': 'minimo_operativo_por_central_mo_del_ofei'
}


def remove_accents(text):
    if isinstance(text, str):
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
    return text


def load_master_data(file_path: str):
    try:
        logger.info("Cargando datos maestros desde el archivo Excel.")
        master_data = pd.read_excel(file_path)
        master_data.columns = (
            master_data.columns.str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace(r'[^\w]', '', regex=True)
            .map(remove_accents)
        )
        return master_data.rename(columns=RENAME_MAP)
    except Exception as e:
        logger.error(f"Error cargando el archivo maestro: {e}")
        raise


def filter_master_data(master_data: pd.DataFrame):
    try:
        logger.info("Filtrando datos maestros para agentes específicos y tipos de central.")

        master_data['nombre_visible_agente'] = master_data['nombre_visible_agente'].fillna('DESCONOCIDO')
        master_data['tipo_de_central_hidro_termo_filo_menor'] = master_data['tipo_de_central_hidro_termo_filo_menor'].fillna('')

        return master_data[
            (master_data['nombre_visible_agente'].str.contains("EMGESA", na=False)) &
            (master_data['tipo_de_central_hidro_termo_filo_menor'].isin(['H', 'T']))
        ]
    except KeyError as e:
        logger.error(f"Error en las columnas del archivo maestro: {e}")
        raise


def load_ddec_data(file_path: str):
    try:
        logging.info("Cargando datos del archivo dDEC1204.TXT.")
        ddec_data = pd.read_csv(
            file_path, 
            delimiter=',', 
            header=None,
            encoding="latin1"
        )
        ddec_data.columns = ["central"] + [f"hora_{i}" for i in range(1, 25)]
        return ddec_data
    except Exception as e:
        logging.error(f"Error cargando el archivo dDEC: {e}")
        raise


def merge_datasets(master_data: pd.DataFrame, ddec_data: pd.DataFrame):
    try:
        logging.info("Realizando merge entre datos maestros y dDEC.")
        return pd.merge(master_data, ddec_data, on='central', how='inner')
    except KeyError as e:
        logging.error(f"Error al hacer merge: {e}")
        raise


def calculate_horizontal_sum(data: pd.DataFrame):
    try:
        logging.info("Calculando suma horizontal de las columnas de horas.")
        hour_columns = [col for col in data.columns if col.startswith('hora_')]
        data['suma_horizontal'] = data[hour_columns].sum(axis=1)
        return data[data['suma_horizontal'] > 0]
    except Exception as e:
        logging.error(f"Error calculando la suma horizontal: {e}")
        raise


def save_results(data: pd.DataFrame, output_file: str):
    try:
        logging.info(f"Guardando resultados filtrados en {output_file}.")
        data.to_csv(output_file, index=False)
    except Exception as e:
        logging.error(f"Error guardando los resultados: {e}")
        raise
