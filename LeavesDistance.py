import numpy as np

def FindLeaves(tree):
    leaves=[]
    for node in tree:
        if len(tree[node])==1:
            leaves.append(node)
    return leaves

def AllPaths(unweighted_tree,leaves):
    leafnum=len(leaves)
    elongating_paths=[]
    for leaf in leaves:
        elongating_paths.append([leaf])
    l2l_paths=[]
    while elongating_paths:
        for path in list(elongating_paths):
            for nextnode in unweighted_tree[path[-1]]:
                if len(path)>=2:
                    if nextnode!=path[-2]:
                        elongating_paths.append(path+[nextnode])
                else:
                    elongating_paths.append(path+[nextnode])            
            elongating_paths.remove(path)
        i=0
        times=0
        maxtimes=len(elongating_paths)
        while times<maxtimes:
            path=elongating_paths[i]
            if path[-1] in leaves:
                l2l_paths.append(path)
                elongating_paths.remove(path)
            else:
                i+=1
            times+=1
    return l2l_paths

def Distance(unweighted_tree,weighted_tree):
    distance_d={}
    leaves=FindLeaves(unweighted_tree)
    paths=AllPaths(unweighted_tree,leaves)
    for path in paths:
        if (path[0],path[-1]) not in distance_d:
            distance=0
            for i in range(len(path)-1):
                distance+=weighted_tree[(path[i],path[i+1])]
            distance_d[(path[0],path[-1])]=distance
            distance_d[(path[-1],path[0])]=distance
    return distance_d
    

unweighted_tree={}
weighted_tree={}
with open("dataset_10328_12.txt","r") as f:
    n=int(f.readline())
    for line in f:
        temp=line.split(":")
        mykey=temp[0].split("->")
        edge=(int(mykey[0]),int(mykey[1]))
        weighted_tree[edge]=int(temp[1])
        if edge[0] not in unweighted_tree:
            unweighted_tree[edge[0]]=[edge[1]]
        elif edge[1] not in unweighted_tree[edge[0]]:
            unweighted_tree[edge[0]].append(edge[1])
        else:
            pass
        if edge[1] not in unweighted_tree:
            unweighted_tree[edge[1]]=[edge[0]]
        elif edge[0] not in unweighted_tree[edge[1]]:
            unweighted_tree[edge[1]].append(edge[0])

d=Distance(unweighted_tree,weighted_tree)
leaves=FindLeaves(unweighted_tree)
leaf_num=len(leaves)
for item in leaves:
    d[item,item]=0
matrix=np.zeros((leaf_num,leaf_num))
for i,j in d:
    matrix[i][j]=int(d[(i,j)])


with open('answer.txt','w') as f:
    for i in range(leaf_num):
        for item in matrix[i]:
            f.write(str(int(item))+' ')
        f.write("\n")










