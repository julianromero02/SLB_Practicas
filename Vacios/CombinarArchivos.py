
import pandas as pd
import glob

ruta_archivos = 'C:/Users/Julian/OneDrive/Escritorio/SLB/Vacios/unir/*.xlsx'

# Obtener la lista de archivos que coinciden con el patrón
archivos = glob.glob(ruta_archivos)

# Leer el primer archivo para identificar las columnas con datos
primer_archivo = archivos[0]
primer_df = pd.read_excel(primer_archivo)
columnas_datos = primer_df.columns[primer_df.any()]

# Leer los archivos y combinarlos en un DataFrame
dataframes = []
for archivo in archivos:
    try:
        # Leer solo las columnas con datos
        df = pd.read_excel(archivo, usecols=columnas_datos)
        dataframes.append(df)
    except Exception as e:
        print(f"Error al leer el archivo {archivo}: {str(e)}")

# Combinar los DataFrames en uno solo
combined_df = pd.concat(dataframes)
# Eliminar filas duplicadas
combined_df = combined_df.drop_duplicates()
combined_df=combined_df.sort_values('CONSECUTIVO')
# Guardar el DataFrame combinado en un archivo excel
combined_df.to_excel('C:/Users/Julian/OneDrive/Escritorio/SLB/Vacios/Vacios.xlsx', index=False)
