# Parallel data processing by using multithreading and queues

# Task: create a program processing data in parallel threads using queues and zip function

import threading 
import queue
import time

# Thread function - processing elements from queue

def worker(q):
	while not q.empty():     #why while not empty??
		item = q.get()
		print(f"Przetwarzanie {item}")
		time.sleep(1) # Processing Time Simulation
		q.task_done()	# what does it do??


# Input data (from two lists)
numbers = [1, 2, 3]		# can you combine data from two files??
letters = ['a', 'b', 'c']

# Joining data with zip() function
combined = list(zip(numbers, letters)) # [(1, 'a'), (2, 'b'), (3, 'c')]

# Creating queue and adding data
q = queue.Queue()
for item in combined:
	q.put(item)

# Creating threads
threads = []
for _ in range(3): # Tree threads      why tree threads??
	t = threading.Thread(target=worker, args=(q, ))  # what are these parameters, also daemon?
	t.start()
	threads.append(t)

# Awaiting for processing completion
for t in threads:
	t.join()

print("All data has been processed.")