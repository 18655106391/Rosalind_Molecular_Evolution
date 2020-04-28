import numpy as np

def ReviseMatrix(matrix,i,j,cluster_list):
    #print("In function ReviseMatrix:")
    print(matrix)
    #print("i:{},j:{},clusterlist:".format(i,j),cluster_list)
    newcol=[]
    size1=len(cluster_list[i])
    size2=len(cluster_list[j])
    n=len(matrix[0])
    newmatrix=np.zeros((n-1,n-1))
    for row_num in range(n): 
        if row_num!=i and row_num!=j:
            newcol.append((matrix[row_num][i]*size1+matrix[row_num][j]*size2)/(size1+size2))
    newcol.append(0)
    matrix=np.delete(matrix,[i,j],1)
    matrix=np.delete(matrix,[i,j],0)
    newmatrix[0:n-2,0:n-2]=matrix
    for index in range(n-1):
        newmatrix[index][n-2]=newcol[index]
        newmatrix[n-2][index]=newcol[index]
    print(newmatrix)
    return newmatrix


def FindClosest(matrix):
    n=len(matrix[0])
    min_val=float("+inf")
    for i in range(n-1):
        for j in range(i+1,n):
            item=matrix[i][j]
            if item<min_val:
                min_val=item
                position=i,j
    return position,min_val

def UPGMA_Unweighted(matrix):
    n=len(matrix[0])
    cluster_d={}
    cluster_list=[]
    unweighted_tree={}
    age={}
    for i in range(n):
        cluster_d[tuple([i])]=i #cluster_d[(cluster)]=node
        cluster_list.append([i]) #cluster position in matrix=clusterlist.index(cluster)
        unweighted_tree[i]=[]
        age[i]=0
    while len(cluster_list)>1:
        min_val=float("+inf")
        position,min_val=FindClosest(matrix)
        i,j=position
        node1=cluster_d[tuple(cluster_list[i])]
        node2=cluster_d[tuple(cluster_list[j])]
        #print(matrix)
        #print("i:{},j:{},node1:{},node2:{},min_val:{}".format(i,j,node1,node2,min_val))
        newnode=next(nodes)
        age[newnode]=min_val/2
        unweighted_tree[node1].append(newnode)
        unweighted_tree[node2].append(newnode)
        unweighted_tree[newnode]=[node1,node2]
        new_cluster=cluster_list[i]+cluster_list[j]
        matrix=ReviseMatrix(matrix,i,j,cluster_list)
        cluster_list.append(new_cluster)
        cluster_list.remove(cluster_list[j])
        cluster_list.remove(cluster_list[i])
        cluster_d[tuple(new_cluster)]=newnode
        #print(cluster_list)
        #print(unweighted_tree)        
    return unweighted_tree,age

def UPGMA_Weighted(unweighted_tree,age):
    tree={}
    for node in unweighted_tree:
        for nextnode in unweighted_tree[node]:
            if (node,nextnode) not in tree:
                tree[(node,nextnode)]=abs(age[node]-age[nextnode])
                tree[(nextnode,node)]=tree[(node,nextnode)]
    return tree
with open("dataset_10332_8.txt","r") as f:
    temp=f.read().split("\n")
n=int(temp[0])
matrix=np.zeros((n,n))
for i in range(n):
    matrix[i]=list(map(int,temp[i+1].split(" ")))
nodes=iter(list(range(n,n*n-2*n)))
unweighted_tree,age=UPGMA_Unweighted(matrix)
tree=UPGMA_Weighted(unweighted_tree,age)
print(tree)
key_list=sorted(tree.keys(),key=lambda x: x[0])

with open("answer.txt","w") as f:
    for i,j in key_list:
        f.write("{}->{}:{}\n".format(i,j,round(tree[(i,j)],2)))


