import numpy as np
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
B = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
C = A + B
T = A.T
D = np.linalg.det(A)


# Output for A
print('A =')
for row in A: print(row)

# Output for B
print('B =')
for row in B: print(row)

# Output for C
print('C =')
for row in C: print(row)

# Output for T
print('T =')
for row in T: print(row)

# Output for D
print('D =', D)