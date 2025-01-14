import argparse
import logging

import randomname

from solver.game import GameSolver
from solver.query import ApiException

logging.basicConfig(
    level="DEBUG", format='%(asctime)s %(levelname)s %(message)s')

SIMPLE = 'simple'
ALL = 'all'


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Script that solves online Maze"
    )
    parser.add_argument("--solve", required=True,
                        type=str, help=f"'{SIMPLE}' to find first solution, '{ALL}' to find all solutions")

    opts = parser.parse_args()
    solve = opts.solve
    if solve not in [SIMPLE, ALL]:
        logging.error("Please use '%s' or '%s' for solve option", SIMPLE, ALL)
        exit(1)

    try:

        player_name = randomname.get_name()
        solver = GameSolver(player_name)

        if solve == SIMPLE:
            solution = solver.find_first_solution()
            solutions = [solution] if solution else None
        elif solve == ALL:
            solutions = solver.find_all_solutions()

        solver.print_solutions(solutions)

    except ApiException as e:
        logging.error("Game aborted : %s", e)
