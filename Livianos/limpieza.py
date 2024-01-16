import pandas as pd
import re
import numpy as np
from unidecode import unidecode
import funciones

#Cargar el archivo de Excel
df=pd.read_excel('livianos16.xlsx')

#¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ IMPORTANTE CAMBIAR FECHA PARA CADA DIA !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#Establecer variables
cordinator="Paola Andrea Chacon Acuna"
fecha="Feb-24"
# Definir una función para truncar los valores de la columna
def truncar_cadena(cadena,op):
    cadena = str(cadena)
    
    if "CALL" not in cadena:
        cadena.replace("-","")
        
    if op==1:
        if "CALL" not in cadena:
            cadena=cadena.replace(" ","")
            if op==1:
                if len(cadena) > 6:
                    return cadena[:6]
                else:
                    return cadena
        else:
            return "CALL OUT" 
    if op==2:
        if "CALL" not in cadena:
            cadena=cadena.replace(" ","")
            if len(cadena) > 6:
                return cadena[-6:]
            else:
                return cadena
        else:
            cadena=cadena.replace(" ","")
            if len(cadena) > 6:
                return cadena[:6]
            else:
                return cadena
def mapear_renta(row):
    rentas=pd.read_excel("Placas.xlsx",sheet_name="Renta",header=0)
    matricula=row['Vehicle plate']
    matching_row=rentas.loc[rentas['Cupo/Placa']==matricula]
    if not matching_row.empty:
        return matching_row['Clase'].values[0]
    else:
        return "No encontrado"
def proveedores(row):
    rentas=pd.read_excel("Placas.xlsx",sheet_name="Renta",header=0)
    call=pd.read_excel("Placas.xlsx",sheet_name="Call Out",header=0)
    
    if row['Service Type']=="RENTA FIJA OFS":
            matricula=row['Vehicle plate']
            matching_row=rentas.loc[rentas['Cupo/Placa']==matricula]
            if not matching_row.empty:
                return matching_row['Segmento'].values[0]
            else:
                return None
    else:
            supplier=row['Suppliers'].lower()
            
            #Search for the supplier value in the Excel column of the DataFrame "CALL"
            call_row=call.loc[call['Excel'].str.lower()==supplier]
            if not call_row.empty:
                #Get the value from the corresponding row in the "SP" column of the df call
                supplier_sp_value=call_row['SP'].values[0]
                return supplier_sp_value
            for _, call_row in call.iterrows():
                if re.search(call_row['Excel'], supplier, re.IGNORECASE):
                    return call_row['SP']
            return row['Suppliers']  
def verificarWBS(cadena):
    cadena=str(cadena)
    cadena=cadena.upper()
    patron_formato1 = r'^CO\d{6}$'
    patron_formato2 = r'^J\.\d{2}\.\d{6}$'
    if re.search(patron_formato1, cadena) or re.search(patron_formato2, cadena):
        #comentado  
        return cadena
    else:
        if len(cadena)==6 and cadena.isdigit():
            cadena=f"CO{cadena}"
            return cadena
        else:
            cadena.replace(' ','')
            return cadena
# Función para eliminar tildes de una palabra
def eliminar_tildes(palabra):
    return unidecode(palabra)
#Corregir los nombres de los lugares
def limpiar_lugares(lugar,columna):
    lugar=str(lugar)
    lugar=unidecode(lugar)
    lugar=lugar.upper()
    """ciudades=['BOGOTA','VILLAVICENCIO','NEIVA','COTA','PUERTO WILCHES','CASTILLA','ACACIAS','YOPAL','VILLANUEVA','OASIS']"""
    ciudades=['BOGOTA','VILLAVICENCIO','NEIVA','COTA','PUERTO WILCHES','CASTILLA','ACACIAS','OASIS']
    partes=lugar.split('-')
    if len(lugar)<15: 
        for ciudad in ciudades:
            match=re.search(rf'\b{ciudad}\b',lugar,flags=re.IGNORECASE)
            if match:
                return match.group()     
    return lugar
def quitar_separadores(valor):
    return f'{valor:,}'.replace(',', '')
def sin_decimales(valor):
    try:
        valor_float = float(valor)
        return int(valor_float)  # Convertir a entero y luego a cadena
    except ValueError:
        return int(valor)
def urbano(ciudad):
    ciudad=unidecode(ciudad)
    if re.search('bogota',ciudad,re.IGNORECASE) or re.search('cota',ciudad,re.IGNORECASE):
        return True
    return False
def villavo(ciudad):
    ciudad=unidecode(ciudad)
    if re.search('villavicencio',ciudad,re.IGNORECASE):
        return True
    return False
def calcular_distancia(row):
    aux = funciones.distanciaReal(row['Origin'], row['Destination'])
    if aux<50:
        aux=50
    if row['Origin']==row['Destination']:
        aux=100
    if pd.isnull(row['Distance KM']):
        if urbano(row['Origin'])==True and urbano(row['Destination']):
            return 80*row["DaysOfServices"]
        if row['Origin']==row['Destination']:
            aux=aux*row['DaysOfServices']
            if row['HORAS'] == '24h':
                aux = aux * 2
            return int(aux)
        elif row['DaysOfServices']>1:
            aux=aux+(100*(row['DaysOfServices']-1))
        elif row['DaysOfServices']==1:
            aux=aux                
    elif row['Distance KM'] < 30:
        aux=aux+(100*(row['DaysOfServices']-1))
    else:
        return row['Distance KM']
    if row['HORAS'] == '24h':
            aux = aux * 2
    return int(aux)
    
def provisionar(row):
    rentas=pd.read_excel("Placas.xlsx",sheet_name="Renta",header=0)
    # Date and hour to compare against (e.g., '09/25/2023 14:00:00')
    hour_request=row['Fecha y hora de creacion de OB2']
    def recargo_hora(freight,hour,add,superadd):
        #¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ IMPORTANTE CAMBIAR FECHA PARA CADA DIA !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       compare_datetime_a = pd.to_datetime('01/15/2024 17:00:00', format='%m/%d/%Y %H:%M:%S')
       compare_datetime_b = pd.to_datetime('01/15/2024 14:00:00', format='%m/%d/%Y %H:%M:%S')
       if hour > compare_datetime_a and hour<compare_datetime_b:
           return freight+add
       elif hour >=compare_datetime_b:
           return freight+superadd
       else:
           return freight
           
    if row['Service Type']=="RENTA FIJA OFS":
        tipo=mapear_renta(row)
        freight=0
        if not tipo=="PICKUP":
            if tipo=="AUT HIBRIDO" or tipo=="PICK UP ELECTRICA":
                #retorno=input(f"Es un recorrido es un {tipo} con {row['GS']} con retorno o día (1: Es todo el día ; 2. 24 horas ")
                if row['HORAS']=='24h':
                    freight= 550000*row['DaysOfServices']
                else:
                    freight=350000*row["DaysOfServices"]
            freight=recargo_hora(freight,hour_request,40000,60000)
            return freight
                    
        if urbano(row['Origin'])==True and urbano(row['Destination']):
            if row['HORAS']=='24h':
                freight= 750000*row["DaysOfServices"]
            else:
                freight= 550000*row["DaysOfServices"]
            freight=recargo_hora(freight,hour_request,40000,60000)
            return freight
        
        
        palabras_busqueda = ["Cristalina", "Pendare", "Quifa", "Rubiales","Ocelote","Hamacas","Caño Sur","Cano Sur","Rubial","Puerto Gaitan","Gaitan"]
        origen = row['Origin']
        destino = row['Destination']

        coincidencia = re.search("|".join(palabras_busqueda), origen, re.IGNORECASE) or re.search("|".join(palabras_busqueda), destino, re.IGNORECASE)
        if coincidencia:
            if urbano(row['Origin'])==True or urbano(row['Destination']) or villavo(row['Origin'])==True or villavo(row['Destination']):
                if urbano(row['Origin']) or urbano(row['Destination']):
                    tarifa=2500000+((row['DaysOfServices']-2)*800000)
                elif villavo(row['Origin'])==True or villavo(row['Destination']):
                    tarifa=1500000+((row['DaysOfServices']-1)*800000) 
                else:
                    print(f"Los días de la {row['GS']} son {row['DaysOfServices']} y el origen es {row['Origin']} y el final es {row['Destination']}")
                    tarifa= input("Ingrese la provisión de este servicio, recuerde que:\nDesde bogota (2 días + días de servicio): $2,500,000 y con retorno $3,500,000\nDesde Villavo (1 días + días de servicio): $1,500,000 y con retorno $2,500,000.  ")
                    tarifa=int(tarifa)
            else:    
                tarifa=row['DaysOfServices']*800000
            if pd.notna(row['TIPO DE VIAJE']) and re.search('emergencia', row['TIPO DE VIAJE'], flags=re.IGNORECASE):
                tarifa=tarifa+300000
            else:
                tarifa=recargo_hora(tarifa,hour_request,300000,400000)    
            return tarifa
        else:
            freight=row['DaysOfServices']*700000
            if row['HORAS']=='24h':
                freight=row['DaysOfServices']*850000
            #or row['Fecha y hora de creacion de OB']
            #df['Fecha Finalizacion2'] = pd.to_datetime(df['Fecha Finalizacion'], format='%m/%d/%Y %H:%M:%S')
            if pd.notna(row['TIPO DE VIAJE']) and re.search('emergencia', row['TIPO DE VIAJE'], flags=re.IGNORECASE) :
                freight=freight+150000 
            else: 
                freight=recargo_hora(freight,hour_request,150000,200000)   
            return freight
            
    else:
        if 150000 < row['StandByDays'] < 1500000:
            costo= int(row['StandByDays']/100000)
            costo=costo+1
            if(row['Vehicle Type']=="CHALUPA"and ['DaysOfServices']==1) :
                freight=1600000
                return freight
            if (row['StandByDays'] % 100000)==0:
                freight=row['DaysOfServices']*costo*100000
            elif(row['StandByDays'] % 100000)<=70000:
                freight=row['DaysOfServices']*costo*100000
            else:
                costo=costo+1
                freight=row['DaysOfServices']*costo*100000    
        else:
            if 'ARAUCA' in (row['Origin'], row['Destination']):
                freight = row['DaysOfServices'] * 1200000
            elif 'GEINTEPROL' in row['Suppliers']:
                freight = 800000 if row['HORAS'] == '24h' else 550000
            elif 'AVANT' in row['Suppliers']:
                freight = row['DaysOfServices'] * (500000 if row['HORAS'] == '12h' else 700000)
            elif 'OPEN' in row['Suppliers']:
                freight = row['DaysOfServices'] * (700000 if row['HORAS'] == '12h' else 900000)
            elif 'PORTRANS' in row['Suppliers']:
                freight = row['DaysOfServices'] * (600000 if row['HORAS'] == '12h' else 900000)
            elif 'CASANARE' in row['Suppliers']:
                freight = row['DaysOfServices'] * (700000 if row['HORAS'] == '12h' else 1050000)
            elif 'BARUC' in row['Suppliers']:
                freight = row['DaysOfServices'] * (650000 if row['HORAS'] == '12h' else 1000000)
            elif 'FRONTERAS' in row['Suppliers']:
                freight = row['DaysOfServices'] * (500000 if row['HORAS'] == '12h' else 700000)
            elif 'SOTRACASA' in row['Suppliers']:
                freight = row['DaysOfServices'] * (700000 if row['HORAS'] == '12h' else 1100000)                
            else:
                if row['HORAS'] == '24h':
                    pick2 = input(f"El servicio {row['GS']} utiliza doble camioneta para las 24 horas: 1 Si una sola camioneta, 2 si son dos camionetas: ")
                    freight =row['DaysOfServices'] * (700000*2 if pick2=='2'else  1000000)
                else:
                    freight=row['DaysOfServices'] *800000
    return freight

def resaltar_fila(valor):
    return ['background-color: yellow' if v else '' for v in valor]            
def parchar(row):
    if pd.isnull(row['Distance KM']):
        return 100 * row['DaysOfServices']
    return row
def tipo(row):
    tipo = row['Vehicle Type'].upper()
    if 'PICK' in tipo:
        df.loc[row.name, 'Vehicle Type'] = 'PICKUP'
    elif 'ESCOLTA' in tipo:
        df.loc[row.name, 'Vehicle Type'] = 'ESCOLTAS'
        df.loc[row.name, 'Vehicle plate']='CALL OUT'
        df.loc[row.name, 'Real Plate services'] = input(f"Ingrese la placa que hizo el servicio de escolta con {row['NN']}: ")
        return 'ESCOLTAS'
    elif 'CHALUPA' in tipo:
        df.loc[row.name, 'Vehicle Type'] = 'CHALUPA'
        df.loc[row.name, 'Vehicle plate']='CALL OUT'
        df.loc[row.name, 'Real Plate services'] = "AST-10"
    return tipo

#Limpieza

df=df[df['ESTADO'].str.lower() != 'viaje cancelado']
df=df.loc[df['BL'] != 'ESP']

#Reemplazo los valores de Logistic Cordinator
df['Logistic Cordinator']=cordinator
#Copiar las columna 1 a otras 2
df['Order Base'] = df['NN']
df['Shipment'] = df['NN']
#Dejar un unico formato de fecha
df['Period']=fecha
# Formato de placas
df['Vehicle plate'] = df['Vehicle plate'].apply(lambda x: truncar_cadena(x, op=1))
df['Real Plate services'] = df['Real Plate services'].apply(lambda x: truncar_cadena(x, op=2))
df['Real Plate services'] = df['Real Plate services'].str.upper()
df['Vehicle plate'] = df['Vehicle plate'].str.upper()
# De SI a YES
df['Rechargable Cost To Client']=df['Rechargable Cost To Client'].str.upper().replace('SI','YES')
#Vamos a corregir el WBS
df['WSB'] = df['WSB'].apply(verificarWBS)
#Calcular los días 
# Supongamos que tienes un DataFrame df con columnas 'Fecha Finalizacion' y 'Fecha y hora de cargue'
df['Fecha Finalizacion2'] = pd.to_datetime(df['Fecha Finalizacion'], format='%m/%d/%Y %H:%M:%S')
df['Fecha y hora de cargue2'] = pd.to_datetime(df['Fecha y hora de cargue'], format='%m/%d/%Y %H:%M:%S')
df['Fecha y hora de creacion de OB2']=pd.to_datetime(df['Fecha y hora de creacion de OB'],format='%m/%d/%Y %H:%M:%S')

# Calcula la diferencia en días, ignorando las horas
df['DaysOfServices'] = (df['Fecha Finalizacion2'].dt.floor('d') - df['Fecha y hora de cargue2'].dt.floor('d')).dt.days + 1

#Calcular días
"""# Assuming you have DataFrame df with columns 'Fecha Finalizacion' and 'Fecha y hora de cargue'
df['Fecha Finalizacion2'] = pd.to_datetime(df['Fecha Finalizacion'], format='%m/%d/%Y %H:%M:%S')
df['Fecha y hora de cargue2'] = pd.to_datetime(df['Fecha y hora de cargue'], format='%m/%d/%Y %H:%M:%S')

# Calculate the difference in days, considering only the date part
print(df['Fecha Finalizacion2'].dtype)
print(df['Fecha y hora de cargue2'].dtype)
df['DaysOfServices'] = (df['Fecha Finalizacion2'].dt - df['Fecha y hora de cargue2'].dt.date).dt.days + 1

# Drop the temporary columns if needed
df.drop(['Fecha Finalizacion2', 'Fecha y hora de cargue2'], axis=1, inplace=True)"""

"""df['Fecha Finalizacion2'] = pd.to_datetime(df['Fecha Finalizacion'], format='%m/%d/%Y %H:%M:%S')
df['Fecha y hora de cargue2'] = pd.to_datetime(df['Fecha y hora de cargue'], format='%m/%d/%Y %H:%M:%S')
df['DaysOfServices'] = np.ceil((df['Fecha Finalizacion2'] - df['Fecha y hora de cargue2']).dt.days+1)"""


df["Suppliers"]= df.apply(proveedores,axis=1)
# Distancia de Ciudades
    #1. Vamos primero a limpiar el nombre de las ciudades 
#df["Origin"]=df["Origin"].str.upper()
#df["Destination"]=df["Destination"].str.upper()
df["Origin"] = df["Origin"].apply(lambda x:limpiar_lugares(x,1))
df["Destination"] = df["Destination"].apply(lambda x:limpiar_lugares(x,1))

# Aplicar el estilo a la columna deseada, si hay algun valor lo coloreo
#df= df.style.applymap(resaltar_valor, subset=['Distance KM'])
     #2 Los que sean lugares iguales van a ser 100km por el número de días y de lo contrario lo dejo nulo   
df['Freight']=df.apply(provisionar,axis=1)
df['Distance KM']=df.apply(calcular_distancia,axis=1)      
columnas_eliminar = ['Fecha Finalizacion2', 'Fecha y hora de cargue2','Fecha y hora de creacion de OB2']
df=df.drop(columns=columnas_eliminar)
# Resaltar
condicion = df['HORAS'] =='24h'

df['Vehicle plate'] = df['Vehicle plate'].apply(lambda x: 'CALL OUT' if x == 'CALL OUT' else x)
#df['Distance KM']=df.apply(parchar,axis=1)  
df['Distance KM']=df['Distance KM'].apply(quitar_separadores)
df['Freight']=df['Freight'].apply(quitar_separadores)
df['Distance KM']=df['Distance KM'].apply(sin_decimales)
df['Freight']=df['Freight'].apply(sin_decimales)
df['Vehicle Type']=df['Vehicle Type'].str.upper().replace(' ','')
df['GLAccountType']="EMPLOYEE TRAVEL"
df['Vehicle Type']=df.apply(tipo,axis=1)
df['Distance KM']=""
df['Freight']=""
df.to_excel('01-16.xlsx', engine='openpyxl', index=False)

