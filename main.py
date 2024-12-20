import logging
from datetime import datetime

import randomname

from solver.game import GameSession
from solver.models import Box, BoxTypeEnum, Node

logging.basicConfig(level="DEBUG", format='%(asctime)s %(levelname)s %(message)s')

if __name__ == "__main__":
    player_name = randomname.get_name()
    session = GameSession(player_name)
    if session.start():
        start_x, start_y = session.current_pos()
        root_node = Node(
            Box(x=start_x, y=start_y, move=True, box_type=BoxTypeEnum.HOME.value),
            moves = session.discover(),
            visited = True,
            last_visited = datetime.now()
        )
        current_node = root_node
        logging.info(current_node)
        while not session.win() and not session.lose():
            # add condition stop if go back to home two times, to avoid infinite loop
            next_move = current_node.choose_path() or current_node.parent # go back to parent if no route
            session.move_to(next_move.pos)
            next_move.visited = True
            next_move.last_visited = datetime.now()
            if not session.win() and not session.lose():
                if not next_move.has_childs():
                    next_move.set_childs(session.discover())
                current_node = next_move
            logging.info(current_node)

        logging.debug(session.play.__dict__)
        logging.info("Game ended, you %s !", "WIN" if session.win() else "LOSE")


    else:
        logging.error("Game not started !")
