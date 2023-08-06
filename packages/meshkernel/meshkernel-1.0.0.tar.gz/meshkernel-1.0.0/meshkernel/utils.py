def plot_edges(node_x, node_y, edge_nodes, ax, *args, **kwargs):
    """Plots the edges at a given axes.
    `args` and `kwargs` will be used as parameters of the `plot` method.


    Args:
        node_x (ndarray): A 1D double array describing the x-coordinates of the nodes.
        node_y (ndarray): A 1D double array describing the y-coordinates of the nodes.
        edge_nodes (ndarray, optional): A 1D integer array describing the nodes composing each mesh 2d edge.
        ax (matplotlib.axes.Axes): The axes where to plot the edges
    """
    for edge_index in range(0, edge_nodes.size, 2):
        first_edge_node_index = edge_nodes[edge_index]
        second_edge_node_index = edge_nodes[edge_index + 1]

        edge_x = [
            node_x[first_edge_node_index],
            node_x[second_edge_node_index],
        ]
        edge_y = [
            node_y[first_edge_node_index],
            node_y[second_edge_node_index],
        ]

        ax.plot(edge_x, edge_y, *args, **kwargs)
