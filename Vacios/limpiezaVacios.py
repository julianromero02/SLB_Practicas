import pandas as pd
import re
import numpy as np

import funciones

from unidecode import unidecode



#Corregir los nombres de los lugares
def limpiar_lugares(lugar):
    lugar=str(lugar)
    lugar=unidecode(lugar)
    lugar=lugar.upper()
    ciudades=['BOGOTA','VILLAVICENCIO','NEIVA','COTA','POZO AKIRA','PUERTO WILCHES','CASTILLA','ACACIAS','YOPAL','VILLANUEVA','PUERTO GAITAN','RUBIALES','TUNJA','CHIPAQUE','PENDARE','BARRANCABERMEJA','TAURAMENA','OASIS']
    #if len(lugar)<15: 
    for ciudad in ciudades:
        match=re.search(rf'\b{ciudad}\b',lugar,flags=re.IGNORECASE)
        if match:
            return match.group()
    return lugar
def limpiar_lugares2(lugar):
    lugar=str(lugar)
    lugar=unidecode(lugar)
    lugar=lugar.upper()
    return lugar
def quitar_separadores(valor):
    return f'{valor:,}'.replace(',', '')
def sin_decimales(valor):
    if type(valor)==str:
        return valor
    try:
        valor_float = float(valor)
        return int(valor_float)  # Convertir a entero y luego a cadena
    except ValueError:
        return int(valor)
#Función para que según el municipio me retorne el lugar más probable
def limpiar_lugares(lugar):
    lugar=str(lugar)
    lugar=unidecode(lugar)
    lugar=lugar.upper()
    ciudades=['BOGOTA','VILLAVICENCIO','NEIVA','COTA','PUERTO WILCHES','CASTILLA','ACACIAS','OASIS',"ACACIAS","SOGAMOSO","CARTAGENA","SANTA MARTA","MONTERIA","SAHAGUN","BOSCONIA","CASTILLA","RUBIALES","PUERTO GAITAN","OASIS","CHIPAQUE",'PENDARE',"BARRANCABERMEJA","BUCARAMANGA","YOPAL","VILLANUEVA","VALLEDUPAR","AGUACHICA","RUBIALES","PUERTO BOYACA","TIBABOSA","PAZ DE ARIPORO","CRISTALINA",'MELGAR','CANO SUR','CAÑO SUR','BARRANQUILLA','CARTAGENA','PAIPA','PUERTO ARAUJO','FUNZA','BARRANCA DE UPIA','DUITAMA','TAURAMENA','TIBASOSA',"BARRANCA DE UPIA","COGUA","RESTREPO","RIOACHA","MONTERÍA","PUERTO SALGAR","GUADUAS","RIOHACHA","TUNJA"]
    for ciudad in ciudades:
        match=re.search(rf'\b{ciudad}\b',lugar,flags=re.IGNORECASE)
        if match:
            return match.group()     
    return lugar
def municipio(row):
    reemplazos = {"META": "VILLAVICENCIO", "SANTANDER": "BARRANCABERMEJA", "CASANARE": "VILLANUEVA","CORDOBA":"MONTERIA","BOYACA":"DUITAMA","BOLIVAR":"CARTAGENA","MAGDALENA":"SANTA MARTA","ATLANTICO":"BARRANQUILLA"}
    #reemplazos2 = {"META": "ACACIAS", "SANTADER": "BUCARAMANGA","BOYACA":"PUERTO BOYACA"}
      # Cambia el nombre de la columna de búsqueda por la tuya
    
    for palabra, reemplazo in reemplazos.items():
        if palabra == row:
            row = reemplazo
            break  # Si se encuentra un reemplazo, se detiene la búsqueda
    return row
def calcular_distancia(row):
    aux = funciones.distanciaReal(row['Origin'], row['Destination'])
    if pd.isnull(row['Distance KMS']):
        return aux
    else:
        try:
            distance_kms = int(row['Distance KMS'])
        except ValueError:
            distance_kms = None  # Set to None if it cannot be converted to an integer
        # Check if 'aux' can be converted to an integer
        try:
            aux_value = int(aux)
        except ValueError:
            aux_value = None  # Set to None if it cannot be converted to an integer
        # Perform the comparison if both values are valid integers
        if distance_kms is not None and aux_value is not None:
            if distance_kms < 60 and aux_value > 60:
                if (row['Distance KMS'])==0:
                    return aux
                if(row['Distance KMS'])<60 and aux>60:
                    return aux
    return aux
#Cargar el archivo de Excel
df=pd.read_excel('v.xlsx')
#Elimino registros cancelados
df=df[df['ESTADO'].str.lower() != 'viaje cancelado']
df=df[df['ESTADO'].str.lower() != 'cancelar viaje']
df["Origin"] = df["Origin"].apply(limpiar_lugares)
df["Destination"] = df["Destination"].apply(limpiar_lugares)
#Reemplazo los valores de Logistic Cordinator
df['Logistic coordinator']="Paola Andrea Chacon Acuna"
df['Period']='Jan-24'
# De SI a YES
df['Rechargable Cost To Client']=df['Rechargable Cost To Client'].str.upper().replace('SI','YES')
df['Order Base']=df['CONSECUTIVO']
df['Shipment']=df['CONSECUTIVO']
df['Real Plate services']=df['Vehicle plate']
df['Suppliers']='COL_SCHLUMBERGER'
df['Vehicle Type']='PICKUP'
df['WBS Element']='EMPLOYEE TRAVEL'
df['Requester']='LOGISTICA'
#Calcular los días 
# Calcular los días

df['Days of services'] = 1
#columnas_eliminar = ['Fecha Finalizacion2', 'Fecha y hora de cargue2']
#df = df.drop(columns=columnas_eliminar)

#Lugares
df["Origin"] = df["Origin"].apply(limpiar_lugares)
df["Destination"]=df["Destination"].apply(limpiar_lugares)

# Reemplazar los valores nulos con una cadena vacía
df["Destination"]=df["Destination"].apply(municipio)
#df['Distance KMS']=df.apply(calcular_distancia,axis=1)

df['Distance KMS'] = df.apply(calcular_distancia, axis=1)

"""df['Distance KMS']=df['Distance KMS'].apply(quitar_separadores)
df['Freight']=df['Freight'].apply(quitar_separadores)"""
df['Distance KMS']=df['Distance KMS'].apply(sin_decimales)
df['Freight']=df['Freight'].apply(sin_decimales)

"""df['DistanceKMS'] = df['ColumnaA'].round()
# Quitar el formato y las comas de la columna "ColumnaA"
df['ColumnaA'] = df['ColumnaA'].apply(lambda x: x.replace(',', ''))"""

#Exportar
df.to_excel('vacios_limpios.xlsx',index=False)