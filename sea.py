class Sea:
    def __init__(self):
        self.islands = {}
        self.routes = {}
        self.adj = {}

    class Island:
        def __init__(self, name, pop = 500, chief_skill = False, rare_shell = 0)
            self.name = name
            self.pop = pop
            self.chief_skill = chief_skill
            self.rare_shell = rare_shell

    class Route:
        def __init__(self, origin, dest, time):
            self.origin = origin
            self.dest = dest
            self.time = time

    def add_island(self, name, pop = 500, chief_skill = False, rare_shell = 0):
        self.islands[name] = self.Island(name, pop, chief_skill, rare_shell)
        self.adj[name] = []

    def add_route(self, origin, dest, time):
        if origin not in self.routes:
            self.routes[origin] = []
        self.routes[origin].append(self.Route(origin, dest, time))

