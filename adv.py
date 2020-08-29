from room import Room
from player import Player
from world import World

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


"""
    PROBLEM: 
        1) I need to traverse this maze. 
        2) I need to do it in less than 960 steps  
        3) I need to use graphs to do it. 
            4) We've completed the maze when our adjacency list has no question marks left AND... 
            5) The number of rooms that we've explored is equal to 500.
    
    SOLUTION: I'm not sure about a solution yet. I'm still discovering. Here are the things I believe I know about the problem.
    
        1) I know I need to populate a list of directions that are available to me at each room in the maze.
            1a) First, I grab the room's id and use that to populate the world.rooms[current_room_id] table.
            
        2) When there's a dead end, I need to find a previous cell which has not been explored.
        3) I'll need to keep track of the directions back to a node where there are unexplored nodes.
            3a) I think I can do this by writing a list that will contain instructions for how to get back to where I started.
        
        4) When I move into a new room, there are a few items I can populate on my graph. 
            4a) I've already filled in in the rooms which are connected to the room I'm in (player.current_room.get_exits())'
            4b) I can also fill in my adjacency list by filling in the values of those pairs.
            4c) The more rooms I visit, the more I'm going to get filled out in my graph.
            4d) The problem arises when I have to backtrack. I'll need to keep a stack of references to the last node with an unexplored path. Ideally, I'll also be keeping the shortest path back to that node too.
            4e) Once I get back to that node, I can pick one of the unexplored directions and go explore it.

"""

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

traversal_path = []


def map_maze(player):

    # Standard graph traversal. Set up something to track visited nodes.
    visited = set()

    # Creating a list for keeping track of where I am and how to get back to where I need to be.
    backtrack = []

    # This is a dictionary for easily mapping my backtrack path.
    reverse = {
        "n": "s",
        "s": "n",
        "e": "w",
        "w": "e"
    }

    # I need a loop to run to explore every node. While the number of rooms in visited is less than 500, do stuff.

    while len(visited) < len(world.rooms):

        # We need to know what room we're currently in.
        current_room = player.current_room

        # We need to know the exits in this current room.
        exits = current_room.get_exits()

        # We want to know the rooms that still remain unexplored.
        unexplored_rooms = [direction for direction in exits if current_room.get_room_in_direction(
            direction) not in visited]

        visited.add(current_room)

        if unexplored_rooms:

            # Picking a direction to go from our list of unexplored rooms.
            random_direction = unexplored_rooms[random.randint(
                0, len(unexplored_rooms) - 1)]

            player.travel(random_direction)
            backtrack.append(random_direction)
            traversal_path.append(random_direction)

        else:

            # If I get stuck, I need to backtrack. I'll start pulling the items from my backtrack list.
            reverse_input = backtrack.pop(-1)

            # We plug reversed_direction into our reverse dict to get the direction we need to go in.
            reverse_output = reverse[reverse_input]
            player.travel(reverse_output)
            traversal_path.append(reverse_output)
    print(visited)

    return traversal_path


map_maze(player)

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
