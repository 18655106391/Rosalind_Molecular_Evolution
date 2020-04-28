import SmallParsimony_Unrooted as SPU
import NearestNeighbors as NN

def HammingDistance(s1,s2):
    score=0
    for i in range(len(s1)):
        if s1[i]!=s2[i]:
            score+=1
    return score

def ChangeFormat(d,n):
    """This Function takes in a dictionary, returns node2string list """
    node2string=[0]*n
    for node in d:
        if node<n:
            node2string[node]=d[node]
    return node2string

def InternalEdges(tree):
    internal_edges=[]
    tree_structure,n,dump=tree
    for start_node in tree_structure:
        if start_node>=n:
            for end_node in tree_structure[start_node]:
                if end_node>=n:
                    temp=(min(start_node,end_node),max(start_node,end_node))
                    if temp not in internal_edges:
                        internal_edges.append(temp)
    return internal_edges
        
    

def Nearest_Neighbor_Interchange(original_tree,n,node2string):
    """Takes in an unrooted tree, the leaf number, and the node2string list"""
    score=float("+inf")
    new_score,tree_info_list=SPU.SmallParsimony_Unrooted(original_tree,n,node2string)
    new_tree=(original_tree,n,ChangeFormat(tree_info_list,n))
    while new_score<score:
        score=new_score
        tree=new_tree
        for edge in InternalEdges(tree):
            for neighbor_tree in NN.NearestNeighborTrees(tree[0],edge):
                neighbor_score,neighbor_info_list=SPU.SmallParsimony_Unrooted(neighbor_tree,n,node2string)
                if neighbor_score<new_score:
                    new_score=neighbor_score
                    new_tree=(neighbor_tree,n,ChangeFormat(neighbor_info_list,n))
        print("score:{},new_score:{}".format(score,new_score))
        WriteProcess(score,neighbor_tree,neighbor_info_list)
    return new_tree

def WriteProcess(score,tree,d):
    with open("answer.txt","a+") as f:
        f.write(str(score)+"\n")
        for key in tree:
            for value in tree[key]:
                f.write(d[key]+"->"+d[value]+":{}\n".format(HammingDistance(d[key],d[value])))
        f.write("\n")
    return

with open("dataset_10336_8.txt","r") as f:
    lines=f.read().split("\n")
if "" in lines:
    lines.remove("")
n=int(lines[0])
nodes=iter(list(range(n)))
unrooted_tree={}
node2string=[]
for line in lines[1:]:
    temp=line.split("->")
    if SPU.IsInt(temp[1]) and SPU.IsInt(temp[0]):
        SPU.InsertDict(unrooted_tree,int(temp[0]),int(temp[1]))
    elif SPU.IsInt(temp[0]):
        if temp[1] not in node2string:
            node2string.append(temp[1])
            index=next(nodes)
        else:
            index=node2string.index(temp[1])
        SPU.InsertDict(unrooted_tree,int(temp[0]),index)
    else:
        if temp[0] not in node2string:
            node2string.append(temp[0])
            index=next(nodes)
        else:
            index=node2string.index(temp[0])
        SPU.InsertDict(unrooted_tree,index,int(temp[1]))
min_tree=Nearest_Neighbor_Interchange(unrooted_tree,n,node2string)

