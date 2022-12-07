import algorithms.dijkstra as dijkstra
#Construct a graph representation of the network of places to visited ready to be used by a TSP solver.

def construct_graph(graph, nodes):
    """Construct a graph representation of the network of places to visited ready to be used by a TSP solver.
    The graph is represented as a dictionary of dictionaries. The keys are the nodes of the graph,
    and the values are dictionaries containing the time needed to travel between the node and its neighbors and 
    the path to take to reach them.
    
    Parameters:
    graph (networkx graph): the graph of the network
    nodes (list): the list of nodes to visit
    
    Returns:
    dict: the graph representation
    """

    #Create a graph with only the nodes to visit
    G = {node: {} for node in nodes}

    for start_node in nodes:
        for end_node in nodes:

            if start_node == end_node:
                continue

            #Find the shortest path between the two nodes
            time, path = dijkstra.dijkstra(graph, start_node, end_node)

            #Add the path to the graph
            G[start_node][end_node] = (time, path)
            
    
    return G
    