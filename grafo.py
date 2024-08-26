import matplotlib.pyplot as plt
import networkx as nx

def automata(transitions, start_state, final_states, input_string):
    current_state = start_state
    for symbol in input_string:
        current_state = transitions[current_state].get(symbol)
        if current_state is None:
            return False
    
    return current_state in final_states

# Definir transiciones del autómata
F_TRANSICION = {
    'q0': {'0': 'q0', '1': 'q1'},
    'q1': {'0': 'q1', '1': 'q0'},
}

# Estado inicial
ESTADO_INICIAL = 'q0'

# Estados finales
ESTADOS_ACEPTADOS = {'q1'}

# Cadena de entrada
input_string = input("Ingresa una cadena para el automata de '1's impares: ")

# Ejecutar el autómata
if automata(F_TRANSICION, ESTADO_INICIAL, ESTADOS_ACEPTADOS, input_string):
    print("Cadena aceptada")
else:
    print("Cadena no aceptada")

# Crear un grafo dirigido
G = nx.DiGraph()

# Agregar nodos (estados)
for state in F_TRANSICION:
    G.add_node(state)

# Agregar aristas (transiciones)
for from_state, transitions_dict in F_TRANSICION.items():
    for symbol, to_state in transitions_dict.items():
        G.add_edge(from_state, to_state, label=symbol)

# Establecer el estado inicial y final
pos = nx.spring_layout(G)  # Posicionamiento de los nodos
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
nx.draw_networkx_edges(G, pos, arrowstyle='->')
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))

# Resaltar estado inicial y final
nx.draw_networkx_nodes(G, pos, nodelist=[ESTADO_INICIAL], node_color='green', node_size=700)
nx.draw_networkx_nodes(G, pos, nodelist=ESTADOS_ACEPTADOS, node_color='red', node_size=700)

plt.axis('off')
plt.show()