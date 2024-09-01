# Instalacion de librerias
# Estas son las librerias que se deben instalar para correr el programa
# pip install matplotlib
# pip install networkx
# pip install pillow

# las demas librerias usadas en el codigo, están instaladas por defecto con Python.

# Importar librerias
import math
import turtle
import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image
import tkinter as tk
from tkinter import ttk

imagen = Image.open("./assets/Fondo.gif")
ancho_imagen, alto_imagen = imagen.size

# Definir el alfabeto del automata
ALFABETO = ["arr", "abj", "izq", "der",
            "d-q", "d-e", "d-z", "d-c", "cu", "t", "r", "ci"]
# Direcciones diagonales (P es punto central):
# Q E
#  P
# Z C

# Definir funcion de transicion del autómata
F_TRANSICION = {
    'q0': {'cu': 'q1', 't': 'q9', 'r': 'q1', 'ci': 'q22'},
    'q1': {'der': 'q2', 'abj': 'q6'},
    'q2': {'abj': 'q3'},
    'q3': {'izq': 'q4'},
    'q4': {'arr': 'q5'},
    'q5': {},
    'q6': {'der': 'q7'},
    'q7': {'arr': 'q8'},
    'q8': {'izq': 'q5'},
    'q9': {'abj': 'q10', 'der':'q14', 'd-c': 'q18'},
    'q10': {'der': 'q11', 'd-e': 'q12'},
    'q11': {'d-q': 'q13'},
    'q12': {'izq': 'q13'},
    'q13': {},
    'q14': {'abj': 'q15', 'd-z': 'q16'},
    'q15': {'d-q': 'q17'},
    'q16': {'arr': 'q17'},
    'q17': {},
    'q18': {'arr': 'q19', 'izq': 'q20'},
    'q19': {'izq': 'q21'},
    'q20': {'arr': 'q21'},
    'q21': {},
    'q22': {'der': 'q23', 'izq': 'q23'},
    'q23': {}
}

# Definir estado inicial del automata
ESTADO_INICIAL = 'q0'

# Definir estados de aceptacion del automata
ESTADOS_ACEPTADOS = {'q5', 'q13', 'q17', 'q21', 'q23'}

# Definir ventana y tortuga
ventana = turtle.Screen()
ventana.title("Juego")
ventana.setup(width=ancho_imagen, height=alto_imagen) # Tamaño de imagen
ventana.cv.master.resizable(False, False) # Tamaño fijo
ventana.bgpic("./assets/Fondo.gif")
tortuga = turtle.Turtle()
tortuga.shape("turtle")

# Posición inicial
tortuga.penup() # Levantar laipz
tortuga.setpos(-140, 135) # Mover
tortuga.pendown() # Bajar lapiz

# Orientación inicial
tortuga.setheading(90)

# Definir valor de avance
FRONTAL = 275
DIAGONAL = math.sqrt((FRONTAL**2)*2)

# Definir las funciones de movimiento
def adelante(distancia):
    tortuga.forward(distancia)
def atras(distancia):
    tortuga.backward(distancia)
def izquierda(distancia):
    tortuga.setheading(180) # Girar
    tortuga.forward(distancia) # Avanzar
    tortuga.setheading(90) # Girar
def derecha(distancia):
    tortuga.setheading(0)
    tortuga.forward(distancia)
    tortuga.setheading(90)
def diagonal_q(distancia):
    tortuga.setheading(135)
    tortuga.forward(distancia)
    tortuga.setheading(90)
def diagonal_e(distancia):
    tortuga.setheading(45)
    tortuga.forward(distancia)
    tortuga.setheading(90)
def diagonal_z(distancia):
    tortuga.setheading(225)
    tortuga.forward(distancia)
    tortuga.setheading(90)
def diagonal_c(distancia):
    tortuga.setheading(315)
    tortuga.forward(distancia)
    tortuga.setheading(90)
def circulo_d(distancia):
    tortuga.setheading(0)
    tortuga.circle(-distancia) # Negativo para dirección de las manecillas del reloj
    tortuga.setheading(90)
def circulo_i(distancia):
    tortuga.setheading(180)
    tortuga.circle(distancia) # Positivo para la dirección contraria a las manecillas
    tortuga.setheading(90)


def validar_alfabeto(array_cadena, alfabeto):
    # Por palabra en cadena de entrada
    for palabra in array_cadena:
        # Si no pertenece al alfabeto
        if palabra.lower() not in alfabeto:
            # Retorna falso y la palabra errada
            return [False, palabra]
    # Si pertenece retorna verdadero
    return [True]

# Definir el automata
def automata(alfabeto, f_transicion, estado_inicial, estados_finales, array_cadena):
    pertenece = validar_alfabeto(array_cadena, alfabeto)[0]
    estados_visitados = []
    
    # Si la cadena no pertenece al alfabeto
    if not pertenece:
        # Mostrar mensaje de error y retornar falso
        palabra = validar_alfabeto(array_cadena, alfabeto)[1]
        print(f"La palabra '{palabra}' no pertenece al alfabeto")
        return False, estados_visitados

    # Si la cadena pertenece se empieza la ejecución del automata
    estado_actual = estado_inicial
    # Se guardan los estados visitados
    estados_visitados.append(estado_actual)  
    
    # Por palabra en la cadena de entrada
    for palabra in array_cadena:
        # Se cambia de estado segun la funcion de transicion para esa palabra
        estado_actual = f_transicion[estado_actual].get(palabra.lower())
        # Si no hay estado para esa palabra
        if estado_actual is None:
            # Se retorna falso, no pertenece al automata
            return False, estados_visitados
        # Si hay estado se añade a los visitados
        estados_visitados.append(estado_actual)  

    # Se retorna booleano de aceptacion y estados visitados
    return estado_actual in estados_finales, estados_visitados

def mostrar_tabla_transiciones(alfabeto, transiciones, estados_visitados):
    # Crear la ventana principal
    ventana_tabla = tk.Tk()
    ventana_tabla.title("Tabla de Transiciones del Autómata")

    # Definir estilo para la tabla
    estilo = ttk.Style()
    estilo.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
    estilo.configure("Treeview", rowheight=25, font=("Helvetica", 9))
    estilo.map('Treeview', background=[('selected', 'blue')], foreground=[('selected', 'white')])

    # Crear un árbol (treeview) para la tabla
    columnas = ['Estado'] + alfabeto
    tree = ttk.Treeview(ventana_tabla, columns=columnas, show='headings')

    # Definir los encabezados de las columnas
    for columna in columnas:
        tree.heading(columna, text=columna)
        tree.column(columna, width=100, anchor='center')

    # Llenar la tabla con las transiciones
    for idx, estado in enumerate(transiciones.keys()):
        fila = [estado]
        for simbolo in alfabeto:
            siguiente_estado = transiciones[estado].get(simbolo, '-')
            fila.append(siguiente_estado)
        
        # Alternar colores de las filas
        if estado in estados_visitados:
            tree.insert('', 'end', values=fila, tags=('highlighted',))
        elif idx % 2 == 0:
            tree.insert('', 'end', values=fila, tags=('evenrow',))
        else:
            tree.insert('', 'end', values=fila, tags=('oddrow',))
    
    # Estilo para filas alternas
    tree.tag_configure('highlighted', background='lightgreen')
    tree.tag_configure('evenrow', background='lightgrey')
    tree.tag_configure('oddrow', background='white')

    # Aplicar color verde a las celdas de los estados visitados
    def resaltar_estado_visitado(event):
        item = tree.identify_row(event.y)
        if item:
            row_values = tree.item(item, 'values')
            estado = row_values[0]
            if estado in estados_visitados:
                tree.tag_configure(item, background='lightgreen')
    
    tree.bind('<Motion>', resaltar_estado_visitado)

    # Empaquetar la tabla y mostrar la ventana
    tree.pack(expand=True, fill='both', padx=10, pady=10)

    # Activar redimensionamiento automático de las columnas
    for columna in columnas:
        tree.column(columna, stretch=tk.YES)

    ventana_tabla.mainloop()

# Definir movimiento asociado al alfabeto
def mover_tortuga(cadena):
    # Si rectangulo
    if cadena[0].lower() == "r":
        for palabra in cadena:
            if palabra.lower() == "arr":
                adelante(FRONTAL/2)
            elif palabra.lower() == "abj":
                atras(FRONTAL/2)
            elif palabra.lower() == "izq":
                izquierda(FRONTAL)
            elif palabra.lower() == "der":
                derecha(FRONTAL)
    # Si circulo
    elif cadena[0].lower() == "ci":
        tortuga.penup()
        tortuga.setpos(0, 135)
        tortuga.pendown()
        for palabra in cadena:
            if palabra.lower() == "der":
                circulo_d(FRONTAL/2)
            elif palabra.lower() == "izq":
                circulo_i(FRONTAL/2)
    # Cuadrado y triangulo
    else:
        for palabra in cadena:
            if palabra.lower() == "arr":
                adelante(FRONTAL)
            elif palabra.lower() == "abj":
                atras(FRONTAL)
            elif palabra.lower() == "izq":
                izquierda(FRONTAL)
            elif palabra.lower() == "der":
                derecha(FRONTAL)
            elif palabra.lower() == "d-q":
                diagonal_q(DIAGONAL)
            elif palabra.lower() == "d-e":
                diagonal_e(DIAGONAL)
            elif palabra.lower() == "d-z":
                diagonal_z(DIAGONAL)
            elif palabra.lower() == "d-c":
                diagonal_c(DIAGONAL)

# Solicitar cadena de entrada
cadena_entrada = ventana.textinput("AUTOMATA", "Ingresa una cadena para el automata tortuga: ")
# Convertir cadena en array de palabras
array_cadena = cadena_entrada.split(" ")

# Ejecutar el autómata
pertenece, estados_visitados = automata(ALFABETO, F_TRANSICION, ESTADO_INICIAL, ESTADOS_ACEPTADOS, array_cadena)

if pertenece:
    print("Pertenece al automata")
    # Mover tortuga si la cadena ha sido aceptada
    mover_tortuga(array_cadena)
    turtle.done()
else:
    print("No pertenece al automata")
    
# Crear un grafo multi dirigido
G = nx.MultiDiGraph()

# Agregar nodos (estados) y asignarles el atributo 'subset'
# Aquí, 'subset' define la capa a la que pertenece el nodo.
subset_map = {
    'q0': 0,
    'q1': 1,
    'q2': 2,
    'q3': 3,
    'q4': 4,
    'q5': 5,
    'q6': 2,
    'q7': 3,
    'q8': 4,
    'q9': 1,
    'q10': 2,
    'q11': 3,
    'q12': 3,
    'q13': 4,
    'q14': 2,
    'q15': 3,
    'q16': 3,
    'q17': 4,
    'q18': 2,
    'q19': 3,
    'q20': 3,
    'q21': 4,
    'q22': 1,
    'q23': 2
}

# Por cada estado de la f de transicion
for state in F_TRANSICION:
    # Se añade un nodo con su subset respectivo
    G.add_node(state, subset=subset_map[state])

# Agregar aristas (transiciones)
for from_state, transitions_dict in F_TRANSICION.items():
    for symbol, to_state in transitions_dict.items():
        if from_state == 'q0' and to_state == 'q1':
            continue
        else:
            if symbol != 'cuadrado' or 'rectangulo':
                G.add_edge(from_state, to_state, label=symbol)

# Agregar manualmente una arista curva para 'cuadrado, rectangulo' y 'circulo'
G.add_edge('q0', 'q1', label='r/cu', key='r/cu', connectionstyle="arc3,rad=0.5")
G.add_edge('q22', 'q23', label='izq/der', key='izq/der', connectionstyle="arc3,rad=0.5")
# Posicionar los nodos utilizando el layout multipartite
pos = nx.multipartite_layout(G, subset_key="subset")

# Dibujar el grafo
nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue', edgecolors='black')


# Dibujar la arista de "rectangulo" (arco por arriba)
nx.draw_networkx_edges(
    G, pos, edgelist=[(u, v) for u, v, d in G.edges(data=True) if d.get('label') == 'r/cu'],
    connectionstyle="arc3,rad=-0.5", arrowstyle='->', arrowsize=20, edge_color='gray'
)

# Dibujar la arista de "circulo" (arco por abajo)
nx.draw_networkx_edges(
    G, pos, edgelist=[(u, v) for u, v, d in G.edges(data=True) if d.get('label') == 'izq/der'],
    connectionstyle="arc3,rad=0.5", arrowstyle='->', arrowsize=20, edge_color='gray'
)

# Crear un diccionario de posiciones para las etiquetas
# Establecer una posición fija para la etiqueta 'cuadrado/rectangulo'
edge_labels = {('q0', 'q1'): 'r/cu'}
edge_labels.update({(u, v): f"{d['label']}" for u, v, d in G.edges(data=True) if (u, v) != ('q0', 'q1') and ('q22', 'q23')})

# Establecer una posición fija para la etiqueta 'circulo'
edge_labels = {('q22', 'q23'): 'der/izq'}
edge_labels.update({(u, v): f"{d['label']}" for u, v, d in G.edges(data=True) if (u, v) != ('q22', 'q23') and ('q22', 'q23')})

# Crear una copia de la posición para ajustar las etiquetas
pos_labels = pos.copy()

# Dibujar el resto de las aristas con estilo predeterminado
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray')

# Dibujar las etiquetas de las demás aristas de manera normal
edge_labels.update({(u, v): f"{d['label']}" for u, v, d in G.edges(data=True) if (u, v) != ('q0', 'q1') and ('q22', 'q23')})
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

# Resaltar estado inicial y estados de aceptación
nx.draw_networkx_nodes(G, pos, nodelist=[ESTADO_INICIAL], node_color='green', node_size=1200)
nx.draw_networkx_nodes(G, pos, nodelist=ESTADOS_ACEPTADOS, node_color='red', node_size=1200)

# Definir los estados visitados que no son ni el estado inicial ni los estados finales
nodos_visitados = [estado for estado in estados_visitados if estado != ESTADO_INICIAL and estado not in ESTADOS_ACEPTADOS]

# Definir el estado final de este automata
nodo_final = [estado for estado in ESTADOS_ACEPTADOS if estado in estados_visitados]

# Repintar nodos visitados en color naranja y estado de aceptación final de morado
nx.draw_networkx_nodes(G, pos, nodelist=nodos_visitados, node_color='orange', node_size=1300)
nx.draw_networkx_nodes(G, pos, nodelist=nodo_final, node_color='purple', node_size=1400)

# Dibujar etiquetas de los nodos
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif', font_weight='bold')

# Título del grafo
plt.title("Diagrama de Estados del Autómata", fontsize=15)

# Quitar los ejes
plt.axis('off')

# Mostrar grafo
plt.show()

# mostrar tabla de transiciones
mostrar_tabla_transiciones(ALFABETO, F_TRANSICION, estados_visitados)