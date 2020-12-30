import datetime
from collections import defaultdict

fl  = open("spoje.csv")

mesta = {}

today = datetime.datetime.now().timetuple().tm_yday


class Graph():
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        # self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        # self.weights[(to_node, from_node)] = weight

def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path

graph = Graph()

for x in fl.readlines():
    x = x[:-1]
    splited = x.split(";")
    city_from, city_to, time, duration, bitmap, train_id = splited
    if(not mesta.get(city_from)):
        mesta[city_from] =  {}
    if(not mesta.get(city_from).get(city_to)):
        mesta[city_from][city_to] = []
    mesta[city_from][city_to].append((city_from, city_to, time, int(duration), bitmap, train_id))
    graph.add_edge(city_from, city_to, int(duration))
fl.flush()


print("[s]poje / [z]astavka")
spoj = input("> ")
if(spoj == 's'):
    city_from = input("From: ")
    city_to = input("To: ")
    print(" -> ".join(dijsktra(graph, city_from , city_to)))

elif(spoj == 'z'):
    city_from = input("From: ")

    print(city_from)
    for x in mesta[city_from]:
        print()
        print(2*"-"+"> "+x)
        for city in mesta[city_from][x]:
            if(len(city[4]) >= today):
                if(city[4][today] == "1"):
                    print(4*" "+4*"-"+city[2], city[5])

else:
    print("Bad input.")

