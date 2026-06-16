# Promaga basado en reglas
# Autor: Gerardo Figueroa
# Fecha: 08/06/26
import streamlit as st
import pandas as pd
import os
import operator

def seleccion_archivos():
    # 1. Seleccion de archivo
    # Buscamos todos los archivos .xlsx en la carpeta actual
    #archivo_seleccionado = "reglas_paking.xlsx"
    archivos_xlsx = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    
    if not archivos_xlsx:
        st.error("No se encontraron archivos Excel (.xlsx) en la carpeta actual.")
        return None  # Devolvemos None explícitamente si no hay archivos
    
    # Si hay archivos, mostramos el selector
    archivo_seleccionado = st.selectbox("Selecciona el archivo que deseas analizar:", archivos_xlsx)
    try:
        df = pd.read_excel(archivo_seleccionado, sheet_name="Sheet1")
        df_reglas = pd.read_excel(archivo_seleccionado, sheet_name="Reglas")
        return df, df_reglas, archivo_seleccionado
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return None
    
# ***************** manejo data frame ************************
def corre_reglas(df,df_reglas):
    # 2. Diccionario de operadores
    operadores = {
        "==": operator.eq,
        "!=": operator.ne,
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">=": operator.ge
    }

    # 3. Inicializar listas para acumular resultados
    coinciden = []
    no_coinciden = []

    # 4. Recorrer todas las reglas
    for _, fila in df_reglas.iterrows():
        col = fila["Columna"]
        signo = fila["Signo"]
        regla = fila["Regla"]

        if col in df.columns and signo in operadores:
            dtype = df[col].dtype

            # --- Manejo de fechas ---
            if pd.api.types.is_datetime64_any_dtype(dtype):
                try:
                    regla_convertida = pd.to_datetime(regla, errors="coerce")
                except Exception:
                    regla_convertida = None

                # Si no es fecha válida, probamos si es número de días
                if regla_convertida is pd.NaT or regla_convertida is None:
                    try:
                        dias = int(regla)
                        # Base: hoy (puedes cambiar a otra columna como Fecha_Emision)
                        regla_convertida = pd.Timestamp.today() + pd.Timedelta(days=dias)
                    except ValueError:
                        regla_convertida = None

            # --- Manejo de números ---
            elif pd.api.types.is_numeric_dtype(dtype):
                try:
                    regla_convertida = float(regla)
                except ValueError:
                    regla_convertida = None

            # --- Manejo de texto ---
            else:
                regla_convertida = regla

            # 5. Aplicar la condición si la regla es válida
            if regla_convertida is not None:
                condicion = operadores[signo](df[col], regla_convertida)

                df_ok = df[condicion].copy()
                df_fail = df[~condicion].copy()

                # Agregar columna para trazabilidad de la regla aplicada
                df_ok["Regla_Aplicada"] = f"{col} {signo} {regla}"
                df_fail["Regla_Aplicada"] = f"{col} {signo} {regla}"

                coinciden.append(df_ok)
                no_coinciden.append(df_fail)

    # 6. Concatenar resultados finales
    df_coincide = pd.concat(coinciden, ignore_index=True) if coinciden else pd.DataFrame()
    df_no_coincide = pd.concat(no_coinciden, ignore_index=True) if no_coinciden else pd.DataFrame()

    # Filtrar df para que queden en df_no_coincide correctos
    df_no_coincide = df[~df['ID'].isin(df_coincide['ID'])]
    # Al entrar en una regla en df_coincide y la duplica. Borras los duplicados
    df_coincide.drop_duplicates(subset=['ID'], inplace=True)
    
    return df_coincide, df_no_coincide
    
 
# *************Deficion pagina principal******************
st.set_page_config(layout="wide")
col1, col2 = st.columns([1, 2])  # proporción: más espacio para el título
with col1:
    st.image("images/img_planta.png", width=150)
with col2:
    st.header("Sistema Basado en Reglas (Rule-based Systems)")
    st.write("⚡Programa estrella para la toma de decisiones que literalmente ***Ahorra tiempo de Trabajo***")

# Explicacion del programa
with st.expander("Explicación del Programa"):
    st.write("""
            Clintes y proveedores externos es comun recibir información que no pertenece a tu sistema (ERP). Al recibirlos, el agente debe procesarlo
            y analizarlo ya sea para elaborar un pedido/paking list procesando 'solo la información' que se ajuste al requerimiento de la empresa.
            A esto denominamos (Rule-based Systems), al incorporar Reglas se puede procesar la información discriminando los datos que esten fuera de la regla
            a traves de formulas que analizan cada regla con cada reglon del archivo, logrando que el operador agilice su trabajo.
            Toda la información es posible exportarlo, borrarlos o guardarlos para su clarificación o metricas. 
            Se muestran 3 tablas o data frames:
            """)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Archivo Entrada (input):** Recibe la información original externa del cliente/proveedor.")
    with col2:
        st.write("**Datos Rechazados (output):** Muestra la información Rechazada, que no coincidio con las reglas del archivo de entrada.")
    with col3:
        st.write("**Datos Validos (output):** Muestra información Valida, que coincidio con las reglas del archivo de entrada.")

#df, df_reglas, archivo_seleccionado = seleccion_archivos()
#selecciona archivos
resultado = seleccion_archivos()
if resultado is not None:
    df, df_reglas, archivo_seleccionado = resultado
    #corre las reglas
    df_coincide, df_no_coincide = corre_reglas(df,df_reglas) 
    # muestra datos
    col1, col2 = st.columns(2)
    with col1:
        st.write("⚙️ Reglas")
        with st.expander(f"Ver vista previa de 'archivo de reglas'"):
                st.write(df_reglas)
    with col2:        
        st.write("Archivo de entrada (input)")
        with st.expander(f"Ver vista previa de {archivo_seleccionado}"):
            st.write(df)
    st.write("❌ Información Rechazada")
    with st.expander(f"Ver vista previa datos rechazados (output)", expanded=False):
        st.write(df_no_coincide)
    st.write("✅ Información Valida")
    with st.expander(f"Ver vista previa datos concidentes (output)", expanded=True):
        st.write(df_coincide)
    #st.markdown("---")
else:
    # Mensaje de espera o instrucciones si aún no se ha cargado nada
    st.info("Por favor, asegúrate de tener archivos válidos en la carpeta.")
#******************* fin programa ppal ***************************

# ******************Definicion panel lateral*************
   
# *****************fin lateral ***********************

