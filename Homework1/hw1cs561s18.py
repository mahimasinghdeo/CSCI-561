
def minimax(costs,adj,path,depth):

    def lettertonumber(string):
        val = 0
        for char in reversed(string):
            val *= 26
            val += ord(char) - ord('A') + 1
        return val - 1

    def numbertoletter(num):
        val = ''
        num = num + 1
        while num > 0:
            val += chr(num % 26 + ord('A') - 1)
            num //= 26
        return val

    def adjacent(region):
        return set([x for x in range(len(adj)) if not visit[x] and adj[region][x] == 1])


    def recursive_func(adj_set, turn, path, utility,alpha_beta):
        if (len(path) > 1 and not (adj_set[0] or adj_set[1])) or len(path) == depth + 1:
            # print "Branch"
            # print branch_costs

            all_costs.append(utility[player])
            return utility

        if (len(path) > 1 and not (adj_set[turn])) or len(path) == depth + 1:
            recursive_func(adj_set, 1 - turn, path, utility,alpha_beta[:])
            return utility

        cost_new = level_cost[turn]

        if len(path) == 1:  # when you only have to look at what is not visited
            next_level = set()  # Nodes for next level
            for i in range(len(adj)):
                if not visit[i]:  # Just additional check
                    next_level.add(i)
        else:  # When its already been in for
            next_level = adj_set[turn]

        for i in next_level:
            path.append(i)
            visit[i] = True
            temp = adj_set[turn]
            adj_set[turn] = adj_set[turn].union(adjacent(i))
            if i in adj_set[turn]:  # if what we just used is still in list
                adj_set[turn].remove(i)
            flag = False
            if i in adj_set[1 - turn]:  # For the other player
                flag = True
                adj_set[1 - turn].remove(i)


            cost_new = min_or_max[turn](cost_new, recursive_func(adj_set, 1 - turn,path,
            [utility[0] + initial_cost[i] * (1 - turn),utility[1] + initial_cost[i] * (turn)],
            alpha_beta[:]),key = lambda x: x[player] - x[1-player])

            alpha_beta[turn] = min_or_max[turn](alpha_beta[turn],cost_new[player]-cost_new[1-player])


            if flag:  # return back to original adj set
                adj_set[1 - turn].add(i)
            adj_set[turn] = temp
            visit[i] = False
            path.pop()
            if alpha_beta[player] >= alpha_beta[1-player]:
                break

        return cost_new




    path = [lettertonumber(x) for x in path]
    cost_tuple = [(lettertonumber(x), y) for x, y in costs]
    initial_cost = [0]*len(adj)
    for i in cost_tuple:
        initial_cost[i[0]] = i[1] #can use append

    adj_set = [set(), set()]
    utility = [0, 0]
    turn = 0
    visit = [False]*len(adj)


    for i in path:
        visit[i] = True
        utility[turn] += initial_cost[i]
        adj_set[turn] = adj_set[turn].union(adjacent(i))
        if i in adj_set[turn]:
            adj_set[turn].remove(i)
        if i in adj_set[1 - turn]:
            adj_set[1 - turn].remove(i)
        turn = 1 - turn

    player = turn
    all_costs = []
    best_costs = (0, float('-inf'))
    alpha_beta = [0, 0]
    alpha_beta[player] = float('-inf')
    alpha_beta[1-player] = float('inf')
    level_cost = [[0,0],[0,0]]
    level_cost[player][player] = float('-inf')
    level_cost[1-player][player]= float('inf')
    min_or_max = [None,None]
    min_or_max[player] = max
    min_or_max[1-player] = min


    if not adj_set[turn]: #Executes when * case
        next_level = set()  # Nodes for next level
        for i in range(len(adj)):
            if not visit[i]: #Just additional check
                next_level.add(i)
    else:# When its already been in for
        next_level = adj_set[turn]

    for i in next_level:
        path.append(i)
        visit[i] = True
        temp = adj_set[turn]
        adj_set[turn] = adj_set[turn].union(adjacent(i))
        if i in adj_set[turn]: #if what we just used is still in list
            adj_set[turn].remove(i)
        flag = False
        if i in adj_set[1 - turn]: #For the other player
            flag = True
            adj_set[1-turn].remove(i)

        cost_new = recursive_func(adj_set,1-turn,path,[utility[0] + initial_cost[i] * (1 - turn),utility[1] + initial_cost[i] * (turn)],
        alpha_beta[:])
        alpha_beta[turn] = min_or_max[turn](alpha_beta[turn],cost_new[player]-cost_new[1-player])

        if cost_new[turn] > best_costs[1]:
            best_costs = (i, cost_new[turn])

       

        if flag:  # return back to original adj set
            adj_set[1 - turn].add(i)
        adj_set[turn] = temp
        visit[i] = False
        path.pop()





    return numbertoletter(best_costs[0]), all_costs



import sys
input_file = open(sys.argv[2], "r")

day = input_file.readline().rstrip()
print("Day is: ", day)

player = input_file.readline().rstrip()
print("Player is: ", player)

rpl = input_file.readline().rstrip("\n").split(',')
rpl = [x.replace("(","") for x in rpl]
rpl = [x.replace(")","") for x in rpl]
costs = []
for i in range(0, len(rpl), 2):
    x = (rpl[i], int(rpl[i+1]))
    costs.append(x)
# print costs



adj = []
for i in range(len(costs)):
    adj.append(eval(input_file.readline().rstrip().strip(",")))
# print("Adjacency Row: ", adj)


if day == "Yesterday":
    today_cost = [0] * len(adj)
    sigma = 0
    for i in range(len(adj)):
        sigma += costs[i][1]
    sigma = sigma*1.0/3

    for i in range(len(costs)):
        today_cost[i] = (sigma + costs[i][1])*1.0/2
    temp = []
    for i in range(len(today_cost)):
        temp.append((costs[i][0],today_cost[i]))
    # print "Temp"
    costs = temp
    # print costs


path = []
region_visited = input_file.readline().rstrip().strip(",")
if region_visited != '*':
    region_visited_concatenated = region_visited.replace(",", "")
    for i in region_visited_concatenated:
        path.append(i)
# print ("Region visited list: ", path)

depth = int(input_file.readline().rstrip())
# print ("Max depth: ", depth)

input_file.close()

print costs
print adj
print path
print depth
next_node, utility_list =  minimax(costs,adj,path,depth)



output_file = open("output.txt",'w')
output_file.write(next_node +"\n")
utility_list = [round(x) for x in utility_list]
utility_list = map(int,utility_list)
utility_list = ",".join(map(str,utility_list))
output_file.write(utility_list)
output_file.close()





















