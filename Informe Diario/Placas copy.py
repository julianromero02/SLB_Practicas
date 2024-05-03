import pandas as pd
import re
import numpy as np
from unidecode import unidecode
from datetime import date
from datetime import datetime
def limpiar_lugares(lugar):
    lugar=str(lugar)
    lugar=unidecode(lugar)
    lugar=lugar.upper()
    ciudades=['BOGOTA','VILLAVICENCIO','NEIVA','COTA','PUERTO WILCHES','CASTILLA','ACACIAS','OASIS',"ACACIAS","SOGAMOSO","CARTAGENA","SANTA MARTA","MONTERIA","SAHAGUN","BOSCONIA","CASTILLA","RUBIALES","PUERTO GAITAN","OASIS","CHIPAQUE",'PENDARE',"BARRANCABERMEJA","BUCARAMANGA","YOPAL","VILLANUEVA","VALLEDUPAR","AGUACHICA","RUBIALES","PUERTO BOYACA","TIBABOSA","PAZ DE ARIPORO","CRISTALINA",'MELGAR','CANO SUR','CAÑO SUR','MADRIRD','FUNZA','CHIA','MOSQUERA']
    for ciudad in ciudades:
        match=re.search(rf'\b{ciudad}\b',lugar,flags=re.IGNORECASE)
        if match:
            return match.group()     
    return lugar
def limpiar_estados(estado):
    estado=str(estado)
    estado=unidecode(estado)
    estado=estado.upper()
    est = [r'SERVICIO', r'DISPONIBLE', r'PROGRAMADO', r'MANTENIMIENTO', r'SIN CONDUCTOR']
    for esta in est:
        match = re.search(rf'\b{esta}\b', estado)
        if match:
            return match.group()
    return estado
def truncar_cadena(cadena):
    cadena = str(cadena)
    cadena=cadena.replace(" ","")
    if "CALL" not in cadena:
        return cadena
    return "CALL OUT"    
def limpiezal(df,cancelado):
    columnas=["NN","ESTADO","Vehicle plate","Origin","Destination","Fecha y hora de cargue","Fecha Finalizacion","BL"]
    df=df[columnas]
    df.rename(columns={'NN':'NN','Fecha y hora de cargue':'Fecha y Hora de cargue'},inplace=True)
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
    columnas=["CONSECUTIVO","ESTADO","Vehicle plate","Origin","Destination","Fecha y Hora de cargue","Fecha Finalizacion","BL"]
    df=df[columnas]
    df.rename(columns={'CONSECUTIVO':'NN'},inplace=True)
    df=df[df['ESTADO'].str.lower() != cancelado]
    df=df[df['Vehicle plate']!="CALL OUT"]
    df['Vehicle plate']=df['Vehicle plate'].apply(truncar_cadena)
    df["Origin"] = df["Origin"].apply(limpiar_lugares)
    df["Destination"] = df["Destination"].apply(limpiar_lugares)
    df['Fecha Finalizacion'] = pd.to_datetime(df['Fecha Finalizacion'])   
    return df   
def limpiezau(df):
    columnas=["CONSECUTIVO","ESTADO","PLACA VEHICULO / VEHICLE LICENSE PLATE","16.- Seleccione el municipio de origen / Select the municipality of your origin","18.- Seleccione el municipio de destino / Select the municipality of your destination","14.- Elija la fecha y hora del servicio / Choose service date and hour","FIN DE RUTA / ROUTE END","8.- Sub Business Line Reservoir Performance Evluation /RPE)","PROVEEDOR"]
    df=df[columnas]
    df=df[df["PROVEEDOR"]=="ENTRAPETROL"]
    df.drop(columns=['PROVEEDOR'],inplace=True)
    df.rename(columns={"CONSECUTIVO":"NN","PLACA VEHICULO / VEHICLE LICENSE PLATE":"Vehicle plate","16.- Seleccione el municipio de origen / Select the municipality of your origin":"Origin","18.- Seleccione el municipio de destino / Select the municipality of your destination":"Destination","14.- Elija la fecha y hora del servicio / Choose service date and hour":"Fecha y Hora de cargue","FIN DE RUTA / ROUTE END":"Fecha Finalizacion","8.- Sub Business Line Reservoir Performance Evluation /RPE)":"BL"},inplace=True)
    df=df[df['ESTADO']!='CANCELAR']
    df['Fecha Finalizacion']=df["Fecha y Hora de cargue"]
    df['BL']=df['BL'].str[5:]
    df["Origin"] = df["Origin"].apply(limpiar_lugares)
    df["Destination"] = df["Destination"].apply(limpiar_lugares)
    df['Fecha Finalizacion'] = pd.to_datetime(df['Fecha Finalizacion'])
    df["Fecha y Hora de cargue"] = pd.to_datetime(df['Fecha y Hora de cargue'])
    df['Fecha Finalizacion']+=pd.Timedelta(hours=4)
    #print( f"{df} \n")
    return df
    #Modificar el tema de las fechas, para luego si pasarlo a tipo fecha De 2023-09-19 13:37:02 o quizá no
    
import pandas as pd
from datetime import datetime
import re

# Define a function to convert the date to the desired format
def reordenar_fecha(fecha_str):
        # Try parsing with the format "M/D/YYYY H:mm"
    try:
        fecha_obj = datetime.strptime(fecha_str, "%m/%d/%Y %H:%M")
        return fecha_obj.strftime("%m/%d/%Y %H:%M:%S")
    except ValueError:
        pass 
    try:
        return datetime.strptime(fecha_str, "%Y/%m/%d %H:%M:%S").strftime("%m/%d/%Y %H:%M:%S")
    except ValueError:
        pass  # If parsing with the first format fails, proceed to the next format

    # Try parsing with the first format "%Y-%m-%d %H:%M:%S"

    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S").strftime("%m/%d/%Y %H:%M:%S")
    except ValueError:
        # If parsing fails, try the second format "%m/%d/%Y %H:%M:%S"
        try:
            return datetime.strptime(fecha_str, "%m/%d/%Y %H:%M:%S").strftime("%m/%d/%Y %H:%M:%S")
        except ValueError:
            # If both fail, assume it's just a date (without time)
            return fecha_str

# Function to process recent data
def reciente(df):
    df.rename(columns={'NN':'ID Servicio',"Origin":"Origen","Destination":"Destino","Vehicle plate":"Cupo","Fecha y Hora de cargue":'Fecha Inicio'},inplace=True)
    df['Fecha Finalizacion'] = df['Fecha Finalizacion'].astype(str)
    df['Fecha Inicio'] = df['Fecha Inicio'].astype(str)
    
    # Apply the reordenar_fecha function to reorder date formats
    df['Fecha Inicio'] = df['Fecha Inicio'].apply(reordenar_fecha)
    df['Fecha Finalizacion'] = df['Fecha Finalizacion'].apply(reordenar_fecha)
    
    # Convert to datetime
    df['Fecha Inicio'] = pd.to_datetime(df['Fecha Inicio'], errors='coerce')
    df['Fecha Finalizacion'] = pd.to_datetime(df['Fecha Finalizacion'], errors='coerce')
    
    # Find the rows with the most recent date
    idx_mas_reciente = df.groupby('Cupo')['Fecha Finalizacion'].idxmax()
    df = df.loc[idx_mas_reciente]
    
    return df


# Función para eliminar después de la coma si el valor es un string
def eliminar_despues_de_coma(cadena):
    if isinstance(cadena, str):
        return cadena.split(',')[0].strip()
    return cadena  # Mantener el valor si no es un string

def actESTADO(row, today):
    fecha_str = row['Fecha Finalizacion']
    fecha_inicio = row['Fecha Inicio']
    fecha_inicio = reordenar_fecha(fecha_inicio)
    fecha = reordenar_fecha(fecha_str)
    palabra = ['CONDUCTOR', 'MANTENIMIENTO']
    today = pd.Timestamp(today)  # Convert today to a Timestamp object
    
    # Attempt to parse the dates
    try:
        fecha = pd.to_datetime(fecha, format="%m/%d/%Y %H:%M:%S")
        fecha_inicio = pd.to_datetime(fecha_inicio, format="%m/%d/%Y %H:%M:%S")
    except ValueError:
        # If parsing fails, assume it's an incorrect date
        fecha_inicio = fecha_inicio
        print(fecha_inicio)

    estado_str = str(row['ESTADO'])  # Convert the value of the 'ESTADO' column to a string

    if not (re.search(rf'\b{"|".join(palabra)}\b', estado_str, flags=re.IGNORECASE)):
        if pd.notnull(fecha) and fecha < today:
            return "DISPONIBLE"
        elif pd.notnull(fecha) and fecha >= today and fecha_inicio <= today:
            return "EN SERVICIO"
        elif pd.notnull(fecha_inicio) and fecha_inicio > today and len(row['Fecha Inicio'].strip()) > 0:
            return "PROGRAMADO"
        elif pd.notnull(fecha) and fecha >= today:
            return "EN SERVICIO"
    return row['ESTADO']
def picoyplaca(row,op):
    pico = ""
    ciudad_ini = row['Origin']
    ciudad_fin = row['Destination']

    end = int((row['Cupo'])[-1])
    hoy = datetime.now()
    dia = hoy.day
    dia = int(dia)
    dia_de_semana = hoy.weekday()
    if op==1:
        dia_de_semana = hoy.weekday()
    elif op==2:
        # Calculate tomorrow's date
        dia_de_semana=hoy.weekday()+1
        
        #print(dia_de_semana)
       
    # Función para verificar las restricciones en una ciudad específica
    def verificar_restricciones(ciudad, end, dia_de_semana):
        if dia_de_semana!=5 or dia_de_semana!=6:
            if re.search('bogota', ciudad, re.IGNORECASE) or re.search('cota', ciudad, re.IGNORECASE):
                if dia_de_semana % 2 == 0:
                    if end <= 5 and end != 0:
                        return "SI"
                elif dia_de_semana % 2 !=0 :
                    if end > 5 or end == 0:
                        return "SI"
                else:
                    return "NO"
            if re.search('villavicencio', ciudad, re.IGNORECASE):
                if (dia_de_semana == 1 and end in [1, 2]) or \
                (dia_de_semana == 2 and end in [3, 4]) or \
                (dia_de_semana == 3 and end in [5, 6]) or \
                (dia_de_semana == 4 and end in [7, 8]) or \
                (dia_de_semana == 0 and end in [9, 0]):
                    return "SI"
            if re.search(r'(bucaramanga|cartagena)', ciudad, re.IGNORECASE):
                if dia_de_semana == 0 and end in [5, 6]:
                    return "SI"
                elif dia_de_semana == 1 and end in [7, 8]:
                    return "SI"
                elif dia_de_semana == 2 and end in [9, 0]:
                    return "SI"
                elif dia_de_semana == 3 and end in [1, 2]:
                    return "SI"
                elif dia_de_semana == 4 and end in [3, 4]:
                    return "SI"
            if re.search('barranquilla',ciudad,re.IGNORECASE):
                if  (dia_de_semana==0 and end in [1,2,3,4])or \
                    (dia_de_semana==1 and end in [5,6,7,8])or \
                    (dia_de_semana==2 and end in [9,0,1,2])or \
                    (dia_de_semana==3 and end in [3,4,5,6])or \
                    (dia_de_semana==4 and end in [7,8,9,0]):
                    return "SI"
            if re.search('santa marta',ciudad,re.IGNORECASE):
                if  (dia_de_semana==0 and end in [2,3])or \
                    (dia_de_semana==1 and end in [4,5])or \
                    (dia_de_semana==2 and end in [6,7])or \
                    (dia_de_semana==3 and end in [8,9])or \
                    (dia_de_semana==4 and end in [0,1]):
                    return "SI"   
        return ""  # Si no se cumplen las restricciones en la ciudad
    
    # Verificar restricciones en el origen y destino
    if verificar_restricciones(ciudad_ini, end, dia_de_semana) == "SI" or \
       verificar_restricciones(ciudad_fin, end, dia_de_semana) == "SI":
        return "SI"
    
    return ""

def leeryUnir():
    df_livianos=pd.read_excel('livianos.xlsx',header=0)
    df_vacios=pd.read_excel('vacios.xlsx',header=0)
    df_urbanos=pd.read_excel('urbanos.xlsx',header=0)
    df_livianos=limpiezal(df_livianos,'viaje cancelado')
    df_vacios=limpiezav(df_vacios,'cancelar viaje')
    df_urbanos=limpiezau(df_urbanos)
    df_livianos=pd.concat([df_urbanos,df_livianos,df_vacios],ignore_index=True)
    df_livianos=reciente(df_livianos)
    #df_livanos=pd.concat([df_livianos,df_urbanos])
    print(df_livianos) 
    return df_livianos
    

#region Read the reports
df_report = pd.read_excel('Daily Utilisation Report.xlsx', header=4)
df_petrol = pd.read_excel('Entrapetrol.xlsx', header=1)
df_petrol=df_petrol.iloc[:,:]
df_formato_guia = pd.read_excel('Formato guia control de renta.xlsx', sheet_name='Control Renta Livianos', header=0, parse_dates=['Fecha Inicio', 'Fecha Finalizacion'])
df_formato_guia=df_formato_guia.iloc[:,:]
df_livianos=leeryUnir()

# Realiza la fusión (merge) basada en las columnas 'Matrícula' y 'Cupo'
df_formato_guia = pd.merge(df_formato_guia, df_report[['Matrícula', 'Sin viajes']], left_on='Cupo', right_on='Matrícula', how='left')
df_formato_guia=df_formato_guia.drop(columns=['Matrícula'])
# Leer el archivo "formato guia control renta" el de realizar el cambio
df_formato_guia['ESTADO']=df_formato_guia['ESTADO'].apply(limpiar_estados)
#df_formato_guia.loc[df_formato_guia['BL']=="VACIO",'BL']=""
#endregion

# Obtener las columnas "Matricula" y "Total Distancia(km)" del archivo "informe"
matriculas_report = df_report['Matrícula'].tolist()
distancias_report = df_report['Total Distancia (km)'].tolist()
#df_report['Sin viajes']=df_report['Sin viajes'].astype(str)
dias_report=df_report['Sin viajes'].tolist()

# Distancias de entrapetrol
matriculas_petrol= df_petrol['Cupo'].tolist()
distancias_petrol = df_petrol['Kms Totales'].tolist()

#Vehicle plate
matriculas_livianos=df_livianos['Cupo'].to_list()
# Crear un diccionario para mapear las matriculas con las distancias del "informe" 
dict_report = dict(zip(matriculas_report, distancias_report))
    #dict_dias=dict(zip(matriculas_report,dias_report))
dict_petrol = dict(zip(matriculas_petrol, distancias_petrol))
# Crear una nueva columna "Kms Totales" en el archivo "formato guia control renta"
df_formato_guia['Kms Nuevo Totales'] = df_formato_guia['Cupo'].map(dict_report)
    #df_formato_guia['Dias en servicio nuevo']=df_formato_guia['Dias en servicio'].map(dict_dias)
df_formato_guia['Kms Totales petrol'] = df_formato_guia['Cupo'].map(dict_petrol)
# Combinar los valores existentes con los nuevos valores solo donde haya coincidencia de placas
    #df_formato_guia['Kms Totales'] = df_formato_guia['Kms Totales petrol'].fillna(df_formato_guia['Kms Nuevo Totales'])
df_formato_guia['Kms Totales']=df_formato_guia['Kms Nuevo Totales'].fillna(df_formato_guia['Kms Totales petrol'])
# Combine 'Dias en servicio' column
    #df_formato_guia['Dias en servicio'] = df_formato_guia['Dias en servicio nuevo'].fillna(df_formato_guia['Dias en servicio'])
# Eliminar la columna "Kms Nuevo Totales"
df_formato_guia.drop('Kms Nuevo Totales', axis=1, inplace=True)
df_formato_guia.drop('Kms Totales petrol',axis=1,inplace=True)
    #df_formato_guia.drop('Dias en servicio nuevo', axis=1, inplace=True)
# Obtener las columnas "Matricula" y "Total Distancia(km)" del archivo "petrol"
columnas_petrol = ['Coordinador','Cupo', 'BL', 'Origen',
                   'Destino', 'ESTADO',
                   'Fecha Inicio', 'Fecha Finalizacion', 'ID Servicio','Observaciones']
df_petrol = df_petrol[columnas_petrol]
columnas_livianos=['Cupo', 'Origen','BL',
                   'Destino','Fecha Inicio',
                'Fecha Finalizacion', 'ID Servicio']
# Realizar el mapeo de las columnas deseadas en el archivo "formato guia control renta"
for columna in columnas_petrol:
    # Crear un diccionario para mapear las matriculas con los valores de la columna actual
    dict_petrol = dict(zip(df_petrol['Cupo'], df_petrol[columna]))
    # Actualizar la columna correspondiente en el archivo "formato guia control renta"
    df_formato_guia[columna] = df_formato_guia['Cupo'].map(dict_petrol)
for columna in columnas_livianos:
    dict_livianos = dict(zip(df_livianos['Cupo'], df_livianos[columna]))
    #df_formato_guia[columna] = df_formato_guia['Cupo'].map(dict_livianos)
    df_formato_guia[columna] = df_formato_guia['Cupo'].map(dict_livianos).fillna(df_formato_guia[columna])

    
# region Convertir las columnas de fecha al formato de texto y luego a fecha
df_formato_guia['Fecha Inicio'] = df_formato_guia['Fecha Inicio'].astype(str)
df_formato_guia['Fecha Finalizacion'] = df_formato_guia['Fecha Finalizacion'].astype(str)

# Reemplazar los guiones "-" por barras "/" en las columnas de fecha
df_formato_guia['Fecha Inicio'] = df_formato_guia['Fecha Inicio'].str.replace('-', '/')
df_formato_guia['Fecha Finalizacion'] = df_formato_guia['Fecha Finalizacion'].str.replace('-', '/')

df_formato_guia['Fecha Inicio']=df_formato_guia['Fecha Inicio'].apply(reordenar_fecha)
df_formato_guia['Fecha Finalizacion']=df_formato_guia['Fecha Finalizacion'].apply(reordenar_fecha)
# endregion

#region Para estandarizar el nombre de los lugares encontrados
df_formato_guia.rename(columns={"Origen":'Origin',"Destino":"Destination"},inplace=True)
df_formato_guia['Origin']=df_formato_guia['Origin'].str.upper()
df_formato_guia['Destination']=df_formato_guia['Destination'].str.upper()

df_formato_guia['Origin']=df_formato_guia['Origin'].apply(eliminar_despues_de_coma)
df_formato_guia['Destination']=df_formato_guia['Destination'].apply(eliminar_despues_de_coma)
# endregion

today = pd.Timestamp.today().date()

df_formato_guia['ESTADO'] = df_formato_guia.apply(lambda row: actESTADO(row, today), axis=1)

# Reemplazar NaN y NaT por valores vacíos en las dos columnas específicas
columnas = ['Fecha Inicio', 'Fecha Finalizacion','ID Servicio']
valores_a_reemplazar = {"nan": '', "NaT": ''}
df_formato_guia[columnas] = df_formato_guia[columnas].replace(valores_a_reemplazar)
df_formato_guia.loc[df_formato_guia['BL']=="VACIO",'ID Servicio']=""
#df_formato_guia.loc[df_formato_guia['BL']=="VACIO",'BL']=""
df_formato_guia.loc[df_formato_guia['BL']=="VACIO",'ESTADO']="DISPONIBLE"
df_formato_guia.loc[df_formato_guia['ESTADO']=="DISPONIBLE",columnas]=""
df_formato_guia['PICO Y PLACA']=""
df_formato_guia['PICO Y PLACA MANANA']=""
df_formato_guia['PICO Y PLACA'] = df_formato_guia.apply(lambda row: picoyplaca(row, 1) if not isinstance(row['Cupo'], float) else None, axis=1)
df_formato_guia['PICO Y PLACA'] = df_formato_guia.apply(lambda row: picoyplaca(row, 2) if not isinstance(row['Cupo'], float) else None, axis=1)
 
df_formato_guia['ESTADO']=df_formato_guia['ESTADO'].apply(limpiar_estados)
# Guardar los cambios en el archivo "formato guia control renta"
df_formato_guia.to_excel('ACT_Formato_guia_control_renta.xlsx', index=False)

