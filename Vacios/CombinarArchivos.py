import pandas as pd
import glob

<<<<<<< HEAD
ruta_archivos = 'C:/Users/57317/Documents/SLB/SLB_programas/Vacios/reportes/*.xlsx'
=======
ruta_archivos = 'C:/Users/57317/Desktop/SLB_Practicas/Vacios/reportes/*.xlsx'
>>>>>>> 4a6c0e269cf9167a4de7e743651e7ed1b63e04cb
# Obtener la lista de archivos que coinciden con el patrón
archivos = glob.glob(ruta_archivos)

# Leer los archivos y combinarlos en un DataFrame
dataframes = []
for archivo in archivos:
    try:
        # Leer todos los datos
        df = pd.read_excel(archivo)
        dataframes.append(df)
    except Exception as e:
        print(f"Error al leer el archivo {archivo}: {str(e)}")

# Combinar los DataFrames en uno solo
combined_df = pd.concat(dataframes, ignore_index=True)
# Eliminar filas duplicadas
#combined_df = combined_df.drop_duplicates()
combined_df = combined_df.sort_values('CONSECUTIVO')
# Guardar el DataFrame combinado en un archivo excel
<<<<<<< HEAD
combined_df.to_excel('C:/Users/57317/Documents/SLB/SLB_programas/Vacios/reportes/UnidosVacios.xlsx', index=False)
=======
combined_df.to_excel('C:/Users/57317/Desktop/SLB_Practicas/Vacios/reportes/UnidossVacios.xlsx', index=False)
>>>>>>> 4a6c0e269cf9167a4de7e743651e7ed1b63e04cb
