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
ALFABETO = ["arriba", "abajo", "izquierda", "derecha",
            "diagonal-q", "diagonal-e", "diagonal-z", "diagonal-c", "cuadrado", "triangulo"]

# Direcciones diagonales (P es punto central):
# Q E
#  P
# Z C

# Definir funcion de transicion del autómata
F_TRANSICION = {
    'q0': {'cuadrado': 'q1', 'triangulo': 'q9'},
    'q1': {'derecha': 'q2', 'abajo': 'q6'},
    'q2': {'abajo': 'q3'},
    'q3': {'izquierda': 'q4'},
    'q4': {'arriba': 'q5'},
    'q5': {},
    'q6': {'derecha': 'q7'},
    'q7': {'arriba': 'q8'},
    'q8': {'izquierda': 'q5'},
    'q9': {'derecha': 'q10', 'diagonal-c': 'q13'},
    'q10': {'abajo': 'q11'},
    'q11': {'diagonal-q': 'q12'},
    'q12': {},
    'q13': {'arriba': 'q14'},
    'q14': {'izquierda': 'q12'},
}


# Definir estado inicial del automata
ESTADO_INICIAL = 'q0'

# Definir estados de aceptacion del automata
ESTADOS_ACEPTADOS = {'q5', 'q12'}

# Definir ventana y tortuga
ventana = turtle.Screen()
ventana.title("Juego")
ventana.setup(width=ancho_imagen, height=alto_imagen)
ventana.cv.master.resizable(False, False)
ventana.bgpic("./assets/Fondo.gif")
tortuga = turtle.Turtle()
tortuga.shape("turtle")

# Posición inicial
tortuga.penup()
tortuga.setpos(-140, 135)
tortuga.pendown()

# Orientación inicial
tortuga.setheading(90)

# Definir valor de avance
FRONTAL = 275
DIAGONAL = math.sqrt((FRONTAL**2)*2)

# Definir las funciones de movimiento
def adelante():
    tortuga.forward(FRONTAL)
def atras():
    tortuga.backward(FRONTAL)
def izquierda():
    tortuga.setheading(180)
    tortuga.forward(FRONTAL)
    tortuga.setheading(90)
def derecha():
    tortuga.setheading(0)
    tortuga.forward(FRONTAL)
    tortuga.setheading(90)
def diagonal_q():
    tortuga.setheading(135)
    tortuga.forward(DIAGONAL)
    tortuga.setheading(90)
def diagonal_e():
    tortuga.setheading(45)
    tortuga.forward(DIAGONAL)
    tortuga.setheading(90)
def diagonal_z():
    tortuga.setheading(225)
    tortuga.forward(DIAGONAL)
    tortuga.setheading(90)
def diagonal_c():
    tortuga.setheading(315)
    tortuga.forward(DIAGONAL)
    tortuga.setheading(90)

def validar_alfabeto(array_cadena, ALfabeto):
    for palabra in array_cadena:
        if palabra.lower() not in ALfabeto:
            return [False, palabra]
    return [True]

# Definir el automata
def automata(alfabeto, f_transicion, estado_inicial, estados_finales, array_cadena):
    pertenece = validar_alfabeto(array_cadena, alfabeto)[0]
    if (not pertenece):
        palabra = validar_alfabeto(array_cadena, alfabeto)[1]
        print(f"La palabra '{palabra}' no pertenece al alfabeto")
        return False
    estado_actual = estado_inicial
    for palabra in array_cadena:
        estado_actual = f_transicion[estado_actual].get(palabra.lower())
        if estado_actual is None:
            return False

    return estado_actual in estados_finales

def mostrar_tabla_transiciones(alfabeto, transiciones):
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
        tree.column(columna, width=100, anchor='center')  # Ajustar ancho y alineación

    # Llenar la tabla con las transiciones
    for idx, estado in enumerate(transiciones.keys()):
        fila = [estado]
        for simbolo in alfabeto:
            siguiente_estado = transiciones[estado].get(simbolo, '-')
            fila.append(siguiente_estado)
        
        # Alternar colores de las filas
        if idx % 2 == 0:
            tree.insert('', 'end', values=fila, tags=('evenrow',))
        else:
            tree.insert('', 'end', values=fila, tags=('oddrow',))
    
    # Estilo para filas alternas
    tree.tag_configure('evenrow', background='lightgrey')
    tree.tag_configure('oddrow', background='white')

    # Empaquetar la tabla y mostrar la ventana
    tree.pack(expand=True, fill='both', padx=10, pady=10)

    # Activar redimensionamiento automático de las columnas
    for columna in columnas:
        tree.column(columna, stretch=tk.YES)

    ventana_tabla.mainloop()

# Definir movimiento asociado al alfabeto
def mover_tortuga(cadena):
    for palabra in cadena:
        if palabra.lower() == "arriba":
            adelante()
        elif palabra.lower() == "abajo":
            atras()
        elif palabra.lower() == "izquierda":
            izquierda()
        elif palabra.lower() == "derecha":
            derecha()
        elif palabra.lower() == "diagonal-q":
            diagonal_q()
        elif palabra.lower() == "diagonal-e":
            diagonal_e()
        elif palabra.lower() == "diagonal-z":
            diagonal_z()
        elif palabra.lower() == "diagonal-c":
            diagonal_c()


# Solicitar cadena de entrada
cadena_entrada = input("Ingresa una cadena para el automata tortuga: ")
array_cadena = cadena_entrada.split(" ")

# Ejecutar el autómata
if automata(ALFABETO, F_TRANSICION, ESTADO_INICIAL, ESTADOS_ACEPTADOS, array_cadena):
    print("Pertenece")
    # Mover tortuga si la cadena ha sido aceptada
    mover_tortuga(array_cadena)
    turtle.done()
else:
    print("No pertenece")
    
# Crear un grafo dirigido
G = nx.DiGraph()

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
    'q12': 5,
    'q13': 3,
    'q14': 4
}

for state in F_TRANSICION:
    G.add_node(state, subset=subset_map[state])

# Agregar aristas (transiciones)
for from_state, transitions_dict in F_TRANSICION.items():
    for symbol, to_state in transitions_dict.items():
        G.add_edge(from_state, to_state, label=symbol)

# Posicionar los nodos utilizando el layout multipartite
pos = nx.multipartite_layout(G, subset_key="subset")

# Dibujar el grafo
nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue', edgecolors='black')
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray')
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif', font_weight='bold')

# Dibujar etiquetas de las aristas
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

# Resaltar estado inicial y estados de aceptación
estado_inicial = 'q0'
estados_finales = {'q5', 'q12'}
nx.draw_networkx_nodes(G, pos, nodelist=[estado_inicial], node_color='green', node_size=1200)
nx.draw_networkx_nodes(G, pos, nodelist=estados_finales, node_color='red', node_size=1200)

# Título del grafo
plt.title("Diagrama de Estados del Autómata", fontsize=15)

# Quitar los ejes
plt.axis('off')

# Mostrar grafo
plt.show()

# mostrar tabla de transiciones
mostrar_tabla_transiciones(ALFABETO, F_TRANSICION)