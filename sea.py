from heapq import heapify, heappop, heappush

class Sea:
    def __init__(self, islands, routes):
        self.islands = {name: self.Island(name, **attributes) for name, attributes in islands.items()}
        self.adj = {name: {} for name in islands}
        
        for origin, dest, time in routes:
            if origin in self.adj and dest in self.adj:
                self.adj[origin][dest] = time

    class Island:
        def __init__(self, name, pop = 500, last_visit = None, rare_shell=0, resources=None):
            self.name = name # island name
            self.pop = pop # population
            self.last_visit = last_visit # last time the island was visited
            self.rare_shell = rare_shell
            self.resources = resources if resources else {} # resources on the island as a dictionary: {name, quantity}
            self.parent = None

        def __str__(self):
            return (f"\nIsland: {self.name}\n"
                    f"Population: {self.pop}\n"
                    f"Last visit: {self.last_visit}\n"
                    f"Rare shell: {self.rare_shell}\n"
                    f"Resources: {self.resources}\n\n")

    def add_island(self, name, pop = 500, last_visit = None, rare_shell=0, resources=None):
        self.islands[name] = self.Island(name, pop, last_visit, rare_shell)
        self.adj[name] = {}

    def add_route(self, origin, dest, time):
        if origin not in self.adj:
            self.add_island(origin)
        self.adj[origin][dest] = time

    def print_routes(self):
        for origin in self.adj:
            for dest, time in self.adj[origin].items():
                print(f"From {origin} to {dest} takes {time}")


    def shortest_paths(self, origin):
        """
        Compute the shortest paths from the origin island to all other islands using Dijkstra's algorithm.

        Args:
            origin (str): The name of the origin island.

        Returns:
            dict: A dictionary with islands as keys and tuples (distance, path) as values.
        """
        if origin not in self.adj:
            return f"{origin} is not an island in the routes"
        
        # Initialize distances with infinity and set the distance to the origin as 0
        distances = {island: float('inf') for island in self.islands}
        distances[origin] = 0

        # Priority queue to process islands, starting with origin island
        priority_queue = [(0, origin)]

        # Dictionary to store the shortest paths to each island
        shortest_paths = {island: [] for island in self.islands if island != origin}
        shortest_paths[origin] = [origin]

        while priority_queue:
            current_distance, current_island = heappop(priority_queue)

            # Skip if the current distance is longer than the shortest known distance
            if current_distance > distances[current_island]:
                continue

            # Check neighbors of the current island
            for neighbor, time in self.adj[current_island].items():
                distance = current_distance + time # Calculate distance to be the current distance plus the travel time

                # If a shorter path to the neighbor is found, update the path and distance
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heappush(priority_queue, (distance, neighbor))
                    shortest_paths[neighbor] = shortest_paths[current_island] + [neighbor]

        # Return the shortest distances and paths to each island
        return {island: (distances[island], shortest_paths[island]) for island in self.islands}
    

    def next_best_island(self, current_island, current_time, alpha=5, k_factor=2):
        """
        Find the next best island to visit, given the current island, current time, and control factors.

        Args:
            current_island (str): The name of the current island.
            current_time (int): The current time.
            alpha (int, optional): The control factor for the recency penalty. Defaults to 5 (larger value means revisits are more strongly discouraged).
            k_factor (int, optional): The scaling factor for the population. Defaults to 2 (larger value means larger populations have more influence on the next best island).
        Returns:
            dict: A dictionary containing the next best island, the last visited island, and the last visit time.
        """
        avg_population = sum(island.pop for island in self.islands.values()) / len(self.islands)
        k = k_factor / avg_population
        
        if current_island not in self.adj:
            return f"{current_island} is not an island in the routes"
        
        distances = {island: float('inf') for island in self.islands}
        distances[current_island] = 0
        priority_queue = [(0, current_island)]
        self.islands[current_island].last_visit = current_time

        last_visited = current_island
        last_visit_time = current_time
        next_island = None

        while priority_queue:
            current_distance, current_island = heappop(priority_queue)
            
            # Update last visited information
            last_visited = current_island
            last_visit_time = current_time

            if current_distance > distances[current_island]:
                continue

            # Look for the next best island
            for neighbor, travel_time in self.adj[current_island].items():
                last_visit_neighbor = self.islands[neighbor].last_visit or 0
                recency_penalty = 1 / (current_time - last_visit_neighbor + 1)
                # Compute the effective distance using population scaling factor and recency penalty
                effective_distance = current_distance + travel_time / (self.islands[neighbor].pop * k) + alpha * recency_penalty 
                
                if effective_distance < distances[neighbor]:
                    distances[neighbor] = effective_distance
                    heappush(priority_queue, (effective_distance, neighbor))
                    
                    # Select this neighbor as the next island to visit
                    next_island = neighbor
                    current_time += travel_time  # Update time after traveling to the neighbor (thus, higher times mean more recent times)
                    # Update last_visit for the current island before moving on
                    self.islands[current_island].last_visit = current_time
                    break  # Stop after finding the next best island

            # Exit the loop early after selecting the next island
            if next_island:
                break

        # Return the next best island, the last visited island, and the last visit time as dictionary of strings
        return {
            "next_island": next_island,
            "last_visited": last_visited,
            "last_visit_time": last_visit_time
        }

    def n_next_best_islands(sea, origin, iterations=15):
        """
        Given a Sea object and an origin island, find the next best island to visit
        for a given number of iterations (trips between islands).

        The algorithm (next_best_island)takes into account the population of the islands and the
        recency of the last visit to each island when determining the next best
        island to visit.

        Args:
            sea (Sea): The Sea object to use for the algorithm
            origin (str): The origin island to start at
            iterations (int, optional): The number of iterations to run the
                algorithm for. Defaults to 15.

        Returns:
            A list of the next best islands to visit in order
        """
        current_time = 0
        path = []
        current_island = origin

        for i in range(iterations):
            print(f"\n--- Iteration {i+1} ---")
            result = sea.next_best_island(current_island, current_time)
            
            next_island = result["next_island"] 
            last_visited = result["last_visited"]
            last_visit_time = result["last_visit_time"]

            if next_island is None:
                print("No more reachable islands.")
                break

            # Print the results for this iteration
            print(f"Current Island: {current_island}")
            print(f"Next Island to Visit: {next_island}")
            print(f"Last Visited Island: {last_visited}")
            print(f"Last Visit Time: {last_visit_time}")

            # Append the path for visualization
            path.append(next_island)

            # Update current_time and move to the next island
            travel_time = sea.adj[current_island].get(next_island, 0)
            current_time += travel_time
            sea.islands[current_island].last_visit = current_time

            # Move to the next island
            current_island = next_island

        # Print the full path taken
        print("\nPath taken across islands:", " -> ".join(path))
    def find_route(self, origin, dest):
        if origin not in self.adj:
            return f"{origin} is not an island in the routes"
        elif dest not in self.adj:
            return f"{dest} is not an island in the routes"
        else:
            for destination, time in self.adj[origin].items():
                if destination == dest:
                    return f"From {origin} to {dest} takes {time}"
            return "No route found"
    
    def find_shortest_route(self, origin):
        if origin not in self.adj:
            return f"{origin} is not an island in the routes"
        else:
            short_dest, short_time = min(self.adj[origin].items(), key = lambda route: route[1])
            

            return f"From {origin} to {short_dest} takes {short_time}"

    def print_island(self, name):
        print(self.islands[name])
    
    def print_all_islands(self):
        for name, island in self.islands.items():
            print(island)

    def print_island_names(self):
        for n in self.islands.keys():
            print(n)

    def print_neighbours(self, name):
        for dest, _ in self.adj[name].items():
            print(f"{name} has a route to {dest}")