import datetime



def matrix_add(A,B):
    for i in range(len(A)):
        for j in range(len(A)):
            A[i][j]+=B[i][j]
    return A

def matrix_del(A,B):
    for i in range(len(A)):
        for j in range(len(A)):
            A[i][j]-=B[i][j]
    return A
