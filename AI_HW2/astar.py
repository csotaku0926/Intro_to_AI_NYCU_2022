import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'

# this part is also my code (part 4)!
# structure for nodes
class node:
    def __init__(self,id,p,c,g):
        self.id = id
        self.parent = p # parent
        self.cost = c
        self.g = g # distance to start
    def __lt__(self,other): # compare function
        return self.cost < other.cost

def astar(start, end):
    # Begin your code (Part 4)
    """
    explanation :
    define the structure of node, containing its id, parent (for path backtracking), total cost (cost) and movement cost (g)
    and a comparison function that compares the cost.
    construct the graph of the map from csv file by using a dictionary that use start id as key, end ids and distances as values
    also build a dictionary with id as key and heuristic cost for each end as values, from the given csv file.
    initialize an open list and closed list (visited list), push start node into open list
    while the open list is not empty, sort the list by the value of total cost,
    then pop out the node with the minimized cost as front node.
    for its adjacency, if it is a key of graph and not in closed set, 
    calculate the total cost of this adjacency, known as f(x) = g(x) + h(x).
    If the adjacency is not in open list yet, and if this is the goal node, reconstruct the path by each parent,
    return the path,distance and num_visited ;
    else push the adjacency into open list with its calculated cost;
    if it is already in the open list, and if it has the less cost, update its cost value 
    finally, push the front node into closed list and end the for loop
    """
    rows = csv.reader(open(edgeFile,newline=''))
    # build a graph
    graph = dict()
    for row in rows:
        # store number
        if row[0].isnumeric():
            k = int(row[0])
            # key not in dict
            if k not in graph:
                graph[k] = list()
            graph[k].append(row)
    # set up heuristic cost
    hrows = csv.reader(open('heuristic.csv',newline=''))
    hcost = dict()
    for row in hrows:
        if row[0].isnumeric():
            hcost[int(row[0])] = [float(row[1]),float(row[2]),float(row[3])]

    # start A* algorithm : f(x) = g(x) + h(x)
    open_list = []
    close_list = [] # visited class member
    num_visited = 0
    open_list.append(node(start,None,0,0)) # push start
    while len(open_list) > 0:
        open_list = sorted(open_list)
        s = open_list.pop(0) # pop nodes with min cost
        # for each successor that is a key of graph
        try:
            for row in graph[s.id]:
                adj = int(row[1])
                # prevent revisited
                visited = False
                for c in close_list:
                    if c.id == adj:
                        visited = True
                        break
                # not visited
                if not visited:
                    # compute f(x) for this successor
                    g2 = s.g + float(row[2])
                    if end == 1079387396:
                        h2 = hcost[adj][0] # for ID1 only!
                    elif end == 1737223506:
                        h2 = hcost[adj][1]
                    else:
                        h2 = hcost[adj][2]
                    f2 = g2 + h2
                    # check if adj in open list
                    inOpen = False
                    i = 0
                    for o in open_list:
                        if o.id == adj:
                            inOpen = True
                            break
                        i += 1
                    # not in open list
                    if not inOpen:
                        num_visited += 1
                        # reach destination
                        if adj == end:
                            # construct path
                            p2 = [end]
                            p = s
                            while p is not None:
                                p2.insert(0,p.id)
                                p = p.parent    
                            return p2, g2, num_visited # new path, new dist, num visited
                        # insert to open list 
                        open_list.append(node(adj,s,f2,g2))
                    else:
                        # check if this path is better
                        if open_list[i].g > g2:
                            open_list[i] = node(adj,s,f2,g2)
        except KeyError:
            continue
        # push s to close list
        close_list.append(s)
    # not found
    return [],-1,-1
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
