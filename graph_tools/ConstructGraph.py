from algorithms import dijkstra
from algorithms import astar
from threading import Thread
#Construct a graph representation of the network of places to visited ready to be used by a TSP solver.

def construct_graph(graph, nodes, algorithm = "dijkstra"):
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

    #Select the algorithm to use
    if algorithm == "Dijkstra":
        print("Dijkstra")
        function = dijkstra.dijkstra
    elif algorithm == "A*":
        print("A*")
        function = astar.astar
    else:
        raise ValueError("Unknown algorithm")

    threads = []
    for start_node in nodes:
        for end_node in nodes:

            if start_node == end_node:
                continue

            #Create a thread for each pair of nodes
            thread = function_thread(graph, start_node, end_node, function)
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

        time, path = thread.time, thread.path

        if(time != float("inf")):
            #Add the path to the graph
            G[path[0]][path[-1]] = {"time": time, "path": path}
            
    
    return G

class function_thread(Thread):
    def __init__(self, graph, start_node, end_node, algorithm):
        Thread.__init__(self)
        self.graph = graph
        self.start_node = start_node
        self.end_node = end_node
        self.time = None
        self.path = None
        self.algorithm = algorithm

    def run(self):
        self.time, self.path = self.algorithm(self.graph, self.start_node, self.end_node)
    