from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)
        frontier = [(initial, 0)]
        best_depth = {initial: 0}
        while frontier:
            current, depth = frontier.pop()
            if depth != best_depth[current]:
                continue
            if current.is_goal:
                result.solution = current
                result.depth = depth
                return result
            if depth >= self.depth_limit:
                continue
            result.nodes_expanded += 1
            for child in reversed(current.neighbors()):
                result.nodes_generated += 1
                if depth + 1 < best_depth.get(child, float("inf")):
                    best_depth[child] = depth + 1
                    frontier.append((child, depth + 1))
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))
        return result
