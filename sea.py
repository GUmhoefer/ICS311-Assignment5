class Sea:
    def __init__(self):
        self.islands = {}
        self.adj = {}

    class Island:
        def __init__(self, name, pop = 500, chief_skill = False, rare_shell = 0):
            self.name = name
            self.pop = pop
            self.chief_skill = chief_skill
            self.rare_shell = rare_shell

        def __str__(self):
            return (f"\nIsland: {self.name}\n"
                    f"Population: {self.pop}\n"
                    f"Chief's Skill: {self.chief_skill}\n"
                    f"Rare Shell: {self.rare_shell}\n\n")

    def add_island(self, name, pop = 500, chief_skill = False, rare_shell = 0):
        self.islands[name] = self.Island(name, pop, chief_skill, rare_shell)
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
        else:
            shortest = {}
            shortest[origin] = 0
            paths = {island: [] for island in self.adj.keys() if island != origin}
        print(paths)
        print(shortest)

        # Still working on this, will eventually be Dijkstra's

 
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
        for name in self.islands:
            print(self.islands[name])

    def print_island_names(self):
        for n in self.islands.keys():
            print(n)

    def print_neighbours(self, name):
        for dest, _ in self.adj[name].items():
            print(f"{name} has a route to {dest}")

        
    