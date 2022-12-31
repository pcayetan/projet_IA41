from heapq import heappop, heappush
from networkx import Graph, max_weight_matching
from itertools import count
from copy import deepcopy
from collections import deque
    

def christofides(dictionary, weight="time"):
    """Compute an approximation of the shortest path between all the nodes of the dictionary
    Uses Christofides Algorithm to solve the traveling's salesman problem (TSP).
    
    Parameters:
    ---------------
    dictionary: python dictionary, complete graph
    weight: weight used in the dictionary
    
    Returns:
    an approximation of the shortest path between the dictionary's nodes
    """
    non_oriented_graph = oriented_to_non_oriented_graph(dictionary=dictionary, weight="time")
    tree = prim_dictionnary(dict=non_oriented_graph, weight="time")
    odd_graph = get_odd_graph(dictionary, tree)
    min_weight_matchings = dic_min_weight_matching(odd_graph)
    eulerian_graph = create_eulerian_graph(tree, min_weight_matchings)
    eulerian_path = hierholzer_eulerian_circuit(eulerian_graph)
    hamiltonian_path = shortcutting(eulerian_path)
    new_path = reorder(hamiltonian_path, list(dictionary.keys())[0])
    return new_path


def oriented_to_non_oriented_graph(dictionary, weight="time"):
    """Compute the non oriented version of the dictionary, cleans the dictionary

    Parameters:
    --------------
    dictionary: oriented graph like [start_node][end_node][weight] = weight
    """
    dictionary_copy = deepcopy(dictionary)
    new_dictionary = {node: {} for node in dictionary_copy.keys()}
    for start_node in dictionary_copy:
        for end_node in dictionary_copy[start_node]:
            if start_node == end_node:
                continue
            w = (dictionary_copy[start_node][end_node][weight] + dictionary_copy[start_node][end_node][weight]) / 2
            new_dictionary[start_node][end_node] = {weight : w}
            new_dictionary[end_node][start_node] = {weight : w}
            del dictionary_copy[end_node][start_node]
    return new_dictionary


def prim_dictionnary(dict, weight="time"):
    """Compute a the edges of a minimim spanning tree (mst) for a graph
    Uses Prim's algorithm

    Parameters:
    ---------------
    G: nx.Graph 
    weight: weight used in the graph
    
    Returns:
    An iterator containing the edges of the mst
    """
    push = heappush
    pop = heappop
    nodes = set(dict)
    tree = {node : {} for node in nodes}
    while nodes:
        u = nodes.pop() #arbitrary node
        heap = []   
        visited = {u}
        for v, d in dict[u].items():
            wt = d.get(weight, 1)
            push(heap, (wt, u, v, d))
        while nodes and heap:
            _, u, v, d = pop(heap)
            if v in visited or v not in nodes:
                continue
            tree[u][v] = d
            tree[v][u] = d
            visited.add(v)
            nodes.discard(v)
            for w, d2 in dict[v].items():
                if w in visited:
                    continue
                new_weight = d2.get(weight, 1)
                push(heap, (new_weight, v, w, d2))
    return tree


def get_odd_graph(dictionary, tree):
    """Get the vertices with odd degree of the tree from the main graph to get a new graph
     Parameters:
    ---------------
        dictionary: graph under dictionary form
        tree: minimum spanning tree
    
    Returns:
        I: dictionary containing the vertices of odd degree
    """
    I = deepcopy(dictionary)
    for node in tree:
        if not (len(tree[node]) % 2):
            for second_node in I[node]:
                I[second_node].pop(node)
            I.pop(node)
    return I


def dic_min_weight_matching(dictionary, weight="time"):
    """Calculate a minimum weight matching from a graph

     Parameters:
    ---------------
        dictionary: graph under dictionary form
        weight: weight used in the graph
    
    Returns:
        edges: dictionary containing the matchings
    
    """
    max_weight = 1 + max(dictionary[first_node][second_node][weight] for first_node in dictionary for second_node in dictionary[first_node])
    new_dic = deepcopy(dictionary)
    for first_node in dictionary:
        for second_node in dictionary[first_node]:
            new_dic[first_node][second_node][weight] = max_weight - dictionary[first_node][second_node][weight]
            
    InvG = Graph(new_dic)
    edges = {}
    matchings = max_weight_matching(InvG, maxcardinality=True, weight=weight)
    for matching in matchings:
        matching = list(matching)
        u = matching[0]
        v = matching[1]
        for node in matching: 
            edges[node] = {}
        w = dictionary[u][v][weight]
        edges[v][u] = {weight : w}
        edges[u][v] = {weight : w}
    return edges


def create_eulerian_graph(tree, min_weight_matchings):
    """ Adds the tree and minimum weight matchings results to get the eulerian graph

    Parameters:
    ---------------
        tree: minimum spanning tree
        min_weight_matchings: dictionary containing the matchings

    Returns:
        graph: dictionary containing the eulerian graph
    """
    graph = deepcopy(tree)
    for node, value in min_weight_matchings.items():
        graph[node].update(value)
    return graph


def hierholzer_eulerian_circuit(eulerian_graph):
    """Calculate an eulerian circuit in an eulerian graph
    
    Parameters:
    ---------------
        eulerian_graph: eulerian graph under dictionary form
    
    Returns:
        path: list containing the circuit
    """
    dic = deepcopy(eulerian_graph)
    first_vertex = list(dic.keys())[0]
    vertex_stack = [first_vertex]
    path = []
    last_vertex = None
    while vertex_stack:
        current_vertex = vertex_stack[-1]
        if dic[current_vertex]:
            next_vertex, _ = list(dic[current_vertex].items())[0]
            vertex_stack.append(next_vertex)
            dic[current_vertex].pop(next_vertex)
            dic[next_vertex].pop(current_vertex)
        else:
            if last_vertex is not None:
                path.append(last_vertex)
            last_vertex = current_vertex
            vertex_stack.pop()
    path.append(current_vertex)
    return  path


def shortcutting(path):
    """Removes the nodes through which the path comes through twice
    Parameters:
    ---------------
        path: list 
    
    Returns:
        nodes: list
    """
    nodes = [path[0]]
    for node in path:
        if node in nodes:
            continue
        nodes.append(node)
    return nodes


def reorder(list, first):
    """Rotate the list until the parameters "first" is in first position, then appends it to the list
    Parameters:
    ---------------
        list: list 
        first: int
    
    Returns:
        list: list
    """
    while(list[0] != first):
        list.append(list.pop(0))
    list.append(first)
    return list