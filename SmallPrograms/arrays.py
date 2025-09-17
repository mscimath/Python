import numpy as np
import array as arr

np_array = np.array([1, 2, 3, 4, 5])
print(np_array)
print(np_array[2])

numbers = arr.array('i', [1, 2, 3, 4, 5])
print(numbers)  # Output: array('i', [1, 2, 3, 4, 5])
print(numbers[1]) # Output: 2
print(numbers[-2])
numbers.append(6)
print(numbers[-1])
np_array_longer = np.append(np_array, 6)
print(np_array_longer[-1])
numbers.remove(numbers[4])
print(numbers)

length = 0
if len(np_array) > len(numbers):
    length = len(numbers)
else:
    length = len(np_array)
# Adding two arrays element-wise
result_for = [np_array[i] + numbers[i] for i in range(length)]
print(result_for)

result_direct = np_array + numbers
print(list(result_direct))

# Speed comparison
import time
# Creating large listings
list1 = list(range(1000000))
list2 = list(range(1000000))
# Timing the addition
start_time = time.time()
result = [list1[i] + list2[i] for i in range(len(list1))]
print(f"Python list took: {time.time() - start_time} seconds")

# Creating NumPy arrays
array1 = np.arange(1000000)
array2 = np.arange(1000000)

# Timing the NumPy arrays addition
start_time = time.time()
result = array1 + array2
print(f"Numpy arrays took: {time.time() - start_time} seconds")
