import pandas as pd
import re

df=pd.read_excel("Agosto Vacios.xlsx")
formato = pd.read_excel("C:/Users/Julian/OneDrive/Escritorio/SLB/Informes diarios KM/ACT_Formato_guia_control_renta.xlsx")

# Calcular los kms por placa
sum_by_plate = df.groupby('Vehicle plate')['Distance KMS'].sum().reset_index()

# Crear un diccionario de mapeo entre 'Vehicle plate' y 'Distance KMS'
mapping_dict = sum_by_plate.set_index('Vehicle plate')['Distance KMS'].to_dict()

# Usar map() para asignar los valores de 'Distance KMS' al DataFrame formato
formato['Kms Vacios'] = formato['Cupo'].map(mapping_dict)

formato.to_excel("C:/Users/Julian/OneDrive/Escritorio/SLB/Informes diarios KM/ACT_Formato_guia_control_renta.xlsx",index=False)

"""# Paso 3: Crear una nueva hoja de Excel con los resultados
output_file_path = 'ruta/del/archivo_con_suma.xlsx'  # Cambia esto a la ruta donde quieres guardar el nuevo archivo Excel
with pd.ExcelWriter(output_file_path) as writer:
    sum_by_plate.to_excel(writer, sheet_name='Suma por placa', index=False)"""

