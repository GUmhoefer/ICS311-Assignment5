from sea import Sea as ocean

def main():
    pacific = ocean()

    pacific.add_island("Tonga", 1000, True, 1)
    pacific.add_island("Samoa", 2000, False, 0)
    pacific.add_island("Fiji", 1500, False, 2)

    pacific.add_route("Tonga", "Samoa", 5)
    pacific.add_route("Tonga", "Fiji", 10)
    pacific.add_route("Samoa", "Fiji", 5)
    pacific.add_route("Fiji", "Tonga", 15)
    pacific.add_route("Fiji", "Samoa", 20)

    pacific.print_routes()
    pacific.print_island("Tonga")

    pacific.print_all_islands()

    pacific.print_neighbours("Tonga")

    print(pacific.find_route("Tonga", "Samoa"))
    print(pacific.find_route("Samoa", "Tonga"))
    print(pacific.find_route("Tonga", "Fiji"))
    print(pacific.find_route("Fiji", "Aotearoa"))
    print(pacific.find_route("Aotearoa", "Tonga"))

    pacific.shortest_paths("Tonga")

    print(pacific.find_shortest_route("Tonga"))

main()
