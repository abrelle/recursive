import sys
import networkx as nx
import random
import matplotlib.pyplot as plt
import timeit


def getGraphFromFile(fileName):
    graph = nx.Graph()

    with open(fileName) as f:
        for line in f:
            edge = []
            for word in line.split():
                edge.append(int(word))
            graph.add_edge(edge[0], edge[1])
            del edge[:]
    return graph


def writeGraph(graph, maxSet):
    f = open("results.txt", "w")
    f.write("List of edges:\n")
    for edge in graph.edges:
        stringEdges = "( " + str(edge[0]) + " - " + str(edge[1]) + " ), "
        f.write(stringEdges)

    f.write("\nNumber of nodes in maximum independent set: ")
    f.write(str(len(maxSet)))
    f.write("\nMaximum independent set: ")
    f.write(" ".join(str(node) for node in maxSet))
    f.close()


def maxSet(graph, nodes):
    localGraph = graph.copy()

    if localGraph.number_of_edges() == 0:
        return set(localGraph.nodes)

    node = list(localGraph.nodes)[0]
    while localGraph.degree[node] == 0:
        index = random.randint(0, len(nodes) - 1)
        node = list(localGraph.nodes)[index]

    neighbors = set(localGraph[node].keys())
    localGraph.remove_node(node)

    set1 = maxSet(localGraph, nodes - {node})
    localGraph.remove_nodes_from(neighbors)
    set2 = maxSet(localGraph, nodes - {node} - set(neighbors))
    set2.add(node)
    return set1 if len(set1) > len(set2) else set2


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == "-f":
        graph = getGraphFromFile(sys.argv[2])

    elif mode == "-c":
        nodes = int(sys.argv[2])
        edges = int(sys.argv[3])
        graph = nx.gnm_random_graph(nodes, edges)

    elif mode == "-t":
        nodes = int(sys.argv[2])
        edges = int(sys.argv[3])
        times = int(sys.argv[4])

        start = timeit.default_timer()
        for i in range(0, times):
            graph = nx.gnm_random_graph(nodes, edges)
            listOfNodes = set(graph.nodes)
            maxISet = maxSet(graph, listOfNodes)

        stop = timeit.default_timer()
        print("Average execution time: ", (stop - start)/times)
        sys.exit()

    else:
        sys.exit("Wrong arguments list.")

    listOfNodes = set(graph.nodes)

    start = timeit.default_timer()
    maxSet = maxSet(graph, listOfNodes)
    stop = timeit.default_timer()

    print("Number of nodes in maximum independent set: ", len(maxSet))
    print("Maximum independent set: ", maxSet)

    print("Execution time: ", stop - start)

    if "-w" in sys.argv:
        writeGraph(graph, maxSet)

    if "-d" in sys.argv:
        plt.subplot(121)
        nx.draw(graph, with_labels=True, font_weight='bold')
        plt.show()
