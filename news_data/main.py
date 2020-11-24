#! /usr/bin/python3
# coding=utf-8

import time
import json
import random
import multiprocessing
from get_data import get_essay, get_url, get_url_numbers


def json_read():
	config = dict()
	try:
		with open('conf.json', 'r') as f:
			config = json.load(f)
	except Exception as error:
		print(error)
	return config


def crawler(q, index):
	process_id = 'Process-' + str(index)
	while not q.empty():
		url = q.get(timeout=2)
		get_essay(url)
		# print(type(url))

		numbers = q.qsize()
		if numbers % 5 == 0:
			sleep_time = 15 + random.random()
			print(f"\t{process_id} sleep {sleep_time}s", numbers)
		else:
			sleep_time = random.randint(0, 2) + random.random()
			print(f"\t{process_id} sleep {sleep_time}s", numbers)
		if numbers % 50 == 0:
			sleep_time = 12 * 60 + random.random()
			print(f"\t{process_id} sleep {sleep_time}s", numbers)
		time.sleep(sleep_time)

		print(process_id, numbers, end=" ")


def main():
	start = time.time()
	manager = multiprocessing.Manager()
	numbers = get_url_numbers()
	work_queue = manager.Queue(numbers)
	for url in get_url():
		work_queue.put(url)
	n = 1
	pool = multiprocessing.Pool(processes=n)
	for i in range(n):
		pool.apply_async(crawler, args=(work_queue, i))

	print("Started processes")
	pool.close()
	pool.join()

	end = time.time()
	print("此次爬虫运行总时间：", end - start)


if __name__ == '__main__':
	main()
