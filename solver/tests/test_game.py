
import pytest

from ..query import ApiException
from ..settings import settings  # noqa

settings.FAKE = True  # noqa
from ..game import GameSolver  # noqa


def test_start_error():
    with pytest.raises(ApiException) as excinfo:
        solver = GameSolver("")
    assert str(excinfo.value) == "Game not started, player not set"


def test_solver_one_solution():

    solver = GameSolver("david")

    solution = solver.find_first_solution()
    solutions = [solution] if solution else None
    solver.print_solutions(solutions)


def test_solver_all_solutions():
    solver = GameSolver("georges")
    solver.print_solutions(solver.find_all_solutions())
