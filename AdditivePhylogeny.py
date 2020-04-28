import numpy as np

def LimbLength(matrix,j):
    n=len(matrix[0])
    min_value=float("+inf")
    for i in range(0,n):
        for k in range(i+1,n):
            temp=(matrix[i][j]+matrix[j][k]-matrix[i][k])/2
            if temp>0 and temp<min_value:
                min_value=temp
    return min_value

def AttachmentPoint(matrix):
    n=len(matrix[0])
    for i in range(n):
        for k in range(i+1,n):
            if matrix[i][k]==matrix[i][n-1]+matrix[k][n-1]:
                return i,k,matrix[i][n-1]

def Weighted2Unweighted(weighted_tree):
    unweighted_tree={}
    for node1,node2 in weighted_tree:
        if node1 not in unweighted_tree:
            unweighted_tree[node1]=[node2]
        else:
            if node2 not in unweighted_tree[node1]:
                unweighted_tree[node1].append(node2)
        if node2 not in unweighted_tree:
            unweighted_tree[node2]=[node1]
        else:
            if node1 not in unweighted_tree[node2]:
                unweighted_tree[node2].append(node1)
    return unweighted_tree
    

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

def FindPath(weighted_tree,i,k):
    tree=Weighted2Unweighted(weighted_tree)
    leaves=FindLeaves(tree)
    #print("Try to find path from {} to {} in".format(i,k),tree,"with leaves",leaves)
    paths=AllPaths(tree,leaves)
    #print("All paths are",paths)
    for path in paths:
        if path[0]==i and path[-1]==k:
            return path
    

def AdditivePhylogeny(matrix,d):
    n=len(matrix[0])
    if n==2:
        d[(0,1)]=matrix[0][1]
        d[(1,0)]=matrix[0][1]
        return d
    limb_length=LimbLength(matrix,n-1)
    for j in range(0,n-1):
        matrix[n-1][j]-=limb_length
        matrix[j][n-1]-=limb_length
    i,k,attachment_distance=AttachmentPoint(matrix)
    matrix=np.delete(matrix,n-1,0)
    matrix=np.delete(matrix,n-1,1)
    d=AdditivePhylogeny(matrix,d)
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!START\nn:{}".format(n))
    #print("limb_length:{}".format(limb_length))
    #print("i,k,Attachment Distance:")
    #print(i,k,attachment_distance)
    #print(d)
    if (i,k) in d:
        newnode=next(nodes)
        d[(i,newnode)]=attachment_distance
        d[(newnode,i)]=attachment_distance
        d[(newnode,n-1)]=limb_length
        d[(n-1,newnode)]=limb_length
        d[(k,newnode)]=d[(i,k)]-attachment_distance
        d[(newnode,k)]=d[(k,newnode)]
        del d[(i,k)]
        del d[(k,i)]
    else:
        path=FindPath(d,i,k)
        #print("Attachment point on the path",path)
        length=0
        counter=0
        while length<attachment_distance:
            length+=d[(path[counter],path[counter+1])]
            counter+=1
        i,k=path[counter-1],path[counter]
        newnode=next(nodes)
        d[(i,newnode)]=attachment_distance-length+d[i,k]
        d[(newnode,i)]=d[(i,newnode)]
        d[(k,newnode)]=d[(i,k)]-d[(i,newnode)]
        d[(newnode,k)]=d[(k,newnode)]
        d[(newnode,n-1)]=limb_length
        d[(n-1,newnode)]=limb_length
        del d[(i,k)]
        del d[(k,i)]
    return d

with open("coronavirus_distance_matrix_additive.txt","r") as f:
    temp=f.read().split("\n")
n=int(temp[0])
matrix=np.zeros((n,n))
if "" in temp:
    temp.remove("")
for i in range(1,len(temp)):
    matrix[i-1]=list(map(int,temp[i].split(" ")))
nodes=iter(list(range(n,n*n-2*n)))
tree=AdditivePhylogeny(matrix,{})
key_list=list(tree)
key_list.sort(key=lambda x: x[0])

with open("answer.txt","w") as f:
    for node1,node2 in key_list:
        f.write("{}->{}:{}\n".format(node1,node2,int(tree[(node1,node2)])))

