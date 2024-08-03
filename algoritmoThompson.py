"""
Primer Proyecto - Trabajo Especial - "Algoritmo de Thompson"
@authors: Araya Valentino, Conforti Angelo, Duran Faustino, Patiño Ignacio.
"""
# La biblioteca Graphviz nos ayuda a visualizar los gráficos
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
    
    pilaAgrupaciones = [] # Pila para guardar los AF de las agrupaciones resueltas
    nuevaERConAmpersands = "" # Expresión pero reemplazando las agrupaciones por "&"
    contadorAmpersands = 0 # Cuento los "&" en la ER definitiva para luego buscarlos por índices en la lista "pilaAgrupaciones"
    agrupacion = "" # Aquí vamos a ir guardando los caracteres que estén dentro de una agrupación
    inicioAgrupacion = 100 # Definimos un número grande para que empiece a tomar la agrupación a partir del primer "("
    
    # Recorremos la expresión regular para obtener las agrupaciones
    for i in range(len(expresionRegular)):
        
        if expresionRegular[i] != "(" and i < inicioAgrupacion: 
            # Si estamos fuera de una agrupación agregamos el caracter a la neuva expresión
            nuevaERConAmpersands += expresionRegular[i]
            
        if expresionRegular[i] == "(":
            # Si encontramos el inicio de la agrupación asignamos el índice a la variable
            inicioAgrupacion = i
    
        if i > inicioAgrupacion and expresionRegular[i] != ")":
            # Si estamos dentro de la agrupación agregamos el caracter a la variable "agrupación"
            agrupacion += expresionRegular[i]
            
        elif expresionRegular[i] == ")":
            # Si encontramos el cierre de la agrupación, le aplicamos el algoritmo de thompson y obtenemos un AFND de esta expresión 
            afndAgrupacion = algoritmo_thompson(agrupacion)
            # Se agrega a la pila de agrupaciones
            pilaAgrupaciones.append(afndAgrupacion)
            # Y en la nueva expresión se agrega un "&" haciendo referencia a la agrupación
            nuevaERConAmpersands += "&"
            # Cuando se termina de procesar una agrupación, se vuelve a inicializar la variable "agrupación" e "inicioAgrupacion" a sus valores iniciales
            agrupacion = ""
            inicioAgrupacion = 100 
    
    # Manejo de las Estrellas de Kleene
    pilaEstrellasKleene =[]  # Lista para guardar los autómatas creados con Estrellas de Kleene   
    nuevaExpresionRegular = "" # Creamos una nueva expresión regular reemplazando el caracter afectado por una estrella de Kleene por un "@"
    nuevaExpresionRegularDefinitiva = "" # Esta variable guarda la ER sin los "*" para que luego pueda ser bien manejada
    contadorArrobas = 0 # Cuento los @ en la ER definitiva para luego buscarlos por índices en la lista "pilaEstrellasKleene"
    
    if "*" in nuevaERConAmpersands: # Si existe una Estrella de Kleene en la expresión...
        # Recorremos la nueva expresión con las agrupaciones reemplazadas por "&"
        for i in range(len(nuevaERConAmpersands)):
            # Si estamos en una Estrella de Kleene, y el caracter anterior no es una agrupación (es un caracter)
            if nuevaERConAmpersands[i] == "*" and nuevaERConAmpersands[i-1] != "&":
                # Obtenemos el AF básico y le aplicamos la Estrella de Kleene
                afndBasico = afnd_basico(nuevaERConAmpersands[i-1])
                afndFinal = estrellaKleene(afndBasico)
                # Agregamos el AFND final a la pila de estrellas de kleene
                pilaEstrellasKleene.append(afndFinal)
                
            # Si el caracter anterior a la estrella de kleene es un "&" (agrupación)
            elif nuevaERConAmpersands[i] == "*" and nuevaERConAmpersands[i-1] == "&":
                # Buscamos la agrupación en la pila de agrupaciones y le aplicamos la estrella de kleene
                afndAgrupacion = pilaAgrupaciones[contadorAmpersands]
                afndFinal = estrellaKleene(afndAgrupacion)
                # Agregamos el AFND final a la pila de estrellas de kleene
                pilaEstrellasKleene.append(afndFinal)
                # Sumamos 1 al contador
                contadorAmpersands += 1
                
        # Volvemos a recorrer y reemplazamos por "@" a lo que le aplicamos Estrellas de Kleene
        for i in range(len(nuevaERConAmpersands)):
            if i != len(nuevaERConAmpersands)-1 and nuevaERConAmpersands[i+1] != "*":
                nuevaExpresionRegular += nuevaERConAmpersands[i]
            elif i != len(nuevaERConAmpersands)-1 and nuevaERConAmpersands[i+1] == "*":
                nuevaExpresionRegular += "@"
            elif i == len(nuevaERConAmpersands)-1:
                nuevaExpresionRegular += nuevaERConAmpersands[i]            
        
        # Quitamos los "*" de la ER
        nuevaExpresionRegularDefinitiva = nuevaExpresionRegular.replace("*", "")            

    if nuevaExpresionRegularDefinitiva == "":
        nuevaExpresionRegularDefinitiva = nuevaERConAmpersands
                
    # Recorremos la expresión regular
    for i in range(len(nuevaExpresionRegularDefinitiva)):
                
        # Creamos un AF básico para el primer caracter
        if i == 0 and nuevaExpresionRegularDefinitiva[i] != "&":
            
            # Si el primer caracter no es una agrupación "&" ni una estrella de kleene "@"
            if nuevaExpresionRegularDefinitiva[i] != "@":
                afnd = afnd_basico(nuevaExpresionRegularDefinitiva[i])
                pilaAutomatas.append(afnd)
            
            # Si el caracter es una estrella de kleene "@"
            else:
                afndEstrellaKleene = pilaEstrellasKleene[contadorArrobas]
                pilaAutomatas.append(afndEstrellaKleene)
                contadorArrobas+=1
                
        # Si el caracter es una agrupación
        elif i == 0 and nuevaExpresionRegularDefinitiva[i] == "&":
            afndAgrupacion = pilaAgrupaciones[contadorAmpersands]
            pilaAutomatas.append(afndAgrupacion)
            contadorAmpersands += 1
            
        # Caso de Concatenación
        # Si econtramos una concatenación "." y el caracter siguiente a ésta, no es una agrupación "@"
        elif nuevaExpresionRegularDefinitiva[i] == "." and i != len(nuevaExpresionRegularDefinitiva)-1 and nuevaExpresionRegularDefinitiva[i+1] != "&":
            # Si el caracter siguiente a la concatenación es una Estrella de Kleene
            if nuevaExpresionRegularDefinitiva[i+1] == "@":
                afndEstrellaKleene = pilaEstrellasKleene[contadorArrobas]
                afnd1 = pilaAutomatas.pop()
                newAfnd = concatenacion(afnd1, afndEstrellaKleene)
                pilaAutomatas.append(newAfnd)
                contadorArrobas += 1
                
            # Si no es una estrella de Kleene (será otro caracter)
            else:
                # Creamos AF básico del caracter siguiente a la concatenación        
                afnd2 = afnd_basico(nuevaExpresionRegularDefinitiva[i+1])
                afnd1 = pilaAutomatas.pop()
            
                # Aplico concatenación
                newAfnd = concatenacion(afnd1, afnd2)
        
                # Agregamos a la pila
                pilaAutomatas.append(newAfnd)
            
        # Si econtramos una concatenación "." y el caracter siguiente a ésta, es una agrupación "@"
        elif nuevaExpresionRegularDefinitiva[i] == "." and i != len(nuevaExpresionRegularDefinitiva)-1 and nuevaExpresionRegularDefinitiva[i+1] == "&":
            afndAgrupacion = pilaAgrupaciones[contadorAmpersands]
            afnd1 = pilaAutomatas.pop()
            newAfnd = concatenacion(afnd1, afndAgrupacion)
            pilaAutomatas.append(newAfnd)
            contadorAmpersands += 1
            
        # Caso de Unión
        elif nuevaExpresionRegularDefinitiva[i] == "|" and i != len(nuevaExpresionRegularDefinitiva)-1 and nuevaExpresionRegularDefinitiva[i+1] != "&":
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
        elif nuevaExpresionRegularDefinitiva[i] == "|" and i != len(nuevaExpresionRegularDefinitiva)-1 and nuevaExpresionRegularDefinitiva[i+1] == "&":
            afndAgrupacion = pilaAgrupaciones[contadorAmpersands]
            afnd1 = pilaAutomatas.pop()
            newAfnd = union(afnd1, afndAgrupacion)
            pilaAutomatas.append(newAfnd)
            contadorAmpersands += 1
            
    return pilaAutomatas.pop()

# Visualizar el Autómata
def graficarAutomata(afnd):
    # Este objeto representa el grafo del autómata
    dot = Digraph()
    
    # Esta función agrega estados y transiciones al grafo
    def add_state(estado, estadosAgregados):
        # Agregamos el estado si no está
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
expresionRegular = "a.(a|b)*"
afnd = algoritmo_thompson(expresionRegular)
graficarAutomata(afnd)
