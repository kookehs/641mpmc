from p1_support import load_level, show_level
from math import sqrt
from heapq import heappush, heappop

def dijkstras_shortest_path(src, dst, graph, adj):
    dist = {}
    prev = {}
    dist[src] = 0
    prev[src] = None
    heap = [(dist[src], src)]


    while heap:
        node = heappop(heap)

        if node[1] == dst:
            break

        for next_node in adj(graph, node):
            alt = dist[node[1]] + next_node[0]

            if next_node[1] not in dist or alt < dist[next_node[1]]:
                dist[next_node[1]] = alt
                prev[next_node[1]] = node[1]
                heappush(heap, next_node)

    if node[1] == dst:
        path = []
        node = node[1]
        while node:
            path.append(node)
            node = prev[node]
        path.reverse()

        return path
    else:
        return []

def navigation_edges(level, cell):
    edges = []
    x, y = cell[1]

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            next_cell = (x + dx, y + dy)
            dist = sqrt(dx * dx + dy * dy)

            if dist > 0 and next_cell in level['spaces']:
                edges.append((dist + cell[0], next_cell))

    return edges

def test_route(filename, src_waypoint, dst_waypoint):
    level = load_level(filename)
    show_level(level)
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)

    if path:
        show_level(level, path)
    else:
        print("No path possible!")

if __name__ ==  '__main__':
    import sys
    _, filename, src_waypoint, dst_waypoint = sys.argv
    test_route(filename, src_waypoint, dst_waypoint)
