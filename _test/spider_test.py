import sys
import time
sys.path.append('..')
from game import Game
import request as req

start = 1
end = 1000

with open('game.txt','a',encoding='utf-8') as f:
    for i in range(start, end+1):
        print('\n=============={}==============\n'.format(i))
        html = req.get_html(i)
        game = Game.getGameByHtml(i, html)
        if game.err:
            continue
        f.write('\n=============={}==============\n'.format(i))
        f.write(str(game))
        print('Write {} done.'.format(i))
        time.sleep(0.05)
        

