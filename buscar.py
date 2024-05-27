def buscar(df_v, df_c):
    df_1 = df_v.explode('celdas')   # DF de variables
    df_2 = df_c.explode('celdas')   # DF de clase

    # Join de celdas de la variable con la clase
    df_j = df_1.set_index('celdas').join(df_2.set_index('celdas'))

    # En este DF están las celdas donde sí hay intersección
    df_cells_intersection = df_j[df_j['clase'].notnull()].reset_index()

    df_cells_intersection = df_cells_intersection.rename(columns={'clase':'new_clase'})
    
    # Los datos con NaN corresponden a datos donde no se hay intersección entre variables y clase. 
    print(df_2.set_index('celdas').join(df_cells_intersection.set_index('celdas')).sort_values(by=['celdas'], ascending=False).to_string())

    