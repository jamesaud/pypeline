import logging

def run_threads(thread_list):
    """
    Add a list of threads, and makes main process wait until they are executed.
    :param thread_list: List[threading.Thread]
    """
    logging.info('Attempting {} concurrent containers...'.format(len(thread_list)))
    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        while thread.is_alive():
            pass

