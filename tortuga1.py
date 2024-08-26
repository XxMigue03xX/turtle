# instalar libreria tk
# Con pip install tk o con sudo apt install python3-tk
import turtle
# Configuración de la ventana
ventana = turtle.Screen()
ventana.title("Juego")
ventana.bgcolor("white")
ventana.setup(width=600, height=600)

# Creación de la tortuga
tortuga = turtle.Turtle()
tortuga.shape("turtle")
tortuga.color("black")
tortuga.speed(1)

# Movimientos básicos para la tortuga
def mover_adelante():
    tortuga.forward(50)

def girar_izquierda():
    tortuga.left(90)

def girar_derecha():
    tortuga.right(90)

# Asignación de comandos
ventana.listen()
ventana.onkey(mover_adelante, "w")    # Adelante con 'w'
ventana.onkey(girar_izquierda, "a")    # Girar a la izquierda con 'a'
ventana.onkey(girar_derecha, "d")      # Girar a la derecha con 'd'

# Ciclo principal
ventana.mainloop()