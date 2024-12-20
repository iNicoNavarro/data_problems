### **Propósito de la Arquitectura**

El diseño está orientado a:

1. Procesar grandes volúmenes de datos de ventas.
2. Gestionar datos históricos y en tiempo real para generar insights accionables.
3. Implementar un modelo analítico robusto que integre gobernanza de datos, predicciones en tiempo real, y reportes avanzados para prevenir desabastecimiento en puntos de venta.

---

### **Descripción por Componentes**

#### **1. Data Source (Fuente de Datos)**

* **Rol:** Es el origen de los datos que pueden provenir de:
  * **Sistemas de ventas transaccionales** para datos históricos.
  * **Dispositivos IoT o puntos de venta** para datos en tiempo real.
* **Flujo:** Los datos son enviados al sistema a través de:
  * **Azure Event Hubs** para ingesta en tiempo real (streaming).
  * **Azure Data Factory** para extracción y carga periódica de datos históricos (batch).

---

#### **2. Data Lake**

El Data Lake sigue el modelo de capas  **Bronze, Silver, y Golden** , una práctica común para organizar los datos según su nivel de transformación.

1. **Bronze Data (Datos en Crudo):**
   * **Rol:** Almacena datos en crudo, tanto de streaming como de batch.
   * **Fuente:** Datos ingresados desde Event Hubs y Data Factory.
   * **Servicios de Azure:**
     * **Azure Data Lake Storage Gen2** : Para almacenamiento eficiente.
     * **Azure Stream Analytics** : Procesa y clasifica datos en tiempo real para almacenamiento.
2. **Silver Data (Datos Transformados):**
   * **Rol:** Almacena datos limpios y estructurados después de transformaciones iniciales.
   * **Fuente:** Datos procesados por **Azure Databricks** y  **Azure Stream Analytics** .
   * **Servicios de Azure:**
     * **Azure Data Lake Storage Gen2** : Continúa almacenando los datos en esta capa.
     * **Azure Databricks** : Realiza transformaciones, limpieza y cálculos básicos.
3. **Golden Data (Datos Refinados):**
   * **Rol:** Datos listos para análisis avanzado, dashboards y machine learning.
   * **Servicios de Azure:**
     * **Azure Synapse Analytics** : Actúa como Data Warehouse para consultas analíticas complejas.

---

#### **3. Metadata**

* **Rol:** Proporciona gobernanza y un catálogo centralizado para facilitar el entendimiento y rastreo de datos.
* **Componentes principales:**
  * **Data Catalog:** Lista todos los activos de datos con su linaje.
  * **Data Dictionary:** Documenta definiciones y estándares de cada campo.
  * **Business Glossary:** Explica los términos del negocio.
* **Servicio de Azure:**  **Azure Purview** .

---

#### **4. Ingesta de Datos**

* **Ingesta en Streaming:**
  * **Azure Event Hubs** recibe datos en tiempo real de los puntos de venta.
  * **Azure Stream Analytics** transforma los datos en tiempo real y los almacena en la capa **Bronze** del Data Lake.
* **Ingesta Batch:**
  * **Azure Data Factory** orquesta la extracción y carga periódica de datos históricos al Data Lake.

---

#### **5. Data Mars / Feature Storage**

* **Rol:** Almacena características (features) derivadas para modelos de machine learning.
* **Servicio de Azure:**
  * **Azure Machine Learning** gestiona datasets reutilizables para proyectos de predicción.

---

#### **6. Analítica Avanzada**

1. **Minería de Datos:**
   * Realiza análisis de datos históricos y detecta patrones.
   * **Servicio de Azure:**  **Azure Databricks** .
2. **Machine Learning y Predicciones:**
   * Entrena e implementa modelos predictivos.
   * Los modelos son utilizados para detectar anomalías y prever desabastecimiento.
   * **Servicio de Azure:**
     * **Azure Machine Learning** para entrenar y gestionar modelos.
     * **Azure Functions** para ejecutar modelos en tiempo real.

---

#### **7. Reportes, OLAP, Dashboards**

* **Rol:** Genera dashboards y reportes para usuarios finales.
* **Servicios de Azure:**
  * **Power BI:** Para visualización avanzada conectada a Synapse.
  * **Azure Synapse Analytics:** Para análisis OLAP y reportes basados en datos refinados.

---

#### **8. Gobernanza de Datos**

* **Rol:** Asegurar que los datos sean confiables, seguros y estén alineados con las políticas empresariales.
* **Componentes:**
  * Políticas, principios y metas: Definidos en  **Azure Purview** .
  * Acceso seguro: Gestionado con  **Azure Active Directory (AAD)** .

---

#### **9. Capacidad de Gestión**

* **Componentes:**
  * **Certificaciones de datos, enmascaramiento y protección:** Gestionados con **Azure Key Vault** y  **Azure Policy** .
  * **Backups:** Proporcionados por **Azure Backup** para recuperación de desastres.

---

#### **10. DevOps**

* **Rol:** Orquestar la implementación continua de pipelines y modelos.
* **Servicios de Azure:**
  * **Azure DevOps** o **GitHub Actions** para integración y despliegue continuo (CI/CD).

---

### **Flujo de Datos Resumido**

1. **Ingesta:**
   * Streaming: Event Hubs → Stream Analytics → Data Lake (Bronze).
   * Batch: Data Factory → Data Lake (Bronze).
2. **Transformación:**
   * Databricks procesa los datos en la capa Silver del Data Lake.
   * Synapse almacena datos refinados (Golden) para análisis OLAP.
3. **Análisis:**
   * Databricks y Machine Learning generan modelos.
   * Synapse y Power BI entregan reportes y dashboards.
4. **Retroalimentación:**
   * Modelos entrenados en Databricks son usados en Stream Analytics para detección en tiempo real.

---

### **Conclusión**

Este diseño asegura:

* **Escalabilidad:** Usando Data Lake y Synapse para manejar grandes volúmenes de datos.
* **Flexibilidad:** Integrando batch y streaming en un mismo flujo.
* **Acción en Tiempo Real:** Detección de patrones con Stream Analytics y Azure ML.
* **Gobernanza:** Garantizando control y rastreo de datos con Azure Purview.
