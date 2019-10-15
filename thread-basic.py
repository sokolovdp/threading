import threading
import logging
import time
import random


logging.basicConfig(level=logging.INFO, format='[%(levelname)s])] [%(threadName)s] [%(message)s]')


def sum_naming(a, b):
    thread_name = threading.current_thread().getName()
    logging.info(f'{thread_name} thread starting')
    print(a+b)
    time.sleep(1)
    logging.info(f'{thread_name} thread ending')


def waiting_for_event(e):
    logging.info('waiting for event....')
    event_is_set = e.wait()
    logging.info(f'event has happened {event_is_set}')


def show(local):
    try:
        val = local.val
    except AttributeError:
        logging.info('No value yet')
    else:
        logging.info('value=%s', val)


def f(local):
    show(local)
    local.val = random.randint(1, 100)
    show(local)


my_threads = []
if __name__ == '__main__':

    my_event = threading.Event()
    waiting_thread = threading.Thread(name='waiter', target=waiting_for_event, args=(my_event,))
    waiting_thread.start()

    for i in range(5):
        t = threading.Thread(name=f'my_new_thread_{i}', target=sum_naming, args=(i, i))
        my_threads.append(t)

    for thread in my_threads:
        thread.setDaemon(True)
        thread.start()
        print(thread.is_alive(), thread.isDaemon())

    for thread in threading.enumerate():
        if thread is threading.current_thread():
            continue
        if thread.getName() == 'waiter':
            continue
        logging.info(f'joining {thread.getName()}')
        thread.join()

    my_event.set()

    time.sleep(3)

    logging.info(f'testing local thread storage..........')
    d = threading.local()
    show(d)
    d.val = 999
    show(d)

    for i in range(2):
        t = threading.Thread(target=f, args=(d,))
        t.start()

    print('STOP TEST!!!!!!')
