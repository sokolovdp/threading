import threading
import logging
import time
import random


logging.basicConfig(level=logging.INFO, format='[%(levelname)s])] [%(threadName)s] [%(message)s]')


class MyCounter:
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.counter = start

    def increment(self):
        logging.info('waiting for lock')
        self.lock.acquire()
        try:  # in case of any error, lock must be released!
            logging.info('lock acquired')
            self.counter += 1
        finally:
            self.lock.release()


def worker(counter):
    for _ in range(3):
        r = random.random()
        logging.info('sleeping %0.02f', r)
        time.sleep(r)
        counter.increment()
    logging.info('worker done')


if __name__ == '__main__':

    my_lock = threading.Lock()
    print('1st lock', my_lock.acquire())
    print('2nd lock', my_lock.acquire(blocking=True, timeout=0.5))
    print('3rd lock', my_lock.acquire(blocking=False))
    my_lock.release()

    my_rlock = threading.RLock()
    print('1st Rlock', my_rlock.acquire())
    print('2nd Rlock', my_rlock.acquire())
    print('3rd Rlock', my_rlock.acquire())
    my_rlock.release()
    my_rlock.release()
    my_rlock.release()

    with my_lock:
        time.sleep(2)
        logging.info('in the with statement')
        print('my lock', my_lock.acquire(blocking=False))
    my_lock = threading.Lock()
    print('my lock', my_lock.acquire())
    my_lock.release()

    exit()

    counter = MyCounter()
    for i in range(3):
        t = threading.Thread(target=worker, args=(counter,))
        t.start()

    logging.info('waiting for worker threads........')
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    logging.info('final counter value: %d', counter.counter)
