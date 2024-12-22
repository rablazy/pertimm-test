import logging

from .models import (Box, BoxTypeEnum, Node, Play, get_unvisited_leaves,
                     printTree)
from .query import *
from .urls import *

logging.basicConfig(level="DEBUG", format='%(asctime)s %(levelname)s %(message)s')

class GameSession(object):

    def __init__(self, player_name):
        self.player_name = player_name
        self.play = None

    def start(self):
        logging.info("Starting game for player: %s", self.player_name)
        response = post(START_URL, dict(player=self.player_name))
        if response["player"]:
            self.play = Play(**response)
            logging.info("Game started, player at pos %s", self.current_pos())
        else:
            raise ApiException("Game not started, player not set")

    def win(self):
        return self.play.win if self.play else False

    def lose(self):
        return self.play.dead if self.play else False

    def current_pos(self):
        if self.play:
            return self.play.position_x - 1, self.play.position_y - 1
        return None

    def discover(self):
        logging.info("Discover map ..")
        moves = []
        if self.play:
            paths = get(self.play.url_discover)
            for path in paths:
                box = Box(path["x"], path["y"], path["move"], path["value"])
                moves.append(box)
                logging.debug(box.__repr__())
        return moves

    def move_to(self, box: Box):
        if self.play:
            logging.info("Moving to x: %s, y: %s ...", box.x, box.y)
            response = post(self.play.url_move, {"position_x" : box.x, "position_y": box.y})
            logging.debug(response)
            self.play = Play(**response)


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


    def forward(self, to_node=None):
        if self.cnode:
            if not to_node:
                to_node = self.cnode.choose_path() or self.cnode.parent
            if to_node and not to_node.is_root(): # do not allow go back to root
                self.move_to(to_node.pos)
                to_node.visited = True
                if not self.win() and not self.lose():
                    if not to_node.has_childs():
                        to_node.set_childs(filter(lambda x : x.move, self.discover()))
                self.cnode = to_node
                return True
        return False


    def backward(self):
        if self.cnode and not self.cnode.is_root():
            self.move_to(self.cnode.parent_pos())
            self.cnode = self.cnode.parent


    def find_first_solution(self):
        self.cnode = self.root
        path = [self.root.pos]

        while not self.win():
            if self.forward() :
                path.append(self.cnode.pos)
            else:
                break

        if self.win():
            logging.info(
                "Game ended after %s moves at %s :  %s",
                len(path), self.current_pos(), self.play.message
            )
            return path

        return None


    def find_all_solutions(self):
        self.cnode = self.root
        first_run = True

        solutions = []
        path = []
        leaves = []

        while first_run or leaves:
            path = [self.root.pos]
            if not first_run:
                if leaves:
                    self.restart()
                    leaves.sort(key=lambda leaf: leaf.pos.x)
                    preferred_path = leaves[0]
                    logging.debug("+++++ Using path to leaf %s", preferred_path.pos)
                    ancestor_pos = preferred_path.ancestor_pos()
                    for p in ancestor_pos[1:]:
                        self.move_to(p)
                        path.append(p)
                    self.cnode = preferred_path
                else:
                    break

            while not self.win():
                if self.forward():
                    path.append(self.cnode.pos)
                else:
                    break

            if self.win():
                solutions.append(path.copy())
                logging.info(
                    "Solution found after %s moves at %s :  %s",
                    len(path), self.current_pos(), self.play.message
                )
                logging.info("***************************************************************************")

            first_run = False
            leaves = list(get_unvisited_leaves(self.root))
            logging.debug(f"Unexplored nodes ===>")
            for leaf in leaves:
                logging.debug(leaf.__repr__())

        # printTree(self.root)

        return solutions


    def _init_root(self):
        start_x, start_y = self.current_pos()
        if self.root is None:
            self.root = Node(
                Box(start_x, start_y, True, BoxTypeEnum.HOME.value),
                childs = list(filter(lambda x : x.move, self.discover()))
            )
            self.root.visited = True

