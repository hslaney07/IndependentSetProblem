import os
import random
from fpdf import FPDF
import networkx as nx
from visualization import IndependentSetMatplotGraph

def random_independent_set(graph):
    """
    Random algorithm to compute an independent set.
    Args:
        graph (nx.Graph): Input graph.
    Returns:
        set: Independent set of vertices.
    """
    independent_set = set()

    while len(graph.nodes) > 0:
        # select random vertex
        random_node = random.choice(list(graph.nodes))
        independent_set.add(random_node)

        # remove the vertex and its neighbors from the graph
        neighbors = list(graph.neighbors(random_node))
        graph.remove_node(random_node)
        graph.remove_nodes_from(neighbors)

    return independent_set

def create_bipartite_graph(n1, n2, d):
    """
    Create a bipartite graph with n1 nodes in set A, n2 nodes in set B,
    and edge probability d / n for each (ai, bj).
    
    Args:
        n1 (int): Number of nodes in set A.
        n2 (int): Number of nodes in set B.
        d (int): Parameter to determine edge probability.

    Returns:
        nx.Graph: A bipartite graph.
    """
    bipartite_graph = nx.Graph()

    set_a = [f"A{i}" for i in range(1, n1 + 1)]
    set_b = [f"B{i}" for i in range(1, n2 + 1)]

    bipartite_graph.add_nodes_from(set_a, bipartite=0)
    bipartite_graph.add_nodes_from(set_b, bipartite=1)

    n = max(n1, n2)
    prob_of_an_edge = d / n   

    for a in set_a:
        for b in set_b:
            if random.random() < prob_of_an_edge: 
                bipartite_graph.add_edge(a, b)
    
    return bipartite_graph


def add_multicolumn_text(pdf, nodes, columns=15, max_width=200, max_height=270, font_size=12):
    """
    Add multiple nodes in a compact, multi-column format to the PDF.

    Args:
        pdf (FPDF): The FPDF instance.
        nodes (list): List of nodes to display.
        columns (int): Number of nodes per line.
        max_width (int): Width of the PDF.
        max_height (int): Height of the page.
        font_size (int): Font size.
    """
    pdf.set_font("Times", size=font_size)
    chunked_nodes = [nodes[i:i + columns] for i in range(0, len(nodes), columns)]
    
    for chunk in chunked_nodes:
       
        line_text = ", ".join(map(str, chunk))   # line of nodes
        
        if pdf.get_y() + 10 > max_height:
            pdf.add_page()  # add a page if needed
        
        pdf.cell(max_width, 10, txt=line_text, ln=True, align="C")

def set_up_folders(d_values):
    '''
    Sets up folders to save graph pdf outputs and graph images.
    Args:
        d_values (list): List of d-values
    Returns:
        tuple where the first value is a list of subfolders for graph images,
             the second value is a string literal of the pdf output folder
    '''

    subfolders = []
    d_value_main_folder = "matplotlib_visuals"
    for d in d_values:
        folder = f'{d_value_main_folder}/d={d}visuals'
        os.makedirs(folder, exist_ok=True)

        subfolders.append(folder)

    pdf_output_folder = "pdf_output"
    os.makedirs(pdf_output_folder, exist_ok=True)

    return subfolders, pdf_output_folder


if __name__ == "__main__":
    # setting up biparite graphs
    n1 = 1000
    n2 = 1000
    d_values = [3, 5, 10]

    graphs = []

    for d in d_values:
        graphs.append([f"Bipartite Graph \n(n1={n1}, n2={n2}, d={d})", create_bipartite_graph(n1=n1, n2=n2, d=d)])

    # values to configure when running simulations
    number_simulations_per_d_value = 100
    graph_output = True
    include_list_of_nodes_in_independent_set_in_pdf = True
    save_to_one_file = False

    # set up pdf
    pdf = FPDF()

    #setting up folders and subfolders
    subfolders, pdf_output_folder = set_up_folders(d_values)
    
    for d, name_and_graph in zip(d_values, graphs):
        name, graph = name_and_graph 
        subfolder = [item for item in subfolders if f"d={d}" in item][0]

        pdf.add_page()
        total_nodes_in_independent_set = 0
        
        print_name = name.replace("\n", "")
        print(f"\t Beginning simulations for {print_name}")

        for iteration in range(0, number_simulations_per_d_value):

            # get values and information to display 
            graph_name = f"{name}, Iter {iteration+1}"
            independent_set = random_independent_set(graph.copy())
            independent_set_size = len(independent_set)
            total_nodes = len(graph.nodes)
            total_nodes_in_independent_set += independent_set_size

            # display info in pdf
            pdf.set_font("Times", style="B", size=16)
            pdf.multi_cell(200, 10, txt=f"Independent Set Information for {graph_name}", align="C")
            pdf.set_font("Times", size=12)
            pdf.cell(200, 10, txt=f"Total Nodes: {total_nodes}", ln=True, align="C")
            pdf.cell(200, 10, txt=f"Independent Set Size: {independent_set_size}", ln=True, align="C")

            if include_list_of_nodes_in_independent_set_in_pdf:
                nodes_in_independent_set_from_A = [node for node in graph if graph.nodes[node]["bipartite"] == 0 and node in independent_set]
                nodes_in_independent_set_from_B = [node for node in graph if graph.nodes[node]["bipartite"] == 1 and node in independent_set]

                pdf.cell(200, 10, txt=f"Nodes in Independent Set from A ({len(nodes_in_independent_set_from_A)}):", ln=True, align="C")
                add_multicolumn_text(pdf, nodes_in_independent_set_from_A)

                pdf.cell(200, 10, txt=f"Nodes in Independent Set from B ({len(nodes_in_independent_set_from_B)}):", ln=True, align="C")
                add_multicolumn_text(pdf, nodes_in_independent_set_from_B)
            
            if graph_output:
                matplotlib_graph = IndependentSetMatplotGraph(graph, independent_set, graph_name)

                graph_save_name = graph_name.replace(" ", "").replace("\n", "")
                saving_location = f"{subfolder}/{graph_save_name}"

                matplotlib_graph.save_fig(saving_location)
                pdf.image(f"{saving_location}.png", type="png", x=10, w=190)
                pdf.add_page()
            
            print(f"\t\t Output complete for iteration #{iteration+1} (d={d})")
        
        avg_node_in_independent_set = total_nodes_in_independent_set/number_simulations_per_d_value
        pdf.set_font("Times", style="B", size=16)
        pdf.set_text_color(255, 0, 0)
        pdf.multi_cell(200, 10, txt=f"Avg. Nodes in Independent Set for {name}: {avg_node_in_independent_set}",  align="C")
        pdf.set_text_color(0, 0, 0)

        if not save_to_one_file:
            graph_save_name = graph_name.replace(" ", "").replace("\n", "")
            pdf.output(f"{pdf_output_folder}/{graph_save_name}.pdf")
            pdf = FPDF()
            print(f"\t Output for {iteration} iterations saved to {pdf_output_folder}/{graph_save_name}.pdf")

    if save_to_one_file:
        pdf.output(f"{pdf_output_folder}/all_graphs_{number_simulations_per_d_value}iterations.pdf")
        print(f"Output for all graphs and iterations saved to {pdf_output_folder}/all_graphs.pdf")
        
    