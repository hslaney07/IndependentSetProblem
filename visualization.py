import matplotlib.pyplot as plt
import networkx as nx

class IndependentSetMatplotGraph:

    def __init__(self, graph, independent_set, name):
        self.graph = graph
        self.pos = nx.bipartite_layout(self.graph, nodes=[node for node in self.graph if self.graph.nodes[node]["bipartite"] == 0])
        self.independent_set = independent_set
        self.selected_node = None
        self.graph_name = name

    def draw_graph(self):
        '''
        Draw the graph and highlight the independent set and selected node.
        Args:
            self (IndependentSetInteractiveGraph): Interactive Graph
        '''
        plt.figure(figsize=(6, 6)) 

        edges_to_draw, edge_colors = self.get_edge_info()     
        
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[node for node in self.graph if self.graph.nodes[node]["bipartite"] == 0 and node not in self.independent_set and (node in list(self.graph.neighbors(self.selected_node)) or node==self.selected_node if self.selected_node!=None else True)], 
                            node_color="skyblue", label="Set A", node_size=1)
    
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[node for node in self.graph if self.graph.nodes[node]["bipartite"] == 1 and node not in self.independent_set and (node in list(self.graph.neighbors(self.selected_node)) or node==self.selected_node if self.selected_node!=None else True)], 
                            node_color="lightgreen", label="Set B", node_size=1)
        
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[node for node in self.graph if self.graph.nodes[node]["bipartite"] == 0 and node in self.independent_set and (node in list(self.graph.neighbors(self.selected_node)) or node==self.selected_node if self.selected_node!=None else True)], 
                            node_color="orange", label="Independent Set, Set A", node_size=1)
        
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[node for node in self.graph if self.graph.nodes[node]["bipartite"] == 1 and node in self.independent_set and (node in list(self.graph.neighbors(self.selected_node)) or node==self.selected_node if self.selected_node!=None else True)], 
                            node_color="darkorange", label="Independent Set, Set B", node_size=1)

        nx.draw_networkx_edges(
            self.graph,
            self.pos,
            edgelist=edges_to_draw,
            edge_color=edge_colors,
            width=0.1,
            alpha=0.2
        )

        # draw labels and title
        independent_set_size = len(self.independent_set)
        total_nodes = len(self.graph.nodes)
        metadata_text = f"Independent Set Size: {independent_set_size}\nTotal Nodes: {total_nodes}"

        plt.legend(scatterpoints=1, bbox_to_anchor=(1.1, 0.08))
        plt.title("Independent Set Visualization for " + self.graph_name)

        plt.gcf().text(0.02, 0.10, metadata_text, fontsize=10, va='top', ha='left',
                       bbox=dict(facecolor='lightgray', alpha=0.7, edgecolor='black'))
        plt.gca().set_axis_off() 
    
    def save_fig(self, saving_location):
        '''
        Saves the graph figure to the saving location.
        Args:
            self (IndependentSetMatplotGraph): Matplot Graph
            saving_location (string): Location where to save the figure to.
        '''
        self.draw_graph()
        fig = plt.gcf()
        fig.patch.set_facecolor("gray")
        
        fig.savefig(f"{saving_location}")
        plt.close()


    def get_edge_info(self):
        '''
        Gets the edges to draw and colors.
        '''
        edges_to_draw = []
        edge_colors = []

        for edge in self.graph.edges:
            if self.selected_node is None:
                edges_to_draw.append(edge)
                edge_colors.append('white')
            else:
                if self.selected_node in edge:
                    edges_to_draw.append(edge)
                    edge_colors.append('red')

        return edges_to_draw, edge_colors
    
    def show(self):
        '''
        Show the interactive graph.
        Args:
            self (IndependentSetMatplotGraph): Matplot Graph
        '''
        self.draw_graph()
        fig = plt.gcf()
        fig.canvas.mpl_connect('button_press_event', self.on_click) 
        plt.show()

    def on_click(self, event):
        '''
        Handle mouse click events.
        Args:
            self (IndependentSetMatplotGraph): Matplot Graph
            event (matplotlib.backend_bases.MouseEvent): Mouse event.
        '''
        if event.xdata is None or event.ydata is None:
            return  # ignore clicks outside the plot area

        # find the nearest node to the click
        closest_node = min(
            self.graph.nodes,
            key=lambda n: (self.pos[n][0] - event.xdata) ** 2 + (self.pos[n][1] - event.ydata) ** 2
        )

        # if user clicks node twice - removes the highlight on the selected node
        self.selected_node = closest_node if self.selected_node != closest_node else None