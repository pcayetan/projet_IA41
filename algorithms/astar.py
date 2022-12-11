from heapq import heappop, heappush
import networkx as nx
import math



def astar(Graph, source, target):
    """Find shortest weighted paths in G from source to target using  A* algorithm.
    Parameters:
    -----------
    G : NetworkX oriented graph
    source : node
       Starting node for path
    target : node
         Ending node for path
    weight : string, optional (default='weight')
         Edge data key corresponding to the edge weight
    Returns:
    --------
    distance : dictionary
         Dictionary of shortest weighted paths keyed by target.
    """
    
    if source == target:
        return (0, [source])
        
    def heuristic(u, v):
            # Get the latitude and longitude coordinates of the nodes
            lat1 = Graph.nodes[u]["y"]
            lon1 = Graph.nodes[u]["x"]
            lat2 = Graph.nodes[v]["y"]
            lon2 = Graph.nodes[v]["x"]
            
            # Convert the coordinates to radians
            lat1 = lat1 * math.pi / 180
            lon1 = lon1 * math.pi / 180
            lat2 = lat2 * math.pi / 180
            lon2 = lon2 * math.pi / 180
            
            # Calculate the great circle distance between the two points
            a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2-lon1)/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            d = 6371 * c 
            
            return d

    push = heappush
    pop = heappop

    neighbor_list=[Graph._succ,Graph._pred]

    #We are using the two way A* algorithm, so we need to keep track of the distances from both the source and the target
    out = [{}, {}] #List of dictionaries, each dictionary contains the distance from the source/target to each node
    path = [{},{}]  # dictionary of paths
    seen = [{source : 0},{target : 0}]  # dictionary of nodes that have been visited
    to_explore = [[],[]] # heap of (distance, heuristic, label) tuples for all non-seen nodes

    #Initialize the heap with the source and target
    push(to_explore[0], (0, heuristic(source, target), source))
    push(to_explore[1], (0, heuristic(target, source), target))
    
    #Initialize the path with the source and target
    path[0][source] = [source]
    path[1][target] = [target]

    direction = 1 #Direction of the search, 0 is forward, 1 is backward

    while to_explore[0] and to_explore[1]:

        direction = 1 - direction #Switch direction

        #Pop the smallest distance node from the heap
        ( _ , dist, v) = pop(to_explore[direction])

        if v in out[direction]:
            continue
        
        out[direction][v] = dist

        #Check if the node has been visited by the other search
        if v in out[1-direction]:
            #If it has, we have found a shortest path
            return (out[0][v] + out[1][v], path[0][v] + list(reversed(path[1][v]))[1:])
        
        for neighbor in neighbor_list[direction][v]:
            if neighbor not in out[direction]:
                weight = weight_node(v, neighbor, out[direction], Graph, direction)
                #If the neighbor has not been visited, add it to the heap
                if neighbor not in seen[direction]:
                    seen[direction][neighbor] = weight
                    push(to_explore[direction], (weight + heuristic(neighbor, target), weight, neighbor))
                    path[direction][neighbor] = path[direction][v] + [neighbor]
                #If the neighbor has been visited, but the new path is shorter, update the heap
                elif weight < seen[direction][neighbor]:
                    seen[direction][neighbor] = weight
                    push(to_explore[direction],  (weight + heuristic(neighbor, target), weight, neighbor))
                    path[direction][neighbor] = path[direction][v] + [neighbor]
            
    return (float('inf'), [])
    

def travel_time_route(u, v, graph):
    """Return the travel time of a route."""
    return graph[u][v][0]['travel_time'] if 'travel_time' in graph[u][v][0] else graph[u][v][0]["length"]/8.33 # 30 km/h

def weight_node(u, v, data, graph, direction):
    """Return the weight of an edge."""
    weight = data[u]
    if direction == 0:
        weight += travel_time_route(u, v, graph)
    else:
        weight += travel_time_route(v, u, graph)
    return weight

