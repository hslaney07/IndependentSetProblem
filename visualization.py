import matplotlib.pyplot as plt
import networkx as nx

class IndependentSetInteractiveGraph:
    def __init__(self, graph, independent_set, name):
        self.graph = graph
        self.pos = nx.spring_layout(graph)
        self.independent_set = independent_set
        self.selected_node = None
        self.graph_name = name

    def draw_graph(self):
        '''
        Draw the graph and highlight the independent set and selected node.
        Args:
            self (IndependentSetInteractiveGraph): Interactive Graph
        '''
        plt.clf() 

        # adds nodes to plot
        nx.draw_networkx_nodes(
            self.graph, self.pos,
            node_color=[
                'darkorange' if n == self.selected_node and n in self.independent_set else
                'darkblue' if n == self.selected_node and n not in self.independent_set else
                'orange' if n in self.independent_set else
                 'lightblue'
                for n in self.graph.nodes
            ],
            node_size=500
        )
        
        # adds edges to the plot
        edges_to_draw = []
        edge_colors = []

        for edge in self.graph.edges:
            if self.selected_node is None:
                edges_to_draw.append(edge)
                edge_colors.append('black')

            else:
                if self.selected_node in edge:
                    edges_to_draw.append(edge)
                    edge_colors.append('red')

        nx.draw_networkx_edges(
            self.graph,
            self.pos,
            edgelist=edges_to_draw,
            edge_color=edge_colors,
            width=1
        )

        # draw labels and title
        independent_set_size = len(self.independent_set)
        total_nodes = len(self.graph.nodes)
        metadata_text = f"Independent Set Size: {independent_set_size}\nTotal Nodes: {total_nodes}"

        nx.draw_networkx_labels(self.graph, self.pos)
        plt.title("Independent Set Visualization for " + self.graph_name)

        plt.gcf().text(0.02, 0.10, metadata_text, fontsize=10, va='top', ha='left',
                       bbox=dict(facecolor='lightgray', alpha=0.7, edgecolor='black'))
        plt.gca().set_facecolor('lightgray') 
        plt.gca().set_axis_off()  
        plt.pause(0.01) 

    def on_click(self, event):
        '''
        Handle mouse click events.
        Args:
            self (IndependentSetInteractiveGraph): Interactive Graph
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
        
        self.draw_graph()

    def show(self):
        '''
        Show the interactive graph.
        Args:
            self (IndependentSetInteractiveGraph): Interactive Graph
        '''
        self.draw_graph()
        fig = plt.gcf()
        fig.canvas.mpl_connect('button_press_event', self.on_click) 
        plt.show()
