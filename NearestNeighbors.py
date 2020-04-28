import copy

def InsertDict(d,key,value):
    if key in d:
        if value not in d[key]:
            d[key].append(value)
    else:
        d[key]=[value]

def Subtree(tree,subtree,new_root,forbidden_node):
    if len(tree[new_root])==1:
        InsertDict(subtree,new_root,-1)
        return subtree
    for node in tree[new_root]:
        if node!=forbidden_node:
            subtree.update(Subtree(tree,subtree,node,new_root))
            InsertDict(subtree,new_root,node)
    return subtree

def OriginalEdges(tree,edge):
    d={}
    for i in range(2):
        node=edge[i]
        for value in tree[node]:
            if value!=edge[1-i]:
                InsertDict(d,node,value)
    return d

def ChangeFormat(tree_copy,a,b):
    tree={}
    for node in tree_copy:
        if tree_copy[node][0]!=-1:
            for value in tree_copy[node]:
                InsertDict(tree,node,value)
                InsertDict(tree,value,node)
    tree[a].append(b)
    tree[b].append(a)
    return tree

def Reconstruct(subtrees,edge,original_edges):
    neighbors=[]
    tree={}
    a,b=edge
    for branch in subtrees:
        tree.update(branch)
    tree[a]=b
    tree[b]=a
    for i in range(2):
        temp=copy.deepcopy(original_edges)
        node21=temp[b][i]
        node12=temp[a][1]
        temp[a]=[temp[a][0],node21]
        temp[b]=[temp[b][1-i],node12]
        tree_copy=copy.deepcopy(tree)
        tree_copy.update(temp)
        neighbors.append(ChangeFormat(tree_copy,a,b))
    return neighbors

def NearestNeighborTrees(tree,edge):
    """This function takes in a unrooted tree & an edge, and returns all the nearest neighbor trees (unrooted)"""
    subtrees=[]
    for i in range(2):
        for node in tree[edge[i]]:
            if node!=edge[1-i]:
                subtrees.append(Subtree(tree,{},node,edge[i]))  
    original_edges=OriginalEdges(tree,edge)
    neighbors=Reconstruct(subtrees,edge,original_edges)
    return neighbors
