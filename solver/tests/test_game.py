
import logging

from ..game import GameSolver

logging.basicConfig(
    level="DEBUG", format='%(asctime)s %(levelname)s %(message)s')


def test_solver_one_solution():

    solver = GameSolver("david")

    solution = solver.find_first_solution()
    if solution:
        assert (len(solution) > 0)
        logging.info("Solution after %s moves:", len(solution))
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
            logging.info("Solution #%s after %s moves:", i+1, len(solution))
            print(*solution, sep=" -> ")
    else:
        logging.info("Found no solution :((")
