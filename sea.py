from heapq import heapify, heappop, heappush

class Sea:
    def __init__(self, islands, routes):
        self.islands = {name: self.Island(name, **attributes) for name, attributes in islands.items()}
        self.adj = {name: {} for name in islands}
        
        for origin, dest, time in routes:
            if origin in self.adj and dest in self.adj:
                self.adj[origin][dest] = time

    class Island:
        def __init__(self, name, pop = 500, last_visit = None, rare_shell=0, resources=None, resource_demand = 12):
            self.name = name # island name
            self.pop = pop # population
            self.last_visit = last_visit # last time the island was visited
            self.rare_shell = rare_shell
            self.resources = resources if resources else {} # resources on the island as a dictionary: {name, quantity}
            self.resource_demand = resource_demand # island's demand for a rare resourc

        def __str__(self):
            return (f"\nIsland: {self.name}\n"
                    f"Population: {self.pop}\n"
                    f"Last visit: {self.last_visit}\n"
                    f"Rare shell: {self.rare_shell}\n"
                    f"Resources: {self.resources}\n\n"
                    f"Resource demand: {self.resource_demand}\n")

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


    def shortest_path(self, origin):
        """
        Compute the shortest paths from the origin island to all other islands using Dijkstra's algorithm.

        Args:
            origin (str): The name of the origin island.

        Returns:
            distances (dict): The shortest distances to each island from the origin.
            shortest_paths (dict): The shortest paths to each island from the origin.
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
        return [(distances[island], shortest_paths[island]) for island in self.islands if island != origin]
    

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
    
    def resource_distribution_path(self, origin, max_overlap, alpha, beta):
        # distances, path_dict = self.shortest_path(origin)
        # all_paths = [path for path in path_dict.values()]

        paths = self.shortest_path(origin)

        # Sort paths by decreasing optimal value
        # Optimal value = a * 1/total_time + b * unique_islands
        sorted_paths = self.sort_paths(paths, 0, len(paths) - 1, alpha, beta)

        # sorted_paths = paths

        # # Sort shortest paths by decreasing number of islands in the path
        # sorted_paths = self.sort_paths(all_paths, 0, len(all_paths) - 1)

        # Create a set to store islands that will be visited in optimal route
        islands_visited = set()

        # Create a list to store the optimal paths
        optimal_paths = []

        # Iterate through the sorted from longest to shortest
        for path in sorted_paths:

            # Create a set from the path for set operations
            path_set = set(path[1])

            # Calculate ratio of overlap between path and visited islands
            ratio = len(path_set.intersection(islands_visited)) / len(path_set)

            # Allow only a certain amount of overlap between paths chosen to
            # avoid revisiting too many islands, while maximising coverage.
            if ratio < max_overlap:

                # Add the path to the optimal paths
                optimal_paths.append(path[1])

                # Update the visited islands set
                islands_visited.update(path_set)
            
        return optimal_paths, sorted_paths
    
    def canoe_distribution(self, origin, max_overlap = .6, alpha = .1, beta = .0001):
        canoe_capacity = 30
        best_paths, sort = self.resource_distribution_path(origin, max_overlap, alpha, beta)
        distribution_time = 0
        canoe_count = 0
        islands_delivered = set()

        for path in best_paths:

            current_time = 0
            canoe_load = 0

            for i in range(len(path)):
                first = path[i]

                if first not in islands_delivered:
                    islands_delivered.add(first)

                if canoe_load + self.islands[first].resource_demand <= canoe_capacity:
                    canoe_load += self.islands[first].resource_demand
                    self.islands[first].resource_demand = 0

                else: 

                    # Send canoe with exactly enough resources to meet the demands for 
                    # the islands so far. Start loading new canoe with resources for the 
                    # current island.
                    canoe_count += 1
                    canoe_load = self.islands[first].resource_demand
                    self.islands[first].resource_demand = 0
                
                # If current island is not the last island in the path, add travel time to next island
                if i < len(path) - 1:
                    second = path[i + 1]
                    current_time += self.adj[first][second]

            # Determine if the current path time is longer than any previous path times
            if current_time > distribution_time:
                distribution_time = current_time

        return canoe_count, distribution_time, islands_delivered
    
    def calc_path_score(self, path, alpha, beta):
        score = alpha * (1/path[0]) + beta * len(path[1])
        # score = (beta * len(path[1])) / (alpha * path[0])
        return score

    def sort_paths(self, paths, begin, end, alpha, beta):
        if begin >= end:
            # Base case if list has 1 or fewer elements
            return paths
        mid = (begin + end) // 2 # Finds middle of list
        self.sort_paths(paths, begin, mid, alpha, beta)
        self.sort_paths(paths, mid + 1, end, alpha, beta)

        # Merge left and right lists
        return self.merge(paths, begin, mid, end, alpha, beta)
    
    def merge(self, paths, begin, mid, end, alpha, beta):
        # Sets the number of elements in the left and right lists
        num_left = mid - begin + 1
        num_right = end - mid

        # Creates two arrays for the left and right lists
        left = [0] * num_left
        right = [0] * num_right

        # Fills the new left and right arrays with the paths from the original array
        for i in range(0, num_left):
            left[i] = paths[begin + i]
        for j in range(0, num_right):
            right[j] = paths[mid + j + 1]
        
        # Sets start indices for left, right, and original lists
        i = 0
        j = 0
        k = begin

        # while i < num_left and j < num_right:
        #     if len(left[i][1]) <= len(right[j][1]):
        #         paths[k] = left[i] # Adds the left list's path to the original array if it is longer than the right path
        #         i += 1 # Increments to next left path
        #     else:
        #         paths[k] = right[j] # Adds the right path to the original array if it is is less than the left path
        #         j += 1 # Increments index to next right path
        #     k += 1 # Increments the position in the original array

        while i < num_left and j < num_right:
            if self.calc_path_score(left[i], alpha, beta) <= self.calc_path_score(right[j], alpha, beta):
                paths[k] = left[i] # Adds the left list's path to the original array if it is longer than the right path
                i += 1 # Increments to next left path
            else:
                paths[k] = right[j] # Adds the right path to the original array if it is is less than the left path
                j += 1 # Increments index to next right path
            k += 1 # Increments the position in the original array

        # After one of the L or R lists is empty, adds the rest of the other list to the original array
        while i < num_left:
            paths[k] = left[i]
            i += 1
            k += 1
        
        while j < num_right:
            paths[k] = right[j]
            j += 1
            k += 1

        return paths

    # Testing methods for Sea class
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