#!/usr/bin/env python
# coding: utf-8

# In[36]:


def mataddition(A,B):
    if(len(A)!=len(B) or len(A[0])!=len(B[0])):
        return "Addition not possible"
    for i in range(len(A)):
        for j in range(len(A[0])):
            A[i][j]=A[i][j]+B[i][j]
    return A

def matsubtraction(A,B):
    if(len(A)!=len(B) or len(A[0])!=len(B[0])):
        return "Subtraction not possible"
    for i in range(len(A)):
        for j in range(len(A[0])):
            A[i][j]=A[i][j]-B[i][j]
    return A

def matmultiplication(A,B):
    if(len(A[0])!=len(B)):
        return "Multiplication not possible"
    result = [[sum(a * b for a, b in zip(A_row, B_col))
                        for B_col in zip(*B)]
                                for A_row in A]
    return result

def zeros_matrix(rows, cols):
    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0.0)

    return M
def copy_matrix(M):
    rows = len(M)
    cols = len(M[0])
    MC = zeros_matrix(rows, cols)
    for i in range(rows):
        for j in range(cols):
            MC[i][j] = M[i][j]

    return MC

def matdeterminant(A, det=0):
    indices = list(range(len(A)))
    if len(A) == 2 and len(A[0]) == 2:
        val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return val
    for fc in indices:
        As = copy_matrix(A)
        As = As[1:]
        height = len(As) 
 
        for i in range(height): 
            As[i] = As[i][0:fc] + As[i][fc+1:] 
 
        sign = (-1) ** (fc % 2) # F) 
        sub_det = matdeterminant(As)
        det += sign * A[0][fc] * sub_det 
 
    return det


# In[ ]:





# In[ ]:




