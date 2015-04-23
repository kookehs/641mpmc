from heapq import heappop, heappush
from math import sqrt

def distance(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    dist = sqrt(dx * dx + dy * dy)

    return dist

def navigation_edges(mesh, forward_points, backward_points, forward_distances, backward_distances, cell):
    edges = []

    for edge in mesh["adj"][cell[1]]:
        if forward_points.get(cell[1]) != None:
            x1 = forward_points[cell[1]][0]
            y1 = forward_points[cell[1]][1]
        elif backward_points.get(cell[1]) != None:
            x1 = backward_points[cell[1]][0]
            y1 = backward_points[cell[1]][1]
        point1 = (x1, y1)
        x2, y2 = closest(point1, edge)
        point2 = (x2, y2)
        dist = distance(point1, point2)

        if forward_distances.get(cell[1], None) != None:
            edges.append((dist + forward_distances[cell[1]], edge, cell[2]))
        elif backward_distances.get(cell[1], None) != None:
            edges.append((dist + backward_distances[cell[1]], edge, cell[2]))

    return edges

def closest(current, next_node):
    x = min(next_node[1], max(next_node[0], current[0]))
    y = min(next_node[3], max(next_node[2], current[1]))

    return x, y

def bidrectional_astar(src, dst, src_rect, dst_rect, mesh, adj):
    forward_dist = {}
    forward_prev = {}
    backward_dist = {}
    backward_prev = {}
    forward_detail_points = {}
    backward_detail_points = {}
    forward_dist[src_rect] = 0
    forward_prev[src_rect] = None
    backward_dist[dst_rect] = 0
    backward_prev[dst_rect] = None
    forward_detail_points[src_rect] = src
    backward_detail_points[dst_rect] = dst
    heap = [(forward_dist[src_rect], src_rect, dst_rect), (backward_dist[dst_rect], dst_rect, src_rect)]

    while heap:
        node = heappop(heap)

        if node[1] in forward_prev and node[1] in backward_prev:
            break

        for next_node in adj(mesh, forward_detail_points, backward_detail_points, forward_dist, backward_dist, node):
            if next_node[2] == dst_rect and (next_node[1] not in forward_dist or next_node[0] < forward_dist[next_node[1]]):
                forward_dist[next_node[1]] = next_node[0]
                forward_prev[next_node[1]] = node[1]
                x, y = closest(forward_detail_points[node[1]], next_node[1])
                forward_detail_points[next_node[1]] = (x, y)
                new_dist = next_node[0] + distance((x, y), dst)
                heappush(heap, (new_dist, next_node[1], next_node[2]))
            elif next_node[2] == src_rect and (next_node[1] not in backward_dist or next_node[0] < backward_dist[next_node[1]]):
                backward_dist[next_node[1]] = next_node[0]
                backward_prev[next_node[1]] = node[1]
                x, y = closest(backward_detail_points[node[1]], next_node[1])
                backward_detail_points[next_node[1]] = (x, y)
                new_dist = next_node[0] + distance((x, y), src)
                heappush(heap, (new_dist, next_node[1], next_node[2]))

    if node[1] in forward_prev and node[1] in backward_prev:
        forward_path = []
        backward_path = []
        node1 = node[1]
        node2 = node[1]
        mid_box = node[1]

        while node1 or node2:
            if node1:
                point1 = forward_detail_points[node1]

                if forward_prev[node1] != None:
                    point2 = forward_detail_points[forward_prev[node1]]
                else:
                    point2 = src

                if point2 != point1:
                    forward_path.append((point2, point1))

                node1 = forward_prev[node1]

            if node2:
                point3 = backward_detail_points[node2]

                if backward_prev[node2] != None:
                    point4 = backward_detail_points[backward_prev[node2]]
                else:
                    point4 = dst

                if point3 != point4:
                    backward_path.append((point3, point4))

                node2 = backward_prev[node2]

        forward_path.reverse()
        forward_path.append((forward_detail_points[mid_box], backward_detail_points[mid_box]))

        return forward_path + backward_path, forward_detail_points.keys() + backward_detail_points.keys()
    else:
        return [], forward_detail_points.keys() + backward_detail_points.keys()

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
        path, discovered = bidrectional_astar(src, dst, src_rect, dst_rect, mesh, navigation_edges)
    else:
        print("No path!")

    if path == []:
        print("No path!")

    return path, discovered
