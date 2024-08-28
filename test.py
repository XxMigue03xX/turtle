# Importar librerias
import math
import turtle
import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image
import tkinter as tk
from tkinter import ttk

# Obtener imagen y extraer su alto y ancho
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
ventana.setup(width=ancho_imagen, height=alto_imagen)
ventana.cv.master.resizable(False, False)
ventana.bgpic("./assets/Fondo.gif")
tortuga = turtle.Turtle()
tortuga.shape("turtle")

# Posición inicial
tortuga.penup() # Levantar lapiz
tortuga.setpos(-140, 135) # Coordenadas x, y
tortuga.pendown() # Bajar lapiz

# Orientación inicial
tortuga.setheading(90) # 0 = =>

# Definir valor de avance
FRONTAL = 275
DIAGONAL = math.sqrt((FRONTAL**2)*2) # Calculo por el teorema de pitagoras

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

# Funcion de validación de alfabeto
def validar_alfabeto(array_cadena, alfabeto):
    # Por cada palabra ingresada
    for palabra in array_cadena:
        # Ver si está en el alfabeto
        if palabra.lower() not in alfabeto:
            # Si no está, retornar falso y la palabra erronea
            return [False, palabra]
    # Si si está, retornar true
    return [True]

# Definir el automata
def automata(alfabeto, f_transicion, estado_inicial, estados_finales, array_cadena):
    # Verificar si la cadena ingresada pertenece al alfabeto
    pertenece = validar_alfabeto(array_cadena, alfabeto)[0]
    if (not pertenece):
        # Si no pertenece emitir un mensaje de error y retornar falso
        palabra = validar_alfabeto(array_cadena, alfabeto)[1]
        print(f"La palabra '{palabra}' no pertenece al alfabeto")
        return False
    # Si si pertenece empieza el recorrido en estado inicial
    estado_actual = estado_inicial
    # Por cada palabra ingresada
    for palabra in array_cadena:
        # Cambiar de estado segun la funcion de transición
        estado_actual = f_transicion[estado_actual].get(palabra.lower())
        # Si lo ingresado no está en la funcion de transicion
        if estado_actual is None:
            # Retornar falso porque no pertenece
            return False
    # Retrornar booleano de pertencia del estado final en los estados de aceptación
    return estado_actual in estados_finales

# Funcion para mostrar la tabla de la funcion de transicion
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
# Convertir cadena de entrada a array de palabras
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
# G = nx.MultiDiGraph()

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
nx.draw_networkx_nodes(G, pos, nodelist=[ESTADO_INICIAL], node_color='green', node_size=1200)
nx.draw_networkx_nodes(G, pos, nodelist=ESTADOS_ACEPTADOS, node_color='red', node_size=1200)

# Título del grafo
plt.title("Diagrama de Estados del Autómata", fontsize=15)

# Quitar los ejes
plt.axis('off')

# Mostrar grafo
plt.show()

# Mostrar tabla de transiciones
mostrar_tabla_transiciones(ALFABETO, F_TRANSICION)