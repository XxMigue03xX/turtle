def automata(transitions, start_state, final_states, input_string):
    current_state = start_state
    for symbol in input_string:
        current_state = transitions[current_state].get(symbol)
        if current_state is None:
            return False
    
    return current_state in final_states

# Definir transiciones del autómata
transitions = {
    'q0': {'0': 'q0', '1': 'q1'},
    'q1': {'0': 'q1', '1': 'q0'},
}

# Estado inicial
start_state = 'q0'

# Estados finales
final_states = {'q1'}

# Cadena de entrada
input_string = input("Ingresa una cadena para el automata de '1's impares: ")

# Ejecutar el autómata
if automata(transitions, start_state, final_states, input_string):
    print("Cadena aceptada")
else:
    print("Cadena no aceptada")