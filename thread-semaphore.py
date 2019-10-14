import random
import time
import logging
from threading import Semaphore, BoundedSemaphore, Thread

logging.basicConfig(level=logging.INFO, format='[%(levelname)s])] [%(threadName)s] [%(message)s]')

max_items = 5
"""
Consider 'container' as a container, of course, with a capacity of 5
items. Defaults to 1 item if 'max_items' is passed.
"""
container = BoundedSemaphore(max_items)


def producer(nloops):
    for _ in range(nloops):
        time.sleep(random.randrange(2, 5))
        logging.info(f'producer: {time.ctime()}')
        try:
            container.release()
            logging.info("Produced an item.")
        except ValueError:
            logging.info("Full, skipping.")


def consumer(nloops):
    for _ in range(nloops):
        time.sleep(random.randrange(2, 5))
        logging.info(f'consumer: {time.ctime()}')
        """
        In the following if statement we disable the default
        blocking behaviour by passing False for the blocking flag.
        """
        if container.acquire(blocking=False):
            logging.info("Consumed an item.")
        else:
            logging.info("Empty, skipping.")


if __name__ == '__main__':
    n = random.randrange(1, 3)
    logging.info(f"Starting with max_items={max_items} n={n}")
    threads = []
    threads.append(Thread(target=producer, args=(n,)))
    threads.append(Thread(target=consumer, args=(random.randrange(n, n + max_items + 2),)))
    for thread in threads:  # Starts all the threads.
        thread.start()
    for thread in threads:  # Waits for threads to complete before moving on with the main script.
        thread.join()
    logging.info("All done.")

    logging.info("Semaphore vs Bounded Semaphore")
    # Usually, you create a Semaphore that will allow a certain number of threads
    # into a section of code. This one starts at 5.
    s1 = Semaphore(5)

    # When you want to enter the section of code, you acquire it first.
    # That lowers it to 4. (Four more threads could enter this section.)
    s1.acquire()

    # Then you do whatever sensitive thing needed to be restricted to five threads.

    # When you're finished, you release the semaphore, and it goes back to 5.
    s1.release()

    # That's all fine, but you can also release it without acquiring it first.
    s1.release()

    # The counter is now 6! That might make sense in some situations, but not in most.
    logging.info(s1._value)  # => 6

    # If that doesn't make sense in your situation, use a BoundedSemaphore.

    s2 = BoundedSemaphore(5)  # Start at 5.
    s2.acquire()  # Lower to 4.
    s2.release()  # Go back to 5.
    try:
        s2.release()  # Try to raise to 6, above starting value.
    except ValueError:
        logging.info('As expected, it complained.')
