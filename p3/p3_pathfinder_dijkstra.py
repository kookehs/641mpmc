from heapq import heappop, heappush
from math import sqrt

def distance(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    dist = sqrt(dx * dx + dy * dy)

    return dist

def navigation_edges(mesh, points, cell):
    edges = []

    for edge in mesh["adj"][cell[1]]:
        x1 = points[cell[1]][0]
        y1 = points[cell[1]][1]
        point1 = (x1, y1)
        x2 = min(edge[1] - 1, max(edge[0], points[cell[1]][0]))
        y2 = min(edge[3] - 1, max(edge[2], points[cell[1]][1]))
        point2 = (x2, y2)
        dist = distance(point1, point2)
        edges.append((dist + cell[0], edge))

    return edges

def dijkstras(src, dst, src_rect, dst_rect, mesh, adj):
    dist = {}
    prev = {}
    detail_points = {}
    dist[src_rect] = 0
    prev[src_rect] = None
    detail_points[src_rect] = src
    heap = [(dist[src_rect], src_rect)]

    while heap:
        node = heappop(heap)

        if node[1] == dst_rect:
            break

        for next_node in adj(mesh, detail_points, node):
            if next_node[1] not in dist or next_node[0] < dist[next_node[1]]:
                dist[next_node[1]] = next_node[0]
                prev[next_node[1]] = node[1]
                x = min(next_node[1][1] - 1, max(next_node[1][0], detail_points[node[1]][0]))
                y = min(next_node[1][3] - 1, max(next_node[1][2], detail_points[node[1]][1]))
                detail_points[next_node[1]] = (x, y)
                heappush(heap, next_node)

    visited = detail_points.keys()
    detail_points[dst_rect] = dst

    if node[1] == dst_rect:
        path = []
        node = node[1]

        while node:
            point1 = detail_points[node]

            if prev[node] != None:
                point2 = detail_points[prev[node]]
            else:
                point2 = src

            path.append((point1, point2))
            node = prev[node]

        path.reverse()

        return path, visited
    else:
        return [], visited

def aabb_contains(point, rect):
    if point[0] >= rect[0] and point[0] <= rect[1] and point[1] >= rect[2] and point[1] <= rect[3]:
        return True

    return False

def find_path(src, dst, mesh):
    src_rect = None;
    dst_rect = None;

    for box in mesh["boxes"]:
        if aabb_contains(src, box):
            src_rect = box
        if aabb_contains(dst, box):
            dst_rect = box
        if src_rect != None and dst_rect != None:
            break

    path = []
    discovered = []

    if src_rect != None and dst_rect != None:
        path, discovered = dijkstras(src, dst, src_rect, dst_rect, mesh, navigation_edges)
    else:
        print("No path!")

    if path == []:
        print("No path!")

    return [path, discovered]
    pass
