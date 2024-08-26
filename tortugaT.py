# Importar libreria tk
# pip install tk
import math
import turtle
from PIL import Image

imagen = Image.open("./assets/Fondo.gif")
ancho_imagen, alto_imagen = imagen.size

# Definir el alfabeto del automata
ALFABETO = ["arriba", "abajo", "izquierda", "derecha",
            "diagonal-q", "diagonal-e", "diagonal-z", "diagonal-c"]

# Direcciones diagonales (P es punto central):
# Q E
#  P
# Z C

# Definir funcion de transicion del autómata
F_TRANSICION = {
    'q0': {'derecha': 'q1', 'diagonal-c': 'q4'},
    'q1': {'abajo': 'q2'},
    'q2': {'diagonal-q': 'q3'},
    'q3': {},
    'q4': {'arriba': 'q5'},
    'q5': {'izquierda': 'q3'},
}

# Definir estado inicial del automata
ESTADO_INICIAL = 'q0'

# Definir estados de aceptacion del automata
ESTADOS_ACEPTADOS = {'q3'}

# Definir valor de avance
FRONTAL = 250
DIAGONAL = FRONTAL**2

# Definir ventana y tortuga
ventana = turtle.Screen()
ventana.title("Juego")
ventana.bgcolor("white")
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

# Definir las funciones de movimiento
def adelante():
    tortuga.forward(100)
def atras():
    tortuga.backward(100)
def izquierda():
    tortuga.setheading(180)
    tortuga.forward(100)
    tortuga.setheading(90)
def derecha():
    tortuga.setheading(0)
    tortuga.forward(100)
    tortuga.setheading(90)
def diagonal_q():
    tortuga.setheading(135)
    tortuga.forward(math.sqrt(20000))
    tortuga.setheading(90)
def diagonal_e():
    tortuga.setheading(45)
    tortuga.forward(math.sqrt(20000))
    tortuga.setheading(90)
def diagonal_z():
    tortuga.setheading(225)
    tortuga.forward(math.sqrt(20000))
    tortuga.setheading(90)
def diagonal_c():
    tortuga.setheading(315)
    tortuga.forward(math.sqrt(20000))
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