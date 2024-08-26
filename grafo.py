import networkx as nx
import matplotlib.pyplot as plt

def automata(transitions, start_state, final_states, input_string):
    current_state = start_state
    for symbol in input_string:
        current_state = transitions[current_state].get(symbol)
        if current_state is None:
            return False
    
    return [current_state in final_states]

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

# Crear un grafo dirigido
G = nx.DiGraph()

# Agregar nodos (estados)
for state in transitions:
    G.add_node(state)

# Agregar aristas (transiciones)
for from_state, transitions_dict in transitions.items():
    for symbol, to_state in transitions_dict.items():
        G.add_edge(from_state, to_state, label=symbol)

# Ejecutar el autómata y obtener el estado final
final_state = automata(transitions, start_state, final_states, input_string)

# Establecer el diseño del grafo
pos = nx.spring_layout(G)  # Posicionamiento de los nodos

# Dibujar nodos con colores diferenciados
node_colors = ['lightblue' if state not in final_states else 'red' for state in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors)

# Dibujar aristas y etiquetas
nx.draw_networkx_edges(G, pos, arrowstyle='->')
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))

# Resaltar estado inicial en verde
nx.draw_networkx_nodes(G, pos, nodelist=[start_state], node_color='green', node_size=700)

# Resaltar estado final en azul (si corresponde)
if final_state in G.nodes():
    nx.draw_networkx_nodes(G, pos, nodelist=[final_state], node_color='blue', node_size=700)

plt.axis('off')
plt.show()