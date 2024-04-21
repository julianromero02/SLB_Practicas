import pandas as pd

# Leer el archivo "petrol" el de EXTRAER LA INFROMACION
df_report = pd.read_excel('Daily Utilisation Report (7).xlsx', header=4)
df_cosmos = pd.read_excel('REPORTE RENTAS.xlsx',sheet_name='julio 7')#COSMOS
df_petrol = pd.read_excel('Entrapetrol 08-07-2023.xlsx', header=3)
#Unificar las bases de datos
df_petrol=df_petrol.iloc[:,3:]
df_cosmos=df_cosmos.rename(columns={'cupo':'Cupo'})
df_cosmos.columns = ['Cupo','Tipo de vehículo','BL','Origen (Donde inicia el vehículo el día del reporte)','Destino (Donde finaliza el vehículo el día del reporte)','Kms Totales','Kms en servicio','Kms Vacios','Estatus','Fecha inicio Estado','Fecha Finalizacion','ID Servicio']
print(df_cosmos.columns)
df_unido=pd.merge(df_cosmos,df_petrol,on='Cupo',how='inner')





#df_unido.to_excel('Formato_unido.xlsx', index=False)
