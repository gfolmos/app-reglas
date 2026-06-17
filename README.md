Autor: Gerardo Figueroa
Fecha: 08/06/26
⚡ Rule-Based Data Validator (Rule-Based Systems)

> **Programa estrella para la toma de decisiones que optimiza y agiliza los flujos de trabajo operativos.**

Al recibir información externa de clientes o proveedores en formatos heterogéneos que no pertenecen nativamente a tu ERP, los agentes suelen consumir horas valiosas procesando y filtrando registros manualmente. 

Este sistema automatiza la discriminación de datos basándose en reglas de negocio predefinidas en archivos de Excel (como órdenes de compra o packing lists). El motor valida cada celda dinámicamente y separa la información apta de la que se encuentra fuera de rango, permitiendo guardar, exportar o analizar métricas de forma inmediata.

## 📌 Características Principales

* **⚡ Motor Dinámico de Reglas:** Soporta operadores lógicos estándar (`==`, `!=`, `<`, `<=`, `>`, `>=`).
* **📅 Inferencia Inteligente de Tipos:** Manejo avanzado y automático para:
    * **Fechas:** Comparación absoluta o basada en diferencias de días relativos respecto a la fecha actual (`Timestamp.today()`).
    * **Numéricos:** Conversión segura a punto flotante (`float`) para evitar desbordamientos o malas interpretaciones.
    * **Texto:** Comparaciones textuales estricta y segura.
* **🔍 Trazabilidad de Auditoría:** Inyecta automáticamente la columna `Regla_Aplicada` en los datos procesados para conocer exactamente qué condición afectó a cada registro.
* **🛡️ Integridad de Datos:** Eliminación interna de registros duplicados por ID y aislamiento estricto de rechazos mediante exclusión lógica con Pandas.
* **💻 UI/UX Intuitiva:** Interfaz modular construida en Streamlit con paneles colapsables (`st.expander`) y distribución asimétrica en formato panorámico (`wide`).

## 🏗️ Estructura del Proyecto

La arquitectura del repositorio mantiene una organización limpia y minimalista, facilitando su despliegue inmediato:

```text
📁 tu-repositorio/
│
├── 📁 images/
│   └── img_planta.png          # Recursos visuales e identidad de la UI.
│
├── 📄 app.py                   # Script principal y motor lógico de Streamlit.
├── 📊 reglas_orden_compra.xlsx # Plantilla de datos y reglas de Órdenes de Compra.
├── 📊 reglas_paking.xlsx       # Plantilla de datos y reglas de Packing List.
└── 📄 requirements.txt         # Lista de dependencias del proyecto.
Nota sobre los archivos Excel (.xlsx): Para que el sistema funcione correctamente, cada archivo debe contener al menos dos pestañas obligatorias:

Sheet1: Matriz de datos de entrada que contiene la columna obligatoria ID.

Reglas: Tabla de configuración con las columnas explicitadas: Columna, Signo y Regla.

⚙️ Arquitectura del Procesamiento de Datos
El flujo lógico de la aplicación sigue una arquitectura secuencial dividida en tres etapas claras:

[ Archivo de Entrada (.xlsx) ] 
       │
       ▼
 ┌───────────┐       🔍 Evaluador de Tipos (Numérico / Fecha / String)
 │  app.py   │ ───►  ⚙️ Aplicación de Operadores Relacionales (`operator`)
 └───────────┘       🛡️ Eliminación de Duplicados e Identificación por ID
       │
       ├─► ❌ [ Datos Rechazados (Output) ] -> No cumplen las reglas del negocio.
       └─► ✅ [ Datos Válidos (Output) ]    -> Listos para ingresar al ERP.
🚀 Requisitos Previos e Instalación
Sigue estos pasos para clonar el repositorio y configurar un entorno de ejecución local aislado.

1. Clonar el repositorio
Bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
cd tu-repositorio
2. Crear y activar un entorno virtual
Se recomienda el uso de virtualenv o venv para mitigar conflictos entre versiones de librerías de Python.

💻 Ejecución de la Aplicación
Para iniciar el servidor local de Streamlit y lanzar la interfaz en tu navegador web predeterminado, ejecuta el siguiente comando en la raíz del proyecto:

Bash
streamlit run app.py
Por defecto, la aplicación se desplegará en la dirección local: http://localhost:8501

💡 Guía de Uso Rápido
Colocación de datos: Asegúrate de que tus archivos .xlsx de reglas estén ubicados directamente en la raíz del proyecto.

Selección: Utiliza el menú desplegable en la barra superior para alternar entre reglas_orden_compra.xlsx y reglas_paking.xlsx.

Auditoría: Expande la sección "Información Válida" o "Información Rechazada" para previsualizar los resultados en tiempo real y analizar la columna de trazabilidad.

🛠️ Tecnologías Utilizadas
Lenguaje: Python 3.9+

Framework de UI: Streamlit - Para el renderizado rápido de interfaces web de datos.

Procesamiento de Datos: Pandas - Para la manipulación, alineación y filtrado eficiente de dataframes.

Librería Core: operator - Mapeo nativo de funciones estándar para operadores lógicos en Python.

📄 Licencia
Este proyecto se encuentra bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.
