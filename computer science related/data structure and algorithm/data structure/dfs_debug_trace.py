graph = {
    "fastapi": ["pydantic", "starlette"],
    "pydantic": ["typing-extensions"],
    "starlette": ["typing-extensions"],
    "typing-extensions": [],
}

## Example C: BFS (queue-based)
from collections import deque


def bfs(graph, start):
    q = deque([start])
    seen = {start}

    while q:
        node = q.popleft()  # break for queue status
        yield node  # break for yielding
        for nxt in graph[node]:
            if nxt not in seen:  # break for each node and seen status
                seen.add(nxt)
                q.append(nxt)  # break for queue and seen update


for node in bfs(graph, "fastapi"):
    print(node)
