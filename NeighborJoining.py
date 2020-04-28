import numpy as np

def D2Dstar(matrix):
    n=len(matrix[0])
    matrix_star=np.zeros((n,n))
    total_distance=[]
    for i in range(n):
        total_distance.append(sum(matrix[i]))
    for i in range(n-1):
        for j in range(i+1,n):
            matrix_star[i][j]=matrix[i][j]*(n-2)-total_distance[i]-total_distance[j]
            matrix_star[j][i]=matrix_star[i][j]
    return matrix_star,total_distance

def FindMin(matrix):
    n=len(matrix[0])
    min_val=float("+inf")
    for i in range(n-1):
        for j in range(i+1,n):
            if matrix[i][j]<min_val:
                position=i,j
                min_val=matrix[i][j]
    return position

def ReviseMatrix(matrix,index2matrix,i,j):
    n=len(matrix[0])
    new_matrix=np.zeros((n-1,n-1))
    new_line=[]
    for col_num in range(n):
        if col_num!=i and col_num!=j:
            new_line.append((matrix[i][col_num]+matrix[j][col_num]-matrix[i][j])/2)
    new_line.append(0)
    matrix=np.delete(matrix,[i,j],0)
    matrix=np.delete(matrix,[i,j],1)
    new_matrix[:n-2,:n-2]=matrix
    for index in range(n-1):
        new_matrix[n-2][index]=new_line[index]
        new_matrix[index][n-2]=new_line[index]
    key_list=sorted(index2node.keys())
    for index in key_list:
        node=index2node[index]
        if index>i and index<j:
            index2node[index-1]=node
        if index==j:
            del index2node[index]
        if index>j:
            del index2node[index]
            index2node[index-2]=node
    return new_matrix,index2node
            

def NeighborJoining(matrix,tree,index2node):
    n=len(matrix[0])
    if n==2:
        node1=index2node[0]
        node2=index2node[1]
        tree[(node1,node2)]=matrix[0][1]
        tree[(node2,node1)]=matrix[0][1]
        return tree
    matrix_star,total_distance=D2Dstar(matrix)
    i,j=FindMin(matrix_star)
    node1=index2node[i]
    node2=index2node[j]
    delta=(total_distance[i]-total_distance[j])/(n-2)
    new_node=next(nodes)
    tree[(node1,new_node)]=(matrix[i][j]+delta)/2
    tree[(new_node,node1)]=tree[(node1,new_node)]
    tree[(node2,new_node)]=(matrix[i][j]-delta)/2
    tree[(new_node,node2)]=tree[(node2,new_node)]
    matrix,index2node=ReviseMatrix(matrix,index2node,i,j)
    index2node[n-2]=new_node
    tree.update(NeighborJoining(matrix,tree,index2node))
    return(tree)  

with open("dataset_10333_7.txt","r") as f:
    temp=f.read().split("\n")
n=int(temp[0])
matrix=np.zeros((n,n))
index2node={}
for i in range(1,n+1):
    alist=temp[i].split(" ")
    if "" in alist:
        alist.remove("") 
    matrix[i-1]=alist
    index2node[i-1]=i-1
nodes=iter(list(range(n,2*n)))
tree=NeighborJoining(matrix,{},index2node)
print(tree)

key_list=sorted(tree.keys(),key=lambda x: x[0])

with open("answer.txt","w") as f:
    for i,j in key_list:
        temp=round(tree[(i,j)],2)
        length=len(str(temp).split(".")[-1])
        if length==1:
            f.write("{}->{}:{}0\n".format(i,j,temp))
        else:
            f.write("{}->{}:{}\n".format(i,j,temp))

