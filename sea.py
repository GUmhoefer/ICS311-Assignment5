from heapq import heapify, heappop, heappush

class Sea:
    def __init__(self, islands, routes):
        # Initialize islands from provided data
        self.islands = {name: self.Island(name, **attributes) for name, attributes in islands.items()}
        self.adj = {name: {} for name in islands}

        # Populate adjacency list and add missing islands if needed
        for origin, dest, time in routes:
            # Ensure origin and dest exist in islands and adjacency list
            if origin not in self.islands:
                self.islands[origin] = self.Island(name=origin)
            if dest not in self.islands:
                self.islands[dest] = self.Island(name=dest)
            
            # Ensure both are also in the adjacency list
            if origin not in self.adj:
                self.adj[origin] = {}
            if dest not in self.adj:
                self.adj[dest] = {}

            # Add the route
            self.adj[origin][dest] = time

    class Island:
        def __init__(self, name, pop = 500, last_visit = 0, resource_demand = 12):
            self.name = name # island name
            self.pop = pop # population
            self.last_visit = last_visit # last time the island was visited
            self.resource_demand = resource_demand # island's demand for a rare resource

        def __str__(self):
            return (f"\nIsland: {self.name}\n"
                    f"Population: {self.pop}\n"
                    f"Last visit: {self.last_visit}\n"
                    f"Resource demand: {self.resource_demand}\n")

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
    

    def next_best_island_greedy(self, current_island, current_time, alpha=5, k_factor=2):
        """
        Greedy approach to find the next best directly connected island to visit.
        Ensures last visit time updates correctly to influence recency penalty.

        Args:
            current_island (str): The current island.
            current_time (int): The current time.
            alpha (int): Recency penalty control factor.
            k_factor (int): Population scaling factor.

        Returns:
            dict: Contains the next best island, last visited island, last visit time, and travel time.
        """
        avg_population = sum(island.pop for island in self.islands.values()) / len(self.islands)
        k = k_factor / avg_population

        # Initialize variables to track the best neighboring island
        next_island = None
        min_effective_distance = float('inf')
        travel_time = 0

        print(f"\nEvaluating neighbors for {current_island} at time {current_time}")

        # Consider only direct neighbors of the current island
        for neighbor, time in self.adj[current_island].items():
            last_visit_neighbor = self.islands[neighbor].last_visit
            time_since_last_visit = current_time - last_visit_neighbor + 1
            recency_penalty = alpha / time_since_last_visit

            # Effective distance includes travel time, population scaling, and recency penalty
            effective_distance = time / (self.islands[neighbor].pop * k) + recency_penalty

            # Debug print statements to observe the impact of each component
            print(f"  Neighbor: {neighbor}")
            print(f"    Travel time: {time}")
            print(f"    Population: {self.islands[neighbor].pop}")
            print(f"    Last visit time: {last_visit_neighbor}")
            print(f"    Time since last visit: {time_since_last_visit}")
            print(f"    Recency penalty (alpha / time since last visit): {recency_penalty}")
            print(f"    Effective distance: {effective_distance}")

            # Select the neighbor with the minimum effective distance
            if effective_distance < min_effective_distance:
                min_effective_distance = effective_distance
                next_island = neighbor
                travel_time = time  # Update travel time for the chosen next island

        # Update the last visit time for both the current island and the next island
        if next_island:
            # Update last visit time for the current island before moving
            self.islands[current_island].last_visit = current_time
            # Update time to reflect travel to next island
            current_time += travel_time
            # Set last visit time of the chosen island to the updated current time
            self.islands[next_island].last_visit = current_time

        return {
            "next_island": next_island,
            "last_visited": current_island,
            "last_visit_time": current_time,
            "travel_time": travel_time
        }


    def n_next_best_islands_greedy(self, origin, iterations=15, alpha=50, k_factor=2):
        """
        Finds the sequence of next best islands to visit using the greedy approach with limited lookahead.
        Displays last visit times on each iteration.

        Args:
            origin (str): The starting island.
            iterations (int): Number of moves to find the next best islands.
            alpha (int): Recency penalty control factor.
            k_factor (int): Population scaling factor.

        Returns:
            list: The ordered list of islands in the visitation path.
        """
        current_time = 0
        path = []
        current_island = origin

        for i in range(iterations):
            print(f"\n--- Iteration {i+1} ---")
            
            # Find the next best island based on the greedy approach
            result = self.next_best_island_greedy(current_island, current_time, alpha, k_factor)
            next_island = result["next_island"]
            travel_time = result["travel_time"]

            if next_island is None:
                print("No more reachable islands.")
                break

            # Update the last visit time for the selected next island
            current_time += travel_time
            self.islands[next_island].last_visit = current_time

            # Update path and current state
            path.append(next_island)
            current_island = next_island
            
            # Print the path up to this point
            print(f"Path so far: {' -> '.join(path)}")

        print("\nFinal path taken across islands:", " -> ".join(path))
        return path
    
    def resource_distribution_path(self, origin, max_overlap = .7):
        """
        Finds an optimal combination of paths to deliver to the most islands based on the number of islands in the path and its total time.

        Args:
            origin (str): The starting island.
            max_overlap (float): Maximum overlap fraction allowed between paths for a path to be selected. (0 to 1)

        Returns:
            list: A list containing lists of island sequences in optimal paths chosen.
        """

        # Finds the shortest paths from the origin to all other islands
        paths = self.shortest_path(origin)

        # Sort paths by ascending order of travel time. 
        sorted_paths = self.sort_paths(paths, 0, len(paths) - 1)

        # Create a set to store islands that will be visited in optimal route
        islands_visited = set(origin)

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
            
        return optimal_paths
    
    def canoe_distribution(self, origin, max_overlap = .7, canoe_capacity = 30):
        """
        Assigns canoes to deliver resources to sets of islands along the optimal shortest routes.

        Args:
            origin (str): The starting island that is the source of the rare resources.
            max_overlap (float): Maximum overlap fraction allowed between paths for a path to be selected. (0 to 1)
            canoe_capacity (int): The maximum amount of resources that a canoe can carry. Starts at 0, and are incremented
                by the demand of islands along a path until the capacity is reached, and the canoe is dispatched to 
                deliver to those islands.

        Returns:
            canoe_count: The number of canoes dispatched to cover deliveries.
            distribution_time: The total time taken for canoes to deliver resources.
            islands_delivered: A set of islands that received resources.
        """
        
        # Calculate the best paths to plan canoe routes, set current distribution time to 0
        best_paths = self.resource_distribution_path(origin, max_overlap)
        distribution_time = 0
        islands_delivered = 0

        # Set origin island's demand to 0
        self.islands[origin].resource_demand = 0
        
        # Start with 1 canoe with load of 0
        canoe_count = 1
        canoe_load = 0

        for path in best_paths:
            
            # Initialise variables for current path
            
            current_time = 0

            for i in range(len(path)):
                first = path[i]
    
                # If the current island has demand, load its demand into the canoe
                if self.islands[first].resource_demand > 0:

                    # Increment the number of islands delivered to
                    islands_delivered += 1

                    # Load canoe with enough for the current island, if the canoe has the capacity
                    # and set island's demand to 0 as it will be fulfilled.
                    if (canoe_load + self.islands[first].resource_demand <= canoe_capacity):
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
                    # Add travel time to next island
                    second = path[i + 1]
                    current_time += self.adj[first][second]
                else:
                    # If the current island is the last island in the path, start a new canoe
                    canoe_load = 0
                    canoe_count += 1

            # Determine if the current path's time is longer than any previous path times
            if current_time > distribution_time:
                distribution_time = current_time

        return canoe_count, distribution_time, islands_delivered

    def sort_paths(self, paths, begin, end):
        """
        Sorts a list of paths in ascending order by distance.

        Args:
            paths (list): A list of paths to be sorted.
            begin (int): The starting index of the list.
            end (int): The ending index of the list.

        Returns:
            list: The sorted list of paths.
        """
        if begin >= end:
            # Base case if list has 1 or fewer elements
            return paths
        mid = (begin + end) // 2 # Finds middle of list
        self.sort_paths(paths, begin, mid)
        self.sort_paths(paths, mid + 1, end)

        # Merge left and right lists
        return self.merge(paths, begin, mid, end)
    
    def merge(self, paths, begin, mid, end):
        """
        Merges the recursively subdivided lists of paths back together in sorted order.

        Args:
            paths (list): A list of paths to be sorted.
            begin (int): The starting index of the list.
            end (int): The ending index of the list.

        Returns:
            list: The sorted sub list of paths.
        """
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

        while i < num_left and j < num_right:
            if left[i][0] <= right[j][0]:
                paths[k] = left[i] # Adds the left list's path to the original array if it is shorter than the right path
                i += 1 # Increments to next left path
            else:
                paths[k] = right[j] # Adds the right path to the original array if it is is shorter than the left path
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