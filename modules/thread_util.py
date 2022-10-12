
import time
from typing import Callable, List


# def wait_and_check_queue(thread_queue: List, wait_predicate: Callable, recheck_interval: int):
#     while(wait_predicate(len(thread_queue))):
#         for i in range(len(thread_queue) - 1, -1, -1):
#             if thread_queue[i].done():
#                 thread_queue.pop(i)
#         time.sleep(recheck_interval)

def wait_and_check_queue(thread_queue: List, max_thread: int, recheck_interval: int):
    while(len(thread_queue) >= max_thread):
        for i in range(len(thread_queue) - 1, -1, -1):
            if thread_queue[i].done():
                thread_queue.pop(i)
        time.sleep(recheck_interval)
