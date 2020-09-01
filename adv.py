from room import Room
from player import Player
from world import World

from utils import Stack, Queue, get_vertex_neighbors, bfs, dfs, closest_unexplored_room

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

traversal_path = []

reverse = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}


def traverse(player):

    # I want to avoid unnecessary travel if possible, so I create a set.
    visited = set()

    # I add the current room to the set.
    visited.add(player.current_room)

    # I initialize a stack to keep track of which nodes are coming next.
    stack = Stack()

    # I initiate a graph to fill out the adjacency list.
    graph = {}

    # For each entry in the graph, I'm going to initialize a dictionary at that room's id.
    graph[player.current_room.id] = {}

    # I'll populate a variable with all possible exits to that room.
    exits = player.current_room.get_exits()

    # For each of those exits, I'll add a new entry into the graph[current_room][direction] slot. Since I don't know what's in that direction just yet, I'll just add a question mark ('?')
    for direction in exits:
        graph[player.current_room.id][direction] = '?'

    # We use a list comprehension to map through our currently unexplored rooms and add them to our list. We only add them if they have not been marked off our adjacency list yet.
    unexplored_rooms = [
        direction[0] for direction in graph[player.current_room.id].items() if direction[1] == '?']

    direction = unexplored_rooms[random.randint(0, len(unexplored_rooms) - 1)]

    stack.push(direction)

    while len(visited) < len(world.rooms):

        # This is going to be our first item that we use to move.
        direction = stack.pop()

        # We'll need to remember where we came from to update the adjacency list.
        prev_node = player.current_room

        # Now after all that setup we finally travel somewhere.
        player.travel(direction)

        # We make a note of where we moved.
        traversal_path.append(direction)

        # We make a note that we've now visited that room.
        visited.add(player.current_room)

        new_exits = player.current_room.get_exits()

        # If the new room that we're in is not already in the graph, we add it.
        if player.current_room.id not in graph:
            #
            graph[player.current_room.id] = {}

            for item in new_exits:
                graph[player.current_room.id][item] = '?'

        # We can now update the graph's adjacency list.
        # We first reverse the direction we came from using the reverse table above.
        reversed_direction = reverse[direction]

        # Then we update the graph so our
        graph[prev_node.id][direction] = player.current_room.id
        graph[player.current_room.id][reversed_direction] = prev_node.id

        unexplored_rooms = [
            direction[0] for direction in graph[player.current_room.id].items() if direction[1] == '?']

        if len(unexplored_rooms) > 0:
            direction = unexplored_rooms[random.randint(
                0, len(unexplored_rooms) - 1)]
            stack.push(direction)

        elif len(visited) == len(world.rooms):
            return traversal_path

        else:
            backtrack_step = closest_unexplored_room(
                graph, player.current_room.id)

            for i in range(0, len(backtrack_step) - 1):
                player.travel(backtrack_step[i])
                traversal_path.append(backtrack_step[i])
                visited.add(player.current_room)
            stack.push(backtrack_step[-1])
        print(graph)


traverse(player)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
