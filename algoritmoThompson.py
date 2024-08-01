"""
Primer Proyecto - Trabajo Especial - "Algoritmo de Thompson"
@authors: Araya Valentino, Conforti Angelo, Duran Faustino, Patiño Ignacio.
"""

# 1. Convertir la Expresión Regular a un AFND mediante Algoritmo de Thompson

# Creamos la clase estado, cada estado tiene un estado final y transiciones
class Estado:
    def __init__(self, final=False):
        self.final = final        
        # Las transiciones de los estados son un diccionario donde la clave es el caracter y el valor es el estado al que transiciona
        self.transiciones = {}

# Creamos la clase AFND para poder crear los autómatas básicos y el autómata de cada operación
class AFND:
    def __init__(self):
        self.estadoInicial = Estado()
        self.estadoFinal = Estado(final=True)

# Función AFND básico
def afnd_basico(caracter):
    # Definimos los estados
    inicial = Estado()
    final = Estado(final=True)
    # Agregamos la transición con el caracter
    inicial.transiciones[caracter] = final
    # Instanciamos el AF básico del caracter
    afnd = AFND()
    afnd.estadoInicial = inicial
    afnd.estadoFinal = final
    return afnd

# Función Concatenación    
def concatenacion(afnd1, afnd2):
    # 1. El estado final del primer autómata deja de ser final
    afnd1.estadoFinal.final = False
    # 2. El estado inicial del segundo autómata deja de ser inicial y se unen con una transición Lambda
    afnd1.estadoFinal.transiciones["λ"] = afnd2.estadoInicial
    # 3. Definimos un nuevo AF
    newAfnd = AFND()
    newAfnd.estadoInicial = afnd1.estadoInicial
    newAfnd.estadoFinal = afnd2.estadoFinal
    return newAfnd

# Función Unión
def union(afnd1, afnd2):
    # 1. Se crea un nuevo estado inicial y un nuevo estado final
    inicial = Estado()
    final = Estado(final=True)
    # 2. Los estados inciales djean de ser iniciales y se añaden transiciones Lambda del nuevo estado inicial a los dos ex estados iniciales
    inicial.transiciones["λ"] = [afnd1.estadoInicial, afnd2.estadoInicial]
    # 3. Los estados finales djean de ser finales y se añaden transiciones Lambda de los ex estados finales al nuevo estado final
    afnd1.estadoFinal.final = False
    afnd2.estadoFinal.final = False
    afnd1.estadoFinal.transiciones["λ"] = final
    afnd2.estadoFinal.transiciones["λ"] = final
    
    # Definimos el nuevo AF
    newAfnd = AFND()
    newAfnd.estadoInicial = inicial
    newAfnd.estadoFinal = final
    return newAfnd

# Creamos la función algoritmo_thompson para armar el AFND final mediante las operaciones        
def algoritmo_thompson(expresionRegular):
    
    pilaAutomatas = []
    
    # Recorremos la expresión regular
    for i in range(len(expresionRegular)):
                
        # Creamos un AF básico para el primer caracter
        if i == 0 and expresionRegular[i] != "(":
            afnd = afnd_basico(expresionRegular[i])
            pilaAutomatas.append(afnd)
        
        # Caso de Concatenación
        elif expresionRegular[i] == "." and i != len(expresionRegular)-1 and expresionRegular[i+1] != "(":
            # Creamos AF básico del caracter siguiente a la concatenación        
            afnd2 = afnd_basico(expresionRegular[i+1])
            afnd1 = pilaAutomatas.pop()
            
            # Aplico concatenación
            newAfnd = concatenacion(afnd1, afnd2)
            
            # Agregamos a la pila
            pilaAutomatas.append(newAfnd)
            
        # Caso de Unión
        elif expresionRegular[i] == "|" and i != len(expresionRegular)-1 and expresionRegular[i+1] != "(":
            # Creamos AF básico del caracter siguiente a la unión
            afnd2 = afnd_basico(expresionRegular[i+1])
            afnd1 = pilaAutomatas.pop()
                      
            # Aplico unión
            newAfnd = union(afnd1, afnd2)  
            
            # Agrego a la pila
            pilaAutomatas.append(newAfnd)
            
        # ESTRELLA DE KLEENE TENDRÁ 2 LÓGICAS:
        #   1. Si es hacia un caracter -> Devolver AF
        #   2. Si es hacia una agrupación -> Resolver agrupación, devolver AF y luego aplicarle Estrella de Kleene
        
        # TRATAR LAS AGRUPACIONES APARTE Y CONTAR AGRUPACIONES
            
        print(pilaAutomatas)
        
        
            
algoritmo_thompson("a.b|c.")
            
            
   