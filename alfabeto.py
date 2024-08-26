cadena_entrada = input("Ingresa una cadena para el automata tortuga: ")
array_cadena = cadena_entrada.split(" ")
Alfabeto = ["arriba", "abajo", "izquierda", "derecha"]

def validar_alfabeto(array_cadena, ALfabeto):
    for palabra in array_cadena:
        if palabra.lower() not in ALfabeto:
            return [False, palabra]
    return [True]

pertenece = validar_alfabeto(array_cadena, Alfabeto)[0]

if(pertenece):
    print(f"La cadena '{cadena_entrada}' pertenece al alfabeto")
else:
    palabra = validar_alfabeto(array_cadena, Alfabeto)[1]
    print(f"La palabra '{palabra}' no pertenece al alfabeto")
    
F_TRANSICION = {
    'q0': {'derecha': 'q1'},
    'q1': {'izquierda': 'q0', 'abajo': 'q2'},
    'q2': {'izquierda': 'q3', 'arriba': 'q1'},
    'q3': {'arriba': 'q4', 'derecha': 'q2'},
    'q4': {}
}