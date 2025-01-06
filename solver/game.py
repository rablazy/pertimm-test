
import logging
from typing import List

from .models import (Cell, CellType, Node, Player, get_unvisited_leaves,
                     printTree)
from .query import ApiException
from .settings import settings
from .urls import *

logging.basicConfig(
    level="DEBUG", format='%(asctime)s %(levelname)s %(message)s')

if settings.FAKE:
    from .fake_query import get, post
else:
    from .query import get, post


class GameSession(object):

    def __init__(self, player_name: str):
        self.player_name = player_name
        self.play: Player = None

    def start(self):
        logging.info("Starting game for player: %s", self.player_name)
        response = post(START_URL, dict(player=self.player_name))
        if response["player"]:
            self.play = Player(**response)
            logging.info("Game started, player at pos %s", self.current_pos())
        else:
            raise ApiException("Game not started, player not set")

    def current_pos(self):
        if self.play:
            return self.play.position_x, self.play.position_y
        return None, None

    def discover(self) -> List[Cell]:
        logging.info("Discover map ..")
        moves = []
        if self.play:
            paths = get(self.play.url_discover)
            for path in paths:
                cell = Cell(path["x"], path["y"], path["move"], path["value"])
                moves.append(cell)
                logging.debug(cell.__repr__())
        return moves

    def move_to(self, cell: Cell):
        if self.play:
            logging.info("Moving to x: %s, y: %s ...", cell.x, cell.y)
            response = post(self.play.url_move, {
                            "position_x": cell.x, "position_y": cell.y})
            logging.debug(response)
            self.play = Player(**response)

    def lose(self):
        return self.play.dead if self.play else False

    def win(self):
        return self.play.win if self.play else False


class GameSolver(GameSession):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start()
        self.root = None
        self._init_root()
        self.cnode = None

    def restart(self):
        self.start()
        self.cnode = self.root

    def find_first_solution(self):
        self.cnode = self.root
        path = [self.root.pos]

        while not self.win() and not self.lose():
            if self._forward():
                path.append(self.cnode.pos)
            else:
                if self.cnode.parent:
                    self._backward()
                    if path:
                        path.pop()
                else:
                    break

        if self.lose():
            logging.info("You lose at %s : %s",
                         self.current_pos(), self.play.message)

        if self.win():
            logging.info(
                "Game win after %s moves at %s :  %s",
                len(path), self.current_pos(), self.play.message
            )
            return path

        return None

    def find_all_solutions(self):
        self.cnode = self.root
        first_run = True

        leaves = []
        solutions = []

        while first_run or leaves:
            if first_run:
                path = [self.root.pos]
            else:
                path = []
                if leaves:
                    self.restart()
                    leaves.sort(key=lambda leaf: leaf.pos.x)
                    preferred_path = leaves[0]
                    logging.debug("+++++ Using path to leaf %s",
                                  preferred_path.pos)
                    ancestor_pos = preferred_path.ancestor_pos()
                    for p in ancestor_pos:
                        self.move_to(p)
                        path.append(p)
                    self.cnode = preferred_path
                else:
                    break

            while not self.win() and not self.lose():
                if self._forward():
                    path.append(self.cnode.pos)
                else:
                    if self.cnode.parent:
                        self._backward()
                        if path:
                            path.pop()
                    else:
                        break

            if self.lose():
                logging.info("You lose at %s : %s",
                             self.current_pos(), self.play.message)
                return []

            if self.win():
                logging.info(
                    "Solution found after %s moves at %s :  %s",
                    len(path), self.current_pos(), self.play.message
                )
                print(*path, sep=" -> ")
                solutions.append(path.copy())

            first_run = False
            leaves = list(get_unvisited_leaves(self.root))
            logging.debug(f"Unexplored nodes ===>")
            for leaf in leaves:
                logging.debug(leaf.__repr__())

            # input()

        # printTree(self.root)
        return solutions

    @classmethod
    def print_solutions(cls, solutions):
        if solutions:
            logging.info("\n\n------ Found %s solutions ------",
                         len(solutions))
            solutions.sort(key=len)
            for i, solution in enumerate(solutions):
                assert (len(solution) > 0)
                logging.info("\nSolution #%s using %s moves:",
                             i+1, len(solution) - 1)
                print(*solution, sep=" -> ")
        else:
            logging.info("Found no solution :((")

    def _forward(self):
        if self.cnode:
            to_node = self.cnode.choose_path()
            if to_node and not to_node.pos.is_home():  # do not allow go back to root
                self.move_to(to_node.pos)
                to_node.visited = True
                if not self.win() and not self.lose():
                    if not to_node.has_childs():
                        to_node.set_childs(
                            filter(lambda x: x.move and not x.is_trap(), self.discover()))
                self.cnode = to_node
                # logging.debug(self.cnode)
                return True
        return False

    def _backward(self):
        if self.cnode and not self.cnode.pos.is_home():
            self.move_to(self.cnode.parent_pos())
            self.cnode = self.cnode.parent

    def _init_root(self):
        start_x, start_y = self.current_pos()
        if self.root is None:
            self.root = Node(
                Cell(start_x, start_y, True, CellType.HOME.value),
                childs=list(
                    filter(lambda x: x.move and not x.is_trap(), self.discover()))
            )
            self.root.visited = True
