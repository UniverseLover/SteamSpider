from concurrent.futures import ThreadPoolExecutor
from os import cpu_count
from game import Game
from request import get_html
import db
import logging


thread_count = cpu_count()*2
start = 1
end = 1000000
unit = (end-start)//thread_count
start_li = [start+i*unit for i in range(thread_count)]

logging.basicConfig(level=logging.INFO)


def run(start, end, woker_id):

    logging.info('Woker {} started.'.format(
        woker_id))
    try:
        for i in range(start, end):
            if i % (unit//200) == 0:
                logging.info('Woker {} work to page {}({:.2f}%).'.format(
                    woker_id, i, 100*(i-start)/(end-start)))
            html = get_html(i)
            game = Game.getGameByHtml(i, html)
            if game.err:
                continue
            bson = game.get_json()
            #db.storage(bson)
    except Exception as e:
        logging.error(e.__str__()+'[woker={}]'.format(woker_id))

    logging.info('Woker {} done.'.format(woker_id))


def main():
    with ThreadPoolExecutor(max_workers=cpu_count()*5) as pool:
        for ix, i in enumerate(start_li):
            t = pool.submit(run, i, i+unit, ix)


if __name__ == '__main__':
    print("Welcome to Steam Spider!(version=0.8)")
    main()
