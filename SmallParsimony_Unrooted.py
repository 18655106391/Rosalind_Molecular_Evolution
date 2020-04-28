import copy

def InsertDict(d,key,value):
    if key in d:
        if value not in d[key]:
            d[key].append(value)
    else:
        d[key]=[value]

def ScoreLeaf(c):
    if c=="A":
        return (0,float("+inf"),float("+inf"),float("+inf"))
    if c=="C":
        return (float("+inf"),0,float("+inf"),float("+inf"))
    if c=="G":
        return (float("+inf"),float("+inf"),0,float("+inf"))
    if c=="T":
        return (float("+inf"),float("+inf"),float("+inf"),0)

def Score(c1,c2):
    if c1==c2:
        return 0
    return 1

def CheckRipe(tree,tag):
    for parent_node in tree:
        if tag[parent_node]==0:
            flag=True
            for child in tree[parent_node]:
                if tag[child]==0:
                    flag=False
            if flag==True:
                return parent_node
    return

alphabet=["A","C","G","T"]

def SmallParsimony(tree,node2base):
    """This function takes in a rooted tree and a list, list[node]==the letter corresponding to the node"""
    tag=[]  #tag[node]=0 or 1
    node_info={}  #node_info[node]=[(scoreA,scoreC,scoreG,scoreT),(sourceA,sourceC,sourceG,sourceT)].source in form of (base1,base2)
    leaf_num=len(node2base)
    for i in range(leaf_num):
        tag.append(1)
        node_info[i]=[ScoreLeaf(node2base[i]),(-1,-1,-1,-1)]
    for i in range(leaf_num,2*leaf_num-1):
        tag.append(0)
    v=CheckRipe(tree,tag)
    while v:
        tag[v]=1
        child1,child2=tree[v]
        scores=[]
        sources=[]
        for k in range(4):
            possibilities=[]
            for i in range(4):
                for j in range(4):
                    possibility=node_info[child1][0][i]+Score(alphabet[i],alphabet[k])+node_info[child2][0][j]+Score(alphabet[j],alphabet[k])
                    possibilities.append((possibility,i,j))
            min_val=float("+inf")
            for possibility,i,j in possibilities:
                if possibility<min_val:
                    min_val=possibility
                    position=i,j
            scores.append(min_val)
            sources.append((alphabet[position[0]],alphabet[position[1]]))
        node_info[v]=[tuple(scores),tuple(sources)]
        v=CheckRipe(tree,tag)
    return node_info

def TraceBack(tree,root_node,root_base,node_base_dict,node_info):
    if node_info[root_node][1][0]==-1:
        node_base_dict[root_node]=root_base
        return node_base_dict
    index=alphabet.index(root_base)
    child1_base,child2_base=node_info[root_node][1][index]
    child1_node,child2_node=tree[root_node]
    node_base_dict[root_node]=root_base
    node_base_dict.update(TraceBack(tree,child1_node,child1_base,node_base_dict,node_info))   
    node_base_dict.update(TraceBack(tree,child2_node,child2_base,node_base_dict,node_info))    
    return node_base_dict

def Disassemble(node2string,i):
    node2base=[]
    for string in node2string:
        node2base.append(string[i])
    return node2base
    
def IsInt(s):
    try:
        int(s)
    except ValueError:
        return 0
    return 1

def FindRoot(tree):
    max_val=0
    for key in tree:
        if key>max_val:
            max_val=key
    return max_val

def Assemble(tree_info_list):
    d={}
    for tree_info in tree_info_list:
        for node in tree_info:
            if node not in d:
                d[node]=tree_info[node]
            else:
                d[node]=d[node]+tree_info[node]
    return d

def Complete(tree):
    complete_tree={}
    for key in tree:
        for value in tree[key]:
            InsertDict(complete_tree,value,key)
            InsertDict(complete_tree,key,value)
    return complete_tree
        
def Distance(s1,s2):
    distance=0
    for i in range(len(s1)):
        if s1[i]!=s2[i]:
            distance+=1
    return distance

def AddRoot(unrooted_tree):
    """Input: unrooted_tree. Output: a dictionary of rooted binary tree, tree[node]=[left_child,right_child]"""
    tree=copy.deepcopy(unrooted_tree)
    max_node=max(list(unrooted_tree.keys()))
    other_node=max(unrooted_tree[max_node])
    root=max_node+1
    tree[root]=[other_node,max_node]
    tree[max_node].append(root)
    tree[max_node].remove(other_node)
    tree[other_node].append(root)
    tree[other_node].remove(max_node)
    return tree,root

def Binarize(rooted_tree,current_root,last_root,binary_tree):
    if len(rooted_tree[current_root])==1:
        return {}
    for node in rooted_tree[current_root]:
        if node!=last_root:
            InsertDict(binary_tree,current_root,node)
    last_root=current_root
    for current_root in binary_tree[last_root]:
        binary_tree.update(Binarize(rooted_tree,current_root,last_root,binary_tree))
    return binary_tree

def SmallParsimony_Unrooted(unrooted_tree,n,node2string):
    """Input an unrooted_tree and leaf number n, output the final_score and the string of each node."""
    rooted_tree,root=AddRoot(unrooted_tree)
    tree=Binarize(rooted_tree,root,-1,{})
    tree_info_list=[]
    final_score=0
    for i in range(len(node2string[0])):
        node2base=Disassemble(node2string,i)
        node_info=SmallParsimony(tree,node2base)
        root=FindRoot(tree)
        score_single_base=min(node_info[root][0])
        final_score+=score_single_base
        tree_info=TraceBack(tree,root,alphabet[node_info[root][0].index(score_single_base)],{},node_info)
        tree_info_list.append(tree_info)
    d=Assemble(tree_info_list)
    return final_score,d


