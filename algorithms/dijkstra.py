from heapq import heappop, heappush

import networkx as nx



def dijkstra(Graph, source, target):
    """Find shortest weighted paths in G from source to target using Dijkstra's algorithm.
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
    time : float
        Shortest time from source to target.
    path : list
        List of nodes in a shortest path.
    """

    if source == target:
        return (0, [source])
    
    push = heappush
    pop = heappop

    neighbor_list=[Graph._succ,Graph._pred]

    #We are using the two way Dijkstra algorithm, so we need to keep track of the distances from both the source and the target
    out = [{}, {}] #List of dictionaries, each dictionary contains the distance from the source/target to each node
    path = [{},{}]  # dictionary of paths
    seen = [{source : 0},{target : 0}]  # dictionary of nodes that have been visited
    to_explore = [[],[]] # heap of (distance,label) tuples for all non-seen nodes

    #Initialize the heap with the source and target
    push(to_explore[0], (0, source))
    push(to_explore[1], (0, target))
    
    #Initialize the path with the source and target
    path[0][source] = [source]
    path[1][target] = [target]

    direction = 1 #Direction of the search, 0 is forward, 1 is backward

    while to_explore[0] and to_explore[1]:

        direction = 1 - direction #Switch direction

        #Pop the smallest distance node from the heap
        (dist, v) = pop(to_explore[direction])

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
                    push(to_explore[direction], (weight, neighbor))
                    path[direction][neighbor] = path[direction][v] + [neighbor]
                #If the neighbor has been visited, but the new path is shorter, update the heap
                elif weight < seen[direction][neighbor]:
                    seen[direction][neighbor] = weight
                    push(to_explore[direction], (weight, neighbor))
                    path[direction][neighbor] = path[direction][v] + [neighbor]
            
    return (float('inf'), [])
    

def travel_time_route(u, v, graph):
    """Return the travel time of a route."""
    return graph[u][v][0]['travel_time'] if 'travel_time' in graph[u][v][0] else 8.33*graph[u][v][0]["lenght"] # 30 km/h

def weight_node(u, v, data, graph, direction):
    """Return the weight of an edge."""
    weight = data[u]
    if direction == 0:
        weight += travel_time_route(u, v, graph)
    else:
        weight += travel_time_route(v, u, graph)
    return weight