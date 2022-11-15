import numpy as np

a = np.array([1,2,3], dtype = "int16")
# print(a)
# print(np.square(a))

b = np.array([[9.0, 8.0, 7.0], [6.0, 5.0, 4.0]])
# print(b)
# print(np.square(b))

#Get dimension
# print(a.ndim, b.ndim)

# #Get shape
# print(a.shape, len(b[0]))

# #Get type
# print(a.dtype, b.dtype)

# #Get size
# print(a.itemsize)

# #Get total size
# print(a.nbytes, b.nbytes)

a = np.array([[1,2,3,4,15,6,7],[8,9,10,11,12,13,14]])
# print(a.shape)

#Get a specific element [r, c]
# print(a[1,-2]) #13

# #Get a specific row
# print(a[1, :])

# #Get a specific column
# print(a[: , 3])

# #Getting a little fancy [startInd : endInd : steps]
# print(a[:, 1:6:2])

b = np.array([[[1,2],[3,4]], [[5,6],[7,8]]])
# #Get a specific element (work outside in)
# print(b[1,0,0]) #5

# #Replace (update) has to be the same matrix size

# #ALl - zeros matrix
# c = np.zeros((3,2,3,2))
# print(c)
#All ones matrix
c = np.ones((3,4))
print(c)

# #All sth matrix
# c = np.full((2,4), 10, dtype="float16")
# print(c)
# c = np.full_like(a, 3)
# print(c)

#Random decimal numbers
d = np.random.rand(4,2)
# print(d)

# print(np.matmul(c,d))
# data = np.genfromtxt("results-penguins-1-2191.csv", delimiter = ",")
# print(data)

# print(a)

# carr = np.array(a/np.max(a, axis=(0,1)) * 15)
# print(carr)



# a = 'asodfjaoisd.lkj'

# b = a.split('.')[0]
# print(a,b)