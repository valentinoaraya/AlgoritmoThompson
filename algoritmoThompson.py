"""
Primer Proyecto - Trabajo Especial - "Algoritmo de Thompson"
@authors: Araya Valentino, Conforti Angelo, Duran Faustino, Patiño Ignacio.
"""
from graphviz import Digraph

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

# Función Estrella de Kleene
def estrellaKleene(afnd):
    # 1. El estado inicial deja de ser inicial y el final deja de ser final y se crea un nuevo estado inicial y un nuevo estado final
    inicial = Estado()
    final = Estado(final=True)
    afnd.estadoFinal.final = False
    # 2. Se agregan transiciones Lambda desde el nuevo estado inicial a el ex estado inicial y al nuevo estado final
    inicial.transiciones["λ"] = [afnd.estadoInicial, final]
    # 3. Se agregan transiciones Lambda desde el ex estado final hacia el nuevo estado final y hacia el ex estado inicial
    afnd.estadoFinal.transiciones["λ"] = [afnd.estadoInicial, final]
    newAfnd = AFND()
    newAfnd.estadoInicial = inicial
    newAfnd.estadoFinal = final
    return newAfnd

# Creamos la función algoritmo_thompson para armar el AFND final mediante las operaciones        
def algoritmo_thompson(expresionRegular):
    
    pilaAutomatas = []
    
    # Manejo de las Estrellas de Kleene
    pilaEstrellasKleene =[]  # Array para guardar los autómatas creados con Estrellas de Kleene   
    nuevaExpresionRegular = "" # Creamos una nueva expresión regular reemplazando el caracter afectado por una estrella de Kleene por un "@"
    nuevaExpresionRegularDefinitiva = "" # Esta variable guarda la ER sin los "*" para que luego pueda ser bien manejada
    contadorArrobas = 0 # Cuento los @ en la ER definitiva para luego buscarlos por índices en la lista "pilaEstrellasKleene"
    
    if "*" in expresionRegular: # Si existe una Estrella de Kleene en la expresión...
        for i in range(len(expresionRegular)):
            if expresionRegular[i] == "*" and expresionRegular[i-1] != ")":
                afndBasico = afnd_basico(expresionRegular[i-1])
                afndFinal = estrellaKleene(afndBasico)
                pilaEstrellasKleene.append(afndFinal)
                
        for i in range(len(expresionRegular)):    
            if i != len(expresionRegular)-1 and expresionRegular[i+1] != "*":
                nuevaExpresionRegular += expresionRegular[i]
            elif i != len(expresionRegular)-1 and expresionRegular[i+1] == "*":
                nuevaExpresionRegular += "@"
            elif i == len(expresionRegular)-1:
                nuevaExpresionRegular += expresionRegular[i]            
        
        nuevaExpresionRegularDefinitiva = nuevaExpresionRegular.replace("*", "")            

    if nuevaExpresionRegularDefinitiva == "":
        nuevaExpresionRegularDefinitiva = expresionRegular    
                
    # Recorremos la expresión regular
    for i in range(len(nuevaExpresionRegularDefinitiva)):
                
        # Creamos un AF básico para el primer caracter
        if i == 0 and nuevaExpresionRegularDefinitiva[i] != "(":
            if nuevaExpresionRegularDefinitiva[i] != "@":
                afnd = afnd_basico(nuevaExpresionRegularDefinitiva[i])
                pilaAutomatas.append(afnd)
            else:
                afndEstrellaKleene = pilaEstrellasKleene[contadorArrobas]
                pilaAutomatas.append(afndEstrellaKleene)
                contadorArrobas+=1        
        # Caso de Concatenación
        elif nuevaExpresionRegularDefinitiva[i] == "." and i != len(nuevaExpresionRegularDefinitiva)-1 and nuevaExpresionRegularDefinitiva[i+1] != "(":
            if nuevaExpresionRegularDefinitiva[i+1] == "@":
                afndEstrellaKleene = pilaEstrellasKleene[contadorArrobas]
                afnd1 = pilaAutomatas.pop()
                newAfnd = concatenacion(afnd1, afndEstrellaKleene)
                pilaAutomatas.append(newAfnd)
                contadorArrobas += 1
            else:
                # Creamos AF básico del caracter siguiente a la concatenación        
                afnd2 = afnd_basico(nuevaExpresionRegularDefinitiva[i+1])
                afnd1 = pilaAutomatas.pop()
            
                # Aplico concatenación
                newAfnd = concatenacion(afnd1, afnd2)
        
                # Agregamos a la pila
                pilaAutomatas.append(newAfnd)
            
        # Caso de Unión
        elif nuevaExpresionRegularDefinitiva[i] == "|" and i != len(nuevaExpresionRegularDefinitiva)-1 and nuevaExpresionRegularDefinitiva[i+1] != "(":
            if nuevaExpresionRegularDefinitiva[i+1] == "@":
                afndEstrellaKleene = pilaEstrellasKleene[contadorArrobas]
                afnd1 = pilaAutomatas.pop()
                newAfnd = union(afnd1, afndEstrellaKleene)
                pilaAutomatas.append(newAfnd)
                contadorArrobas += 1
            else:
                
                # Creamos AF básico del caracter siguiente a la unión
                afnd2 = afnd_basico(nuevaExpresionRegularDefinitiva[i+1])
                afnd1 = pilaAutomatas.pop()

                # Aplico unión
                newAfnd = union(afnd1, afnd2)  
            
                # Agrego a la pila
                pilaAutomatas.append(newAfnd)
            
    return pilaAutomatas.pop()

# Visualizar el Autómata

def visualize_nfa(afnd):
    dot = Digraph()
    
    def add_state(estado, estadosAgregados):
        if estado not in estadosAgregados:
            estadosAgregados.add(estado)
            for caracter, estadoSiguiente in estado.transiciones.items():
                if isinstance(estadoSiguiente, list):
                    for ns in estadoSiguiente:
                        dot.edge(str(id(estado)), str(id(ns)), label=caracter)
                        add_state(ns, estadosAgregados)
                else:
                    dot.edge(str(id(estado)), str(id(estadoSiguiente)), label=caracter)
                    add_state(estadoSiguiente, estadosAgregados)
            if estado.final:
                dot.node(str(id(estado)), shape='doublecircle')
            else:
                dot.node(str(id(estado)))
    
    add_state(afnd.estadoInicial, set())
    dot.render('afnd', format='png', view=True)

# Ejemplo de uso:
regex = "c*.a|b"
nfa = algoritmo_thompson(regex)
visualize_nfa(nfa)