import re
import pandas as pd

txt = "{1,'200',3,4,5,6,77,23,222,1}"
lista  = ['1','23','200','100']

x = re.findall('\d+',str(txt))

print(x)

# df = pd.read_csv('./New_DB_Personas.csv')

# print(df)

# def encontrar(row):
#     ls = re.findall('\d+',row['presencias'])
#     return ls

# df['lista'] = df.apply(encontrar, axis=1)

# print(df['lista'].to_numpy())