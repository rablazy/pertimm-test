import logging

import randomname

from solver.game import GameSolver
from solver.query import ApiException, HttpError

logging.basicConfig(level="DEBUG", format='%(asctime)s %(levelname)s %(message)s')

if __name__ == "__main__":

    try:

        player_name = randomname.get_name()
        solver = GameSolver(player_name)
        #solver.find_first_solution()

        solutions = solver.find_all_solutions()
        logging.info("Found %s solutions :", len(solutions))
        for i, solution in enumerate(solutions):
            logging.info("--- Solution %s after %s moves:", i+1, len(solution))
            print(*solution, sep=" -> ")

    except (HttpError, ApiException) as e:
        logging.error("Game aborted : %s", e)
