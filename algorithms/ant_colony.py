#Solve the TSP problem with the ant_colony algorithm
from threading import Thread

class ant_colony:

    class ant(Thread):

        def __init__(self, graph, start_node, alpha, beta, first_pass=False, heuristic=None):
            """Create an ant
            
            Args:
                graph: The graph to visit
                start: The node where the ant starts
                alpha: The alpha parameter of the algorithm, usually smaller than 1
                beta: The beta parameter of the algorithm, usually bigger than 1"""
            Thread.__init__(self)

            self.graph = graph
            self.start_node = start_node
            self.path = [start_node]
            self.current = start_node
            self.distance = float(0)
            self.alpha = alpha
            self.beta = beta
            
            self.finished = False
            self.first_pass = first_pass

            if heuristic is None:
                self.heuristic = self._heuristic

        def run(self):
            """Run the ant until it has visited all the nodes"""
            while len(self.path) < len(self.graph):
                self._move()

            self.path.append(self.start_node)
            self.finished = True

        def _move(self):
            """Move the ant to the next node and update the path and the distance"""

            #Get the neighbors of the current node
            neighbors = list(self.graph[self.current].keys())

            #Remove the nodes already visited
            for node in self.path:
                if node in neighbors:
                    neighbors.remove(node)

            #If there is no neighbor, the ant is stuck
            if len(neighbors) == 0:
                self.distance += self.graph[self.current][self.start_node]["time"]
                self.current = self.start_node
                self.path.append(self.start_node)

                self.finished = True
                return

            #Compute the probability of each neighbor
            probabilities = self._probability(neighbors)

            #Choose the next node
            next_node = self._choose(probabilities)

            #Add the distance to the total distance
            self.distance += self.graph[self.current][next_node]["time"]

            #Update the current node and the path
            self.current = next_node
            self.path.append(next_node)
        
        def _probability(self, visitable_nodes):
            """Compute the probability of going to the node
            Use the function on the wikipedia page
            
            Args:
                node: The node to go to
            
            Returns:
                The probability of going to the node"""

            sum_of_probabilities = 0
            probabilities = {}

            #If it's the first pass, the probability is 1 for each node
            if self.first_pass:
                for node in visitable_nodes:
                    probabilities[node] = 1
                    sum_of_probabilities += probabilities[node]
            else:
                for node in visitable_nodes:
                    probabilities[node] = self.heuristic(node) ** self.beta * self.graph[self.current][node]["pheromone"] ** self.alpha
                    sum_of_probabilities += probabilities[node]

            #Normalize the probabilities
            if sum_of_probabilities == 0:
                for node in visitable_nodes:
                    probabilities[node] = 1 / len(visitable_nodes)
            else:
                for node in visitable_nodes:
                    probabilities[node] /= sum_of_probabilities

            #Compute the probability
            return probabilities

        def _choose(self, probabilities):
            """Choose the next node to go to
            
            Args:
                probabilities: The probabilities of each node
            
            Returns:
                The node to go to"""
            
            from random import random

            #Choose a random number between 0 and 1
            r = random()

            #Choose the node
            for node in probabilities.keys():
                r -= probabilities[node]
                if r <= 0:
                    return node

        
        def _heuristic(self, node):
            """Compute the heuristic of the node
            Use the function on the wikipedia page
            
            Args:
                node: The node to compute the heuristic
            
            Returns:
                The heuristic of the node"""
            return 1 / self.graph[self.current][node]["time"]
        
    def __init__(self, graph, start_node, alpha=0.5, beta=2, rho=0.5, n_ants=10, n_iterations=100, first_pass=True, heuristic=None):
        """Create an ant_colony object
        
        Args:
            graph: The graph to visit
            start: The node where the ants start
            alpha: The alpha parameter of the algorithm, usually smaller than 1
            beta: The beta parameter of the algorithm, usually bigger than 1
            rho: The rho parameter of the algorithm, usually between 0 and 1
            n_ants: The number of ants
            n_iterations: The number of iterations
            first_pass: If True, the ants will visit all the nodes randomly on the first pass
            heuristic: The heuristic function to use"""

        self.graph = graph
        self.start_node = start_node
        if alpha < 0 :
            raise ValueError("alpha must be positive")
        self.alpha = alpha
        if beta < 0 :
            raise ValueError("beta must be positive")
        self.beta = beta
        if rho < 0 or rho > 1:
            raise ValueError("rho must be between 0 and 1")
        self.rho = rho
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.first_pass = first_pass
        self.heuristic = heuristic

        self.ants = []

    def run(self):
        """Run the algorithm"""
        #Create the ants
        best_ant = self.ant(self.graph, self.start_node, self.alpha, self.beta, self.first_pass, self.heuristic)
        best_ant.path = []
        best_ant.distance = float("inf")
        #Run the iterations
        for i in range(self.n_iterations):
            self._iteration()
            if self.first_pass:
                best_ant = self.ants[0]
            for ant in self.ants:
                if ant.distance < best_ant.distance:
                    best_ant = ant
        
        #Find the best ant

        return best_ant.path, best_ant.distance

    def _iteration(self):
        """Run one iteration of the algorithm"""
        #Create the ants
        self.ants = []
        for i in range(self.n_ants):
            self.ants.append(self.ant(self.graph, self.start_node, self.alpha, self.beta, self.first_pass, self.heuristic))

        #Start the ants, they will run in parallel
        for ant in self.ants:
            ant.start()

        #Wait for the ants to finish
        for ant in self.ants:
            ant.join()

        #Update the pheromone
        self._update_pheromone()

        self.first_pass = False
    
    def _update_pheromone(self):
        """Update the pheromone of each edge with the formula on the wikipedia page"""
        for edge in self.graph:
            for edge2 in self.graph[edge]:
                #Remove the pheromone
                if not self.first_pass:
                    self.graph[edge][edge2]["pheromone"] *= (1 - self.rho)
                else:
                    max = 0
                    #If it's the first pass, the pheromone is equal to 1 devided by the maximum distance
                    for ant in self.ants:
                        if ant.distance > max:
                            max = ant.distance
                    self.graph[edge][edge2]["pheromone"] = 1 / max

            #Add the pheromone
        for ant in self.ants:
            for i in range(len(ant.path) - 1):
                self.graph[ant.path[i]][ant.path[i + 1]]["pheromone"] += 1 / ant.distance