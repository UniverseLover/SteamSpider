import logging
import time
import math
from concurrent.futures import ThreadPoolExecutor
from os import cpu_count

import db
from game import Game
from request import get_html

thread_count = cpu_count()*2 if cpu_count() >= 4 else 16
start = 1
end = 1000000
report_count = 100
unit = (end-start)//thread_count
start_li = [start+i*unit for i in range(thread_count)]

logging.basicConfig(level=logging.INFO)


def run(start, end, woker_id, time_verbose, press_test=False):

    tic = time.time()

    logging.info('Woker {} started.'.format(
        woker_id))
    try:
        for i in range(start, end):
            if i % (unit//report_count) == 0:
                logging.info('Woker {} work to page {}({:.2f}%).'.format(
                    woker_id, i, 100*(i-start)/(end-start)))
            html = get_html(i)
            game = Game.getGameByHtml(i, html)
            if game.err:
                continue
            bson = game.get_json()
            if not press_test:
                db.storage(bson)
    except Exception as e:
        logging.error(e.__str__()+'[woker={}]'.format(woker_id))

    logging.info('Woker {} done.'.format(woker_id))

    toc = time.time()

    if time_verbose:
        logging.info('Woker {} work used {:.2f}min.'.format(
            woker_id, (toc-tic)/60))


def main(time_verbose=0):
    with ThreadPoolExecutor(max_workers=cpu_count()*5) as pool:
        for ix, i in enumerate(start_li):
            t = pool.submit(run, i, i+unit, ix, time_verbose)


def press_test():
    print('Press test start.')
    start, end, report_count, last_time = 1, 50, 1, math.inf
    for thread_count in range(1, 100):
        print('testing {}-thread mode'.format(thread_count))

        tic = time.time()
        for i in range(5):
            unit = (end-start)//thread_count
            start_li = [start+i*unit for i in range(thread_count)]
            with ThreadPoolExecutor(max_workers=100) as pool:
                for ix, i in enumerate(start_li):
                    t = pool.submit(run, i, i+unit, ix, 0, True)
        toc = time.time()
        tictoc = (toc - tic)/5
        if tictoc > last_time:
            if thread_count == 2:
                print("It's strange,but it's science!")
            print('It is seemed the best number of thread count is {}.[time={:.2f}]'.format(
                thread_count-1, last_time))
            return thread_count-1
        else:
            last_time = tictoc


if __name__ == '__main__':
    print("Welcome to Steam Spider!(version=1.0)")
    main()