import logging
from datetime import datetime

import randomname

from solver.game import GameSession
from solver.models import Box, BoxTypeEnum, Node
from solver.query import ApiException, HttpError

logging.basicConfig(level="DEBUG", format='%(asctime)s %(levelname)s %(message)s')

if __name__ == "__main__":
    player_name = randomname.get_name()
    session = GameSession(player_name)
    try:
        if session.start():
            start_x, start_y = session.current_pos()
            root_node = Node(
                Box(start_x, start_y, True, BoxTypeEnum.HOME.value),
                moves = session.discover(),
                visited = True,
                last_visited = datetime.now()
            )
            current_node = root_node
            count_move = 0
            while not session.win() and not session.lose():
                # add condition stop if go back to home two times, to avoid infinite loop
                next_node = current_node.choose_path() or current_node.parent # go back to parent if no route
                session.move_to(next_node.pos)
                next_node.visited = True
                next_node.last_visited = datetime.now()
                count_move += 1
                if not session.win() and not session.lose():
                    if not next_node.has_childs():
                        next_node.set_childs(list(filter(lambda x : x.move is True, session.discover())))
                    current_node = next_node

            logging.info("Game ended after %s moves at %s :  %s", count_move, session.current_pos(), session.play.message)

        else:
            logging.error("Game not started !")

    except (HttpError, ApiException) as e:
        logging.error("Game aborted %s", e)
