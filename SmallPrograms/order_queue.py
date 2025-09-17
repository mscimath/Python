import queue
import threading
import time

# Create FIFO queue
order_queue = queue.Queue()

# Function to Process Orders
def process_orders():
	while True:
		try:
			# Collect order from queue (blocks, if the queue is empty)
			order = order_queue.get()
			print(f"Processing order no: {order}")

			# Processing Time Simulation
			time.sleep(2)

			print(f"The order {order} has been processed.")

			# Mark the task as completed
			order_queue.task_done()

		except Exception as e:
			print(f"Error while processing order: {e}")

# Function to add orders to queue
def add_orders():
	for i in range(1, 6):	# Simulate 5 orders
		print(f"Order {i} accepted")
		order_queue.put(f"Order-{i}")
		time.sleep(1) # Simulation of pausing between orders

# Launch thread handling order processing
worker_thread = threading.Thread(target=process_orders, daemon=True)
worker_thread.start()

# Add orders in the main thread
add_orders()

# Wait untill all orders get processed
order_queue.join()
print("All orders has been processed.") 