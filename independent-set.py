import networkx as nx
from visualization import IndependentSetInteractiveGraph

def greedy_independent_set(graph):
    """
    not greedy
    Greedy algorithm to compute an independent set.
    Args:
        graph (nx.Graph): Input graph.
    Returns:
        set: Independent set of vertices.
    """
    independent_set = set()

    while len(graph.nodes) > 0:
        # select the vertex with the smallest degree
        # grab random node
        min_degree_node = min(graph.nodes, key=lambda x: graph.degree[x])
        independent_set.add(min_degree_node)

        # remove the vertex and its neighbors from the graph
        neighbors = list(graph.neighbors(min_degree_node))
        graph.remove_node(min_degree_node)
        graph.remove_nodes_from(neighbors)

    return independent_set

# look at bipartite graphs, n=1000
    # randomly place edges

def generate_graphs():
    """
    Generate different families of graphs for testing.
    Returns:
        dict: A dictionary where graph names are keys and graphs are values.
    """
    graphs = {
        "random_graph": nx.gnp_random_graph(50, 0.2, seed=42),
        "bipartite_graph": nx.complete_bipartite_graph(25, 25),
        "grid_graph": nx.grid_2d_graph(7, 7),
        "path_graph": nx.path_graph(50),
        "cycle_graph": nx.cycle_graph(50),
    }
    return graphs

if __name__ == "__main__":
    graphs = generate_graphs()
    for name, graph in graphs.items():
        independent_set = greedy_independent_set(graph.copy())

        print(f"\nVisualizing {name}:")
        print(f"Independent Set Size: {len(independent_set)}")

        interactive_graph = IndependentSetInteractiveGraph(graph, independent_set, name)
        interactive_graph.show()

