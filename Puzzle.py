# Name: Kelsey Schmidt
# OSU Email: schmkels@oregonstate.edu
# Course: CS325 - Analysis Of Algorithms - Section 400
# Assignment 8: Graph Algorithms – II
# Date: 2-17-21
# Description: Implementation of an algorithm to solve a puzzle problem.

import heapq
from collections import deque

def solve_puzzle(Board, Source, Destination):
    """
    Puzzle description:
    You are given a puzzle consisting of a 2D matrix
    consisting of rows of valid movement squares "-" that you can traverse,
    and wall squares "#", that you cannot traverse.
    You can move either up, down, left, or right.
    Also given are a Source cell and Destination cell,
    given as coordinate pairs (a,b) and (x,y).

    The grid is 1-indexed, so the top left corner's coordinate would be (1,1),
    the first row's coordinates would be (1,1), (1,2), (1,3),
    second row would be (2,1), (2,2), (2,3), etc.

    The object is to move from the Source cell to the Destination cell
    in the fewest steps, not counting the Source or Destination in the final total.

    This function returns the amount of steps between Source and Destination,
    as well as the path taken as a series of directions (Up, Down, Left, Right),
    from the Source to the Destination (the path is for the extra credit portion).

    Example:
    An input of Board = [
    ["-","-","-","-","-"],
    ["-","-","#","-","-"],
    ["-","-","-","-","-"],
    ["#","-","#","#","-"],
    ["-","#","-","-","-"]
    ]

    Makes a grid like this:

    -	-	-	-	-
    -	-	#	-	-
    -	-	-	-	-
    #	-	#	#	-
    -	#	-	-	-

    With a Source of (1,1) and a Destination of (5,5),
    the output would be: 7, RRRRDDDD

    Invalid Destinations will return None.
    """
    # if we're not moving we can just return and save some work
    if (Source == Destination):
        return "0, Source is the Destination"

    # using our given puzzle matrix input, we can make a graph input instead,
    # like we used in the exploration for Dijkstra's algorithm from Week 7.
    # we need to find the valid cells orthogonally adjacent to each cell in the puzzle input,
    # and can give a weight of 1 to each neighboring cell edge to represent a distance of 1 cell.
    graph = dict()
    length_puzzle = len(Board)
    length_puzzle_0 = len(Board[0])
    for i in range (1, length_puzzle+1):
        for j in range(1, length_puzzle_0+1):
            if Board[i - 1][j - 1] == "#":
                continue    # skip wall cells
            graph[(i,j)] = dict()
            for k in range(max(i-1, 1), min(i+2,length_puzzle+1)):
                # skip inputs outside of the puzzle range
                for l in range(max(j-1, 1), min(j+2,length_puzzle_0+1)):
                    # skip inputs outside of the puzzle range
                    if (abs(i-k) == abs(j-l)) or (Board[k - 1][l - 1] == "#"):
                        continue    # skip the cell itself, wall cells, or cells diagonal from the current cell
                    # assign an edge weight of 1
                    graph[(i,j)][(k,l)] = 1

    # now we can use the code for Dijkstra's algorithm as given in the exploration,
    # with the graph and Source input
    distances = {vertex: float("infinity") for vertex in graph}
    distances[Source] = 0
    # track parent nodes to generate the path if we reach the Destination
    parents = {vertex: None for vertex in graph}

    # manually set distance for source as -1: the directions say to not count the starting cell or the destination cell
    # Since we immediately mark this as complete, it won't affect Dijkstra's algorithm for the distance calculations
    pq = [(-1, Source)]
    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)

        # Nodes can get added to the priority queue multiple times.
        # We only process a vertex the first time we remove it from the priority queue.
        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            # Only consider this new path if it's better than any path we've already found.
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # set the parent cell, so we can traverse the path later
                parents[neighbor] = current_vertex

            # we can stop once we get to the destination
            if neighbor == Destination:
                break

            heapq.heappush(pq, (distance, neighbor))

        # break out of while loop as well if we broke for neighbor == Destination
        if neighbor == Destination:
            break

    # if there is not a possible path from source to destination
    if distances[Destination] == float("inf"):
        return "None, No path from Source to Destination"

    # track the path backwards through the parents, appending directions into a list
    # using a deque for O(1) insertion at the front, so it won't add any significant runtime,
    # nor increase our overall time complexity.
    path = deque([])
    item = Destination
    while parents[item] is not None:
        if item[0] == parents[item][0] - 1:
            direction = "U"
        elif item[0] == parents[item][0] + 1:
            direction = "D"
        elif item[1] == parents[item][1] - 1:
            direction = "L"
        elif item[1] == parents[item][1] + 1:
            direction = "R"
        path.appendleft(direction)
        item = parents[item]

    # this returns distance traveled minus the start and end points, and the path for extra credit
    output = str(str(distances[Destination]) + ", "+("".join(path)))
    return output


Board = [
    ["-","-","-","-","-"],
    ["-","-","#","-","-"],
    ["-","-","-","-","-"],
    ["#","-","#","#","-"],
    ["-","#","-","-","-"]
    ]
Source = (1,3)
Destination = (3,3)
print(solve_puzzle(Board, Source, Destination))
Source = (1,1)
Destination = (5,5)
print(solve_puzzle(Board, Source, Destination))
