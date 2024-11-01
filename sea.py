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
            self.name = name
            self.pop = pop
            self.last_visit = last_visit
            self.rare_shell = rare_shell
            self.resources = resources if resources else {}
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
        if origin not in self.adj:
            return f"{origin} is not an island in the routes"
        
        distances = {island: float('inf') for island in self.islands}
        distances[origin] = 0
        priority_queue = [(0, origin)]
        shortest_paths = {island: [] for island in self.islands if island != origin}
        shortest_paths[origin] = [origin]

        while priority_queue:
            current_distance, current_island = heappop(priority_queue)

            if current_distance > distances[current_island]:
                continue

            for neighbor, time in self.adj[current_island].items():
                distance = current_distance + time

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heappush(priority_queue, (distance, neighbor))
                    shortest_paths[neighbor] = shortest_paths[current_island] + [neighbor]

        return {island: (distances[island], shortest_paths[island]) for island in self.islands}

 
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