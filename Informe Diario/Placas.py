import pandas as pd
import re
import numpy as np
from unidecode import unidecode
from datetime import date

def limpiar_lugares(lugar):
    lugar=str(lugar)
    lugar=unidecode(lugar)
    lugar=lugar.upper()
    ciudades=['BOGOTA','VILLAVICENCIO','NEIVA','COTA','PUERTO WILCHES','CASTILLA','ACACIAS','OASIS',"ACACIAS","SOGAMOSO","CARTAGENA","SANTA MARTA","MONTERIA","SAHAGUN","BOSCONIA","CASTILLA","RUBIALES","PUERTO GAITAN","OASIS","CHIPAQUE",'PENDARE',"BARRANCABERMEJA","BUCARAMANGA","YOPAL","VILLANUEVA","VALLEDUPAR","AGUACHICA","RUBIALES","PUERTO BOYACA","TIBABOSA","PAZ DE ARIPORO","CRISTALINA",'MELGAR','CANO SUR','CAÑO SUR'],'FUNZA'
    for ciudad in ciudades:
        match=re.search(rf'\b{ciudad}\b',lugar,flags=re.IGNORECASE)
        if match:
            return match.group()     
    return lugar
def truncar_cadena(cadena):
    cadena = str(cadena)
    cadena.replace(" ","")
    if "CALL" not in cadena:
        cadena.replace("-","")
        return cadena
    return "CALL OUT"
 
def limpiezal(df,cancelado):
    columnas=["ESTADO","Vehicle plate","Origin","Destination","Fecha Finalizacion"]
    df=df[columnas]
    df=df[df['ESTADO'].str.lower() != cancelado]
    df=df[df['Vehicle plate']!="CALL OUT"]
    #~ se usa para negar la condición de filtro,
    df = df[~df['ESTADO'].str.contains('CALL', case=False)]
    df['Vehicle plate']=df['Vehicle plate'].apply(truncar_cadena)
    df["Origin"] = df["Origin"].apply(limpiar_lugares)
    df["Destination"] = df["Destination"].apply(limpiar_lugares)
    df['Fecha Finalizacion'] = pd.to_datetime(df['Fecha Finalizacion'])
    return df
def limpiezav(df,cancelado):
    columnas=["ESTADO","Vehicle plate","Origin","Destination","Fecha Finalizacion"]
    df=df[columnas]
    #df.rename(columns={'CONSECUTIVO':'NN'},inplace=True)
    df=df[df['ESTADO'].str.lower() != cancelado]
    df=df[df['Vehicle plate']!="CALL OUT"]
    df['Vehicle plate']=df['Vehicle plate'].apply(truncar_cadena)
    df["Origin"] = df["Origin"].apply(limpiar_lugares)
    df["Destination"] = df["Destination"].apply(limpiar_lugares)
    df['Fecha Finalizacion'] = pd.to_datetime(df['Fecha Finalizacion'])
    
    return df    
def reciente(df):
    df['Fecha Finalizacion']=pd.to_datetime(df['Fecha Finalizacion'])
    #Find the rows whit the most recent date
    idx_mas_reciente=df.groupby('Vehicle plate')['Fecha Finalizacion'].idxmax()
    df['Vehicle plate'] = df['Vehicle plate'].apply(truncar_cadena)
    df=df.loc[idx_mas_reciente]
    df['Fecha Finalizacion'] = df['Fecha Finalizacion'].dt.strftime('%m/%d/%Y')
    return df   
#def pico(row):
        
# Función para eliminar después de la coma si el valor es un string
def eliminar_despues_de_coma(cadena):
    if isinstance(cadena, str):
        return cadena.split(',')[0].strip()
    return cadena  # Mantener el valor si no es un string

def verificar(df,df_livianos):
    # Supongamos que tienes los DataFrames df y df_livianos
    # Filtrar placas comunes entre ambos DataFrames
    placas_comunes = set(df['Cupo']).intersection(df_livianos['Vehicle plate'])
    # Paso 1: Abrir el archivo en modo de escritura ('w' para escritura, 'a' para anexar)
    with open('observaciones.txt', 'w') as archivo:
    # Paso 2: Escribir contenido en el archivo
        archivo.write('Este es un ejemplo de cómo escribir en un archivo de texto en Python.\n')
        archivo.write('Puedes escribir múltiples líneas también.\n')
        archivo.write('Cada llamada a archivo.write agrega texto al archivo.\n')
        # Iterar sobre las placas comunes
        for placa in placas_comunes:
            # Filtrar los DataFrames por placa
            df_filtrado = df[df['Cupo'] == placa]
            df_livianos_filtrado = df_livianos[df_livianos['Vehicle plate'] == placa]
            
            # Obtener la cadena de 'Destination' en df_livianos
            destination_livianos = df_livianos_filtrado['Destination'].iloc[0]
                # Verificar si destination_livianos está en alguna parte de la columna 'Destination' de df
            if not df_filtrado['Destination'].str.contains(destination_livianos, case=False, na=False).any():
                        # Pedir la entrada del valor correcto
                    # Construir el mensaje de entrada con f-string
                mensaje = (
                            f"\nEl destino en formato sumistrado por el proveedor es: {df_filtrado['Destination'].tolist()}, y aparece en {df_filtrado['ESTADO'].tolist()} ,el carro finaliza el {df_filtrado['Fecha Finalizacion'].tolist()}:\n"
                            f"El destino en el Ontrack es: {df_livianos_filtrado['Destination'].tolist()}, con fecha de finalizacion {df_livianos_filtrado['Fecha Finalizacion'].tolist()}\n"
                            f"Para la placa {placa} tiene 3 opciones: \n1. Cambiar a la del OnTrack.\n2. Ingresar una nueva\n3.Dejar la misma\n"
                        )
                nueva_destination = input(mensaje)
                        # Modificar el DataFrame df con la nueva cadena en Destination
                if(nueva_destination=='1'):
                        archivo.write(f"\nEl destino en formato sumistrado por el proveedor es: {df_filtrado['Destination'].tolist()}, y aparece en {df_filtrado['ESTADO'].tolist()} ,el carro finaliza el {df_filtrado['Fecha Finalizacion'].tolist()}:\n"
                            f"El destino en el Ontrack es: {df_livianos_filtrado['Destination'].tolist()}, con fecha de finalizacion {df_livianos_filtrado['Fecha Finalizacion'].tolist()}\n")
                        df.loc[df['Cupo']==placa,'Destination']= df_livianos_filtrado['Destination'].iloc[0]
                        df.loc[df['Cupo']==placa,'Fecha Finalizacion']=df_livianos_filtrado['Fecha Finalizacion'].iloc[0]
                        if input("Requiere cambiar el estado del carro a DISPONIBLE: 1 si o 0 no: ") == '1':
                            df.loc[df['Cupo']==placa,'ESTADO']="DISPONIBLE"
                elif nueva_destination == '2':
                    archivo.write(
                    f"\nEl destino en formato sumistrado por el proveedor es: {df_filtrado['Destination'].tolist()}, y aparece en {df_filtrado['ESTADO'].tolist()} ,el carro finaliza el {df_filtrado['Fecha Finalizacion'].tolist()}:\n"
                    f"El destino en el Ontrack es: {df_livianos_filtrado['Destination'].tolist()}, con fecha de finalizacion {df_livianos_filtrado['Fecha Finalizacion'].tolist()}\n")
                    df.loc[df['Cupo'] == placa, 'Destination'] = input("Ingrese el nombre del lugar: ")
                    df.loc[df['Cupo'] == placa, 'Fecha Finalizacion'] = df_livianos_filtrado['Fecha Finalizacion'].iloc[0]
                    if input("Requiere cambiar el estado del carro a DISPONIBLE: 1 si o 0 no: ") == '1':
                        df.loc[df['Cupo'] == placa, 'ESTADO'] = "DISPONIBLE"
    return df

#Read the dailty report 
df_report = pd.read_excel('Daily Utilisation Report.xlsx', header=4)
#df_cosmos = pd.read_excel('REPORTE JULIO-AGOSTO.xlsx',sheet_name='JULIO 18')#COSMOS
df_petrol = pd.read_excel('Entrapetrol.xlsx', header=1)
#Unificar las bases de datos
df_petrol=df_petrol.iloc[:,1:]
# Leer el archivo "formato guia control renta" el de realizar el cambio
df_formato_guia = pd.read_excel('Formato guia control de renta.xlsx', sheet_name='Control Renta Livianos', header=3, parse_dates=['Fecha Inicio', 'Fecha Finalizacion'])

df_formato_guia=df_formato_guia.iloc[:,2:]

df_livianos=pd.read_excel('livianos.xlsx',header=0)
df_vacios=pd.read_excel('vacios.xlsx',header=0)
df_livianos=limpiezal(df_livianos,'viaje cancelado')
df_vacios=limpiezav(df_vacios,'cancelar viaje')
df_livianos=pd.concat([df_livianos,df_vacios],ignore_index=True)
df_livianos=reciente(df_livianos)

print(df_livianos) 

# Obtener las columnas "Matricula" y "Total Distancia(km)" del archivo "informe"
matriculas_report = df_report['Matrícula'].tolist()
distancias_report = df_report['Total Distancia (km)'].tolist()
# Distancias de entrapetrol
matriculas_petrol= df_petrol['Cupo'].tolist()
distancias_petrol = df_petrol['Kms Totales'].tolist()
#Vehicle plate
matriculas_vacios=df_vacios['Vehicle plate'].to_list()
matriculas_livianos=df_livianos['Vehicle plate'].to_list()
# Crear un diccionario para mapear las matriculas con las distancias del "informe" 
dict_report = dict(zip(matriculas_report, distancias_report))
dict_petrol = dict(zip(matriculas_petrol, distancias_petrol))
# Crear una nueva columna "Kms Totales" en el archivo "formato guia control renta"
df_formato_guia['Kms Nuevo Totales'] = df_formato_guia['Cupo'].map(dict_report)
df_formato_guia['Kms Totales petrol'] = df_formato_guia['Cupo'].map(dict_petrol)
# Combinar los valores existentes con los nuevos valores solo donde haya coincidencia de placas
#df_formato_guia['Kms Totales'] = df_formato_guia['Kms Totales petrol'].fillna(df_formato_guia['Kms Nuevo Totales'])
df_formato_guia['Kms Totales']=df_formato_guia['Kms Nuevo Totales'].fillna(df_formato_guia['Kms Totales petrol'])
# Eliminar la columna "Kms Nuevo Totales"
df_formato_guia.drop('Kms Nuevo Totales', axis=1, inplace=True)
df_formato_guia.drop('Kms Totales petrol',axis=1,inplace=True)
# Obtener las columnas "Matricula" y "Total Distancia(km)" del archivo "petrol"
columnas_petrol = ['Cupo', 'BL', 'Origen',
                   'Destino', 'ESTADO',
                   'Fecha Inicio', 'Fecha Finalizacion', 'ID Servicio']
df_petrol = df_petrol[columnas_petrol]
# Realizar el mapeo de las columnas deseadas en el archivo "formato guia control renta"
for columna in columnas_petrol:
    # Crear un diccionario para mapear las matriculas con los valores de la columna actual
    dict_petrol = dict(zip(df_petrol['Cupo'], df_petrol[columna]))
    # Actualizar la columna correspondiente en el archivo "formato guia control renta"
    df_formato_guia[columna] = df_formato_guia['Cupo'].map(dict_petrol)
    
# Convertir las columnas de fecha al formato de texto
df_formato_guia['Fecha Inicio'] = df_formato_guia['Fecha Inicio'].astype(str)
df_formato_guia['Fecha Finalizacion'] = df_formato_guia['Fecha Finalizacion'].astype(str)
# Reemplazar los guiones "-" por barras "/" en las columnas de fecha
df_formato_guia['Fecha Inicio'] = df_formato_guia['Fecha Inicio'].str.replace('-', '/')
df_formato_guia['Fecha Finalizacion'] = df_formato_guia['Fecha Finalizacion'].str.replace('-', '/')

# Reemplazar NaN y NaT por valores vacíos en las dos columnas específicas
columnas = ['Fecha Inicio', 'Fecha Finalizacion']
valores_a_reemplazar = {"nan": '', "NaT": ''}
df_formato_guia[columnas] = df_formato_guia[columnas].replace(valores_a_reemplazar)
df_formato_guia.loc[df_formato_guia['ESTADO']=="DISPONIBLE",columnas]=""
df_formato_guia.rename(columns={"Origen":'Origin',"Destino":"Destination"},inplace=True)
df_formato_guia['Origin']=df_formato_guia['Origin'].str.upper()
df_formato_guia['Destination']=df_formato_guia['Destination'].str.upper()

df_formato_guia['Origin']=df_formato_guia['Origin'].apply(eliminar_despues_de_coma)
df_formato_guia['Destination']=df_formato_guia['Destination'].apply(eliminar_despues_de_coma)




df_formato_guia=verificar(df_formato_guia,df_livianos)

# Guardar los cambios en el archivo "formato guia control renta"
df_formato_guia.to_excel('ACT_Formato_guia_control_renta.xlsx', index=False)

