# --- ALGORITMO DE THOMPSON --- #
def algThompson(er):
    for i in range(len(er)):
        print(er[i])
    
    

# 1. El usuario ingresa una Expresión Regular
expresionRegular = input("Ingrese una Expresión Regular: ")

# 2. Creamos un Algoritmo de Thompson en base a la ER
algThompson(expresionRegular)

# 3. Leemos cadenas y verificamos si son aceptadas o no