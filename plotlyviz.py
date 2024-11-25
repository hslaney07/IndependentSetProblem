import networkx as nx
import plotly.graph_objects as go

class PlotlyVisual:
    def __init__(self, graph, independent_set, name):
        self.graph = graph
        self.pos = nx.bipartite_layout(self.graph, nodes=[node for node in self.graph if self.graph.nodes[node]["bipartite"] == 0])
        self.independent_set = independent_set
        self.selected_node = None
        self.graph_name = name

    def get_node_colors(self):
        node_colors = []
        for node in self.graph.nodes:
            if node in self.independent_set:
                if node is self.selected_node:
                    node_colors.append('darkorange')  # Highlight selected nodes
                else:
                    node_colors.append('orange')
            else:
                if self.graph.nodes[node]["bipartite"] == 0:
                    node_colors.append('skyblue')  # Color for set A
                else:
                    node_colors.append('lightgreen')  # Color for set B
        return node_colors

    def get_edge_info(self):
        edges_to_draw = []
        edge_colors = []

        for edge in self.graph.edges:
            if self.selected_node is None:
                edges_to_draw.append(edge)
                edge_colors.append('lightgray')
            else:
                if self.selected_node in edge:
                    edges_to_draw.append(edge)
                    edge_colors.append('red')

        return edges_to_draw, edge_colors

    def plotly_draw_graph(self):
        """
        Create a Plotly graph visualization.
        """
        # Node positions from NetworkX layout
        node_x = [self.pos[node][0] for node in self.graph.nodes]
        node_y = [self.pos[node][1] for node in self.graph.nodes]
        node_colors = self.get_node_colors()

        # Edge data
        edge_x, edge_y = [], []
        for edge in self.graph.edges:
            x0, y0 = self.pos[edge[0]]
            x1, y1 = self.pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        # Create the Plotly figure
        fig = go.Figure()

        # Add edges as lines
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='lightgray'),
            hoverinfo='none',
            mode='lines'
        ))

        # Add nodes as scatter points
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            marker=dict(
                size=10,
                color=node_colors,
                opacity=1,
                line=dict(width=2, color='black')
            ),
            text=list(self.graph.nodes),
            hoverinfo='text',
            name='Nodes',
            customdata=list(self.graph.nodes)  # Store node names for click events
        ))

        # Title and layout adjustments
        fig.update_layout(
            title=f"Independent Set Visualization for {self.graph_name}",
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            clickmode='event+select'  # Enable click events
        )

        # Add a callback for click events
        fig.update_traces(
            selectedpoints=[],
            marker=dict(size=15)  # Make selected node bigger
        )

        fig.update_layout(
            dragmode='zoom'  # Enable zoom functionality
        )

        fig.show()

    def update_selected_node(self, selected_node):
        """Toggle selection of the node."""
        self.selected_node = selected_node if self.selected_node != selected_node else None
        self.plotly_draw_graph()

    def show(self):
        """
        Show the interactive graph.
        """
        self.plotly_draw_graph()
