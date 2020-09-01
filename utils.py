
# Note: This Queue class is sub-optimal. Why?
class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


def get_vertex_neighbors(graph, room):
    return graph[room].values()


def bfs(graph, starting_vertex):
    visited = set()
    queue = Queue()
    queue.enqueue([starting_vertex])

    while queue.size() > 0:
        current_path = queue.dequeue()

        current_vertex = current_path[-1]

        if current_vertex not in visited:
            neighbors = get_vertex_neighbors(graph, current_vertex)

            for neighbor in neighbors:
                new_path = list(current_path)
                new_path.append(neighbor)
                queue.enqueue(new_path)

                if neighbor == "?":
                    return new_path
            visited.add(current_vertex)


def dfs(graph, starting_vertex):
    visited = set()
    stack = Stack()
    stack.push([starting_vertex])

    while stack.size() > 0:
        current_path = stack.pop()
        current_vertex = current_path[-1]

        if current_vertex not in visited:
            neighbors = get_vertex_neighbors(graph, current_vertex)
            for neighbor in neighbors:
                new_path = [current_path]
                new_path.append(neighbor)
                stack.push(new_path)

                if neighbor == '?':
                    return new_path
            visited.add(current_vertex)


def closest_unexplored_room(graph, current_room):

    # We can run a BFS to find the closest node which satisfies our condition of having an unexplored edge.
    unexplored = bfs(graph, current_room)

    print("Here's what remains: ", unexplored)
    path = []

    for i in range(0, len(unexplored) - 1):
        graph_list = list(graph[unexplored[i]].items())
        direction = ''

        for entry in graph_list:
            if entry[1] == unexplored[i + 1]:
                direction = entry[0]
        path.append(direction)
    return path
