import numpy as np
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
B = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
C_add = np.add(A, B)
T = A.T
D_det = np.linalg.det(A)
C_sub = np.subtract(A, B)
C_div = np.divide(A, B)


# Output for A
print('A =')
for row in A: print(row)

# Output for B
print('B =')
for row in B: print(row)

# Output for C_add
print('C_add =')
for row in C_add: print(row)

# Output for T
print('T =')
for row in T: print(row)

# Output for D_det
print('D_det =', D_det)

# Output for C_sub
print('C_sub =')
for row in C_sub: print(row)

# Output for C_div
print('C_div =')
for row in C_div: print(row)