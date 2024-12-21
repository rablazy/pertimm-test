import logging
from datetime import datetime

import randomname

from solver.game import GameSession, GameSolver
from solver.models import Box, BoxTypeEnum, Node
from solver.query import ApiException, HttpError

logging.basicConfig(level="DEBUG", format='%(asctime)s %(levelname)s %(message)s')

if __name__ == "__main__":

    try:

        player_name = randomname.get_name()
        solver = GameSolver(player_name)
        solver.find_all_solutions()

    except (HttpError, ApiException) as e:
        logging.error("Game aborted : %s", e)
