import sys
import networkx as nx
import random
import matplotlib.pyplot as plt


def maxSet(graph, nodes):

    if graph.number_of_edges() == 0:
        return set(graph.nodes)

    node = list(graph.nodes)[0]
    while graph.degree[node] == 0:
        index = random.randint(0, len(nodes) - 1)
        node = list(graph.nodes)[index]

    neighbors = set(graph[node].keys())
    graph.remove_node(node)

    set1 = maxSet(graph, nodes - {node})
    graph.remove_nodes_from(neighbors)
    set2 = maxSet(graph, nodes - {node} - set(neighbors))
    set2.add(node)
    return set1 if len(set1) > len(set2) else set2


if __name__ == '__main__':
    graph = nx.Graph()
    graph.add_edge(0, 4)
    graph.add_edge(0, 3)
    graph.add_edge(1, 4)
    graph.add_edge(2, 3)
    graph.add_edge(3, 5)

    plt.subplot(121)
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()
    listOfNodes = set(graph.nodes)
    print(maxSet(graph, listOfNodes))


