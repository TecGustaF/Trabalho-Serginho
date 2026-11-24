import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def __init__(self, heuristic=None):
        if heuristic is not None:
            self.heuristic = heuristic

    def heuristic(self, state: State) -> int:
        distance = 0
        for i, tile in enumerate(state.tiles):
            if tile != 0:
                r, c = divmod(i, 3)
                gr, gc = divmod(GOAL_STATE.index(tile), 3)
                distance += abs(r - gr) + abs(c - gc)
        return distance

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)
        order = count()
        frontier = [(initial.cost + self.heuristic(initial), next(order), initial)]
        best_cost = {initial: initial.cost}
        while frontier:
            _, _, current = heapq.heappop(frontier)
            if current.cost != best_cost[current]:
                continue
            if current.is_goal:
                result.solution = current
                result.depth = len(current.path()) - 1
                return result
            result.nodes_expanded += 1
            for child in current.neighbors():
                result.nodes_generated += 1
                if child.cost < best_cost.get(child, float("inf")):
                    best_cost[child] = child.cost
                    priority = child.cost + self.heuristic(child)
                    heapq.heappush(frontier, (priority, next(order), child))
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))
        return result
