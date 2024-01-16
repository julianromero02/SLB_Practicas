
import pandas as pd
import os
# Ruta del directorio donde se encuentran los archivos Excel
directorio = "C:/Users/Julian/OneDrive/Escritorio/SLB/Livianos"

# Crear un archivo Excel nuevo para almacenar las hojas


# Lista para almacenar los DataFrames de las hojas
dataframes = []

# Obtener la lista de archivos Excel en el directorio
archivos_excel = [archivo for archivo in os.listdir(directorio) if archivo.endswith('limpio.xlsx')]

# Leer cada archivo Excel y su primera hoja en un DataFrame y agregarlo a la lista
for archivo in archivos_excel:
    ruta_archivo = os.path.join(directorio, archivo)
    df = pd.read_excel(ruta_archivo, sheet_name=0)  # Cambiar 0 por el índice de la hoja si es diferente
    dataframes.append(df)

# Concatenar todos los DataFrames en uno solo
df_final = pd.concat(dataframes, ignore_index=True)

ruta_archivo_final = "C:/Users/Julian/OneDrive/Escritorio/SLB/Livianos/Agu_11.xlsx"
df_final.to_excel(ruta_archivo_final, index=False)

print("Archivos unidos y guardados en:", ruta_archivo_final)