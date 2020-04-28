import numpy as np


with open("data.txt","r") as f:
    temp=f.read().split("\n")
num=int(temp[0])
matrix=np.zeros((num,num))
i=0
for line in temp[1:]:
    if len(line)>0:
        matrix[i]=list(map(float,line.split(" ")))
    i+=1
print(matrix)
