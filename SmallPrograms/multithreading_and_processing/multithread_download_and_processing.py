# Title: Download data from multiple sources simultaneously and process them

# You have a URL list, from which data need to be downloaded.
# After downloading it each thread analyses data and displays a result (for example word count)
# Make use of the queue (queue.Queue) to store URLs and 


import threading
import queue
import requests # for downloading data from URLs
import time

# Except function - downloading and processing data
def download_and_process(q):
	while not q.empty():
		url, filename = q.get()
		try:
			print(f"Pobieram: {url}")
			response = requests.get(url)
			response.raise_for_status()	#What is it??
			content = response.text
			# Data analysis: count words in text
			word_count = len(content.split())
			print(f"Downloaded from {url}, number of words: {word_count}")

			# Saving results to file
			with open(filename, 'w', encoding='utf-8') as f:   #why utf??
				f.write(content)

		except requests.RequestException as e:
			print(f"Error downloading {url}: {e}")
		finally:
			q.task_done()

# URL list (examplary data)
urls = [
	"https://www.example.com",
	"https://www.python.org",
	"https://httpbin.org/get"
]

# Creating file names for each URL
filenames = [f"plik_{i}.txt" for i in range(len(urls))]

# Creating queue and adding data
q = queue.Queue()
for item in zip(urls, filenames):
	q.put(item)

# Creating exceptions
threads = []
for _ in range(3): #Tree threads
	t = threading.Thread(target=download_and_process, args=(q,))
	t.start()
	threads.append(t)

# Awaiting complition
for t in threads:
	t.join()

print("Downloading and processing completed.")