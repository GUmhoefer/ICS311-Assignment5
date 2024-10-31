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

    def add_island(self, name, pop = 500, chief_skill = False, rare_shell = 0):
        self.islands[name] = self.Island(name, pop, chief_skill, rare_shell)
        self.adj[name] = []

    def add_route(self, origin, dest, time):
        if origin not in self.adj:
            self.add_island(origin)
        self.adj[origin].append(((dest, time)))

    def print_routes(self):
        for origin in self.adj:
            for dest, time in self.adj[origin]:
                print(f"From {origin} to {dest} takes {time} hours")