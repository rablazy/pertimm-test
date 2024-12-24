
import logging

import pytest

from ..query import ApiException
from ..settings import settings  # noqa

settings.FAKE = True  # noqa
from ..game import GameSolver  # noqa

logging.basicConfig(
    level="DEBUG", format='%(asctime)s %(levelname)s %(message)s')


def test_start_error():
    with pytest.raises(ApiException) as excinfo:
        solver = GameSolver("")
    assert str(excinfo.value) == "Game not started, player not set"


def test_solver_one_solution():

    solver = GameSolver("david")

    solution = solver.find_first_solution()
    if solution:
        assert (len(solution) > 0)
        logging.info("Solution using %s moves:", len(solution) - 1)
        print(*solution, sep=" -> ")
    else:
        logging.info("Found no solution :((")


def test_solver_all_solutions():
    solver = GameSolver("georges")
    solutions = solver.find_all_solutions()
    if solutions:
        logging.info("\n\n------ Found %s solutions ------", len(solutions))
        for i, solution in enumerate(solutions):
            assert (len(solution) > 0)
            print("\n")
            logging.info("Solution #%s using %s moves:",
                         i+1, len(solution) - 1)
            print(*solution, sep=" -> ")
    else:
        logging.info("Found no solution :((")
