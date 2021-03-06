"""
https://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
graph = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}
"""
from typing import List, Set

class Graph:
    X = [(-1, -1), (-1, 1), (1, -1), (1, 1)]   # Vertex located diagonally from point
    Plus = [(-1, 0), (0, -1), (0, 1), (1, 0)]  # Vertex located horizontally and vertically from point

    @staticmethod
    def decorator_hex(land_map: Set[str], i: str, j: int):
        if i+str(j) in land_map and i in 'ABCDEFGHIJKL' and j in range(1, 10):
            return i + str(j)

    @staticmethod
    def prepare_graph_hex(land_map: Set[str]) -> dict:
        dict_of_cells = {}
        for i in land_map:
            one_cell = set()
            if i[0] in 'ACEGIK':
                one_cell.add(Graph.decorator_hex(land_map, chr(ord(i[0]) - 1), int(i[1]) - 1))  # l
                one_cell.add(Graph.decorator_hex(land_map, chr(ord(i[0]) - 1), int(i[1])))      # l
                one_cell.add(Graph.decorator_hex(land_map, chr(ord(i[0]) + 1), int(i[1]) - 1))  # r
                one_cell.add(Graph.decorator_hex(land_map, chr(ord(i[0]) + 1), int(i[1])))      # r
            else:  # 'BDFHJL'
                one_cell.add(Graph.decorator_hex(land_map, chr(ord(i[0]) - 1), int(i[1])))      # l
                one_cell.add(Graph.decorator_hex(land_map, chr(ord(i[0]) - 1), int(i[1]) + 1))  # l
                one_cell.add(Graph.decorator_hex(land_map, chr(ord(i[0]) + 1), int(i[1])))      # r
                one_cell.add(Graph.decorator_hex(land_map, chr(ord(i[0]) + 1), int(i[1]) + 1))  # r
            one_cell.add(Graph.decorator_hex(land_map, chr(ord(i[0])), int(i[1]) - 1))
            one_cell.add(Graph.decorator_hex(land_map, chr(ord(i[0])), int(i[1]) + 1))
            try:
                one_cell.remove(None)
            except KeyError:
                pass
            dict_of_cells.update({i: one_cell})
        return dict_of_cells

    @staticmethod
    def decorator(land_map: List[List[int]], i, j, unlimited: bool):
        try:
            if (land_map[i][j] != 0 or unlimited) and i >= 0 and j >= 0:
                return i, j
        except IndexError:
            pass

    """
    prepare_graph(land_map: list, diagonal: bool) returns dict of vertex connected horizontally,
    vertically and/or diagonally (diagonal: bool). The condition to connect values in matrix is
    != 0 or w/o restrictions - connect every single element with the next one (unlimited: bool). 
    Use result in dfs, dfs_path, bfs, bfs_path methods as first input parameter. 
    [[1, 0, 1, 0],
     [1, 0, 0, 1],
     [0, 1, 0, 1]]
         ||
         \/
    {(1, 3): {(2, 3), (0, 2)}, (2, 3): {(1, 3)}, (2, 1): {(1, 0)},
     (1, 0): {(0, 0), (2, 1)}, (0, 2): {(1, 3)}, (0, 0): {(1, 0)}}
    """
    @staticmethod
    def prepare_graph(land_map: List[List[int]], diagonal: bool, unlimited: bool) -> dict:
        dict_of_cells = {}
        for i in range(len(land_map)):
            for j in range(len(land_map[i])):
                one_cell = set()
                if land_map[i][j] != 0 or unlimited:
                    if diagonal:
                        for g in Graph.X:
                            one_cell.add(Graph.decorator(land_map, i + g[0], j + g[1], unlimited))  # d
                    for g in Graph.Plus:
                        one_cell.add(Graph.decorator(land_map, i + g[0], j + g[1], unlimited))      # v
                    try:
                        one_cell.remove(None)
                    except KeyError:
                        pass
                    dict_of_cells.update({(i, j): one_cell})
        return dict_of_cells

    """
    {(1, 3): {(2, 3), (0, 2)}, (2, 3): {(1, 3)}, (2, 1): {(1, 0)},
     (1, 0): {(0, 0), (2, 1)}, (0, 2): {(1, 3)}, (0, 0): {(1, 0)}}
         ||
         \/
    island returns list of sets with coordinates of islands w/ or w/o diagonal connections
    [{(1, 3), (2, 3), (0, 2)}, {(1, 0), (0, 0), (2, 1)}]
    """
    @staticmethod
    def island(graph: dict) -> List[set]:
        list_of_islands = []
        for i in graph:
            cell_path = Graph.dfs(graph, i)
            if cell_path not in list_of_islands:
                list_of_islands.append(cell_path)
        return list_of_islands

    @staticmethod
    def dfs(graph, start):
        visited, stack = set(), [start]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                stack.extend(graph[vertex] - visited)
        return visited

    @staticmethod
    def dfs_paths(graph, start, goal):
        stack = [(start, [start])]
        while stack:
            (vertex, path) = stack.pop()
            for next in graph[vertex] - set(path):
                if next == goal:
                    yield path + [next]
                else:
                    stack.append((next, path + [next]))

    @staticmethod
    def dfs_paths_recursion(graph, start, goal, path=None):
        if path is None:
            path = [start]
        if start == goal:
            yield path
        for next in graph[start] - set(path):
            yield from Graph.dfs_paths_recursion(graph, next, goal, path + [next])

    @staticmethod
    def bfs_paths(graph, start, goal):
        queue = [(start, [start])]
        while queue:
            (vertex, path) = queue.pop(0)
            for next in graph[vertex] - set(path):
                if next == goal:
                    yield path + [next]
                else:
                    queue.append((next, path + [next]))
