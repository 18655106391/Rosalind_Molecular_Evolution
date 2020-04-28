import numpy as np

def LimbLength(matrix,j):
    n=len(matrix[0])
    min_value=float("+inf")
    for k in range(1,n):
        temp=(matrix[0][j]+matrix[j][k]-matrix[0][k])/2
        if temp>0 and temp<min_value:
            min_value=temp
    return min_value
        



with open("dataset_10329_11.txt",'r') as f:
    content=f.read().split("\n")
leaf_num=int(content[0])
distance_matrix=np.zeros((leaf_num,leaf_num))
for i in range(leaf_num):
    temp=content[i+2].split(" ")
    for j in range(leaf_num):
        distance_matrix[i][j]=int(temp[j])
j=int(content[1])
print(distance_matrix)
print(LimbLength(distance_matrix,j))

