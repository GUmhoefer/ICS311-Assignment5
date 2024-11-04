# ICS311-Assignment5

Readme for sea.py and seaofisland.ipynb. Authors: Gregor Umhoefer, Jonathan Lee

Running the seaofisland.ipynb will populate the graph with islands and routes, also demonstrate algorithms 1 and 2. This notebook can be used to test the sea.py graph functions.

Algorithm 1: n_next_best_islands_greedy(island name, number of islands)
  This algorithm simulates a chief visiting multiple islands, specified by the number of islands parameter. It considers island population, recency of last visit, and the distance to the island, to determine the best route to take. Specify the island the chief starts from as the first parameter, and the number of islands to visit as the second.

Algorithm 2: canoe_distribution(source island, maximum path overlap, canoe capacity)
  This algorithm finds the shortest paths from the source to the other islands, and forms a distribution route from the paths. It considers the number of islands reached in the paths, the time they take, and the amount that the paths overlap. Specify the island that the resource comes from, the maximum overlap ratio (between 0 and 1) that the paths can contain, and the canoe capacity. The maximum overlap defaults to .7, lower values will reduce the number of paths added, while higher values will increase the number of paths added. Canoe capacity defaults to 30.

Please contact gregoru@hawaii.edu with any questions or problems.
