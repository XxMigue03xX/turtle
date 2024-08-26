import turtle

#Alfabeto
# T(Avanzar) F(Izquierda) G (Retroceder) H (Derecha)
# [0,1,2,3,4,5,6,7,8,9]

# 1. Delimitar escenario (si se sale que avise o que sea ilimitado)
# 2. Logica de estados
# 3. Estados de aceptación
# 4. Grafica estetica

#Estados

#Estado incial

#Estados de aceptación

#Función de transición

# Crear la ventana y la tortuga
ventana = turtle.Screen()
ventana.title("Juego")
ventana.bgcolor("white")
ventana.setup(width=600, height=600)
tortuga = turtle.Turtle()
tortuga.shape("turtle")

# Definir las funciones de movimiento
def adelante():
  tortuga.forward(20)

def atras():
  tortuga.backward(20)

def izquierda():
  tortuga.left(90)

def derecha():
  tortuga.right(90)

# Definir la función para leer el texto y mover la tortuga
def mover_tortuga(texto):
  for caracter in texto:
    if caracter == "t" or caracter == "T":
      adelante()
    elif caracter == "g" or caracter == "G":
      atras()
    elif caracter == "f" or caracter == "F":
      izquierda()
    elif caracter == "h" or caracter == "H":
      derecha()

# Leer el texto y mover la tortuga
texto = input("Ingrese el texto para mover la tortuga: ")
mover_tortuga(texto)

# Mantener la ventana abierta
turtle.done()