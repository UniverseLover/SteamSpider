from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from game import Game
import db
import request as req
import logging

thread_count = cpu_count()*2
start = 1
end = 1000000
unit = (end-start)//thread_count
start_li = [start+i*unit for i in range(thread_count)]

logging.basicConfig(level=logging.INFO)


def run(start, end, woker_id):

    count = 0

    for i in range(start, end):
        if count % 2000 == 0:
            logging.info('Woker {} work to page {}({}%).'.format(
                woker_id, i, 100*(i-start)/(end-start)))
        html = req.get_html(i)
        game = Game.getGameByHtml(i, html)
        if game.err:
            continue
        bson = game.get_json()
        db.storage(bson)

        count += 1
    logging.info('Woker {} done.'.format(woker_id))


def main():

    with ThreadPoolExecutor(max_workers=thread_count) as pool:
        for ix, i in enumerate(start_li):
            t = pool.submit(run, i, i+unit, ix)


if __name__ == '__main__':
    main()
