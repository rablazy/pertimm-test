import logging
from datetime import datetime

from .models import Box, BoxTypeEnum, Node, Play
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
                logging.debug(box)
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


    def forward(self):
        if self.cnode:
            next_node = self.cnode.choose_path() or self.cnode.parent
            self.move_to(next_node.pos)
            next_node.visited = True
            if not self.win() and not self.lose():
                if not next_node.has_childs():
                    next_node.set_childs(self.discover())
            self.cnode = next_node


    def backward(self):
        if self.cnode and not self.cnode.is_root():
            self.move_to(self.cnode.parent_pos())
            self.cnode = self.cnode.parent


    def find_all_solutions(self):

        self.cnode = self.root
        count_move = 0
        while not self.win() and not self.lose():
            self.forward()
            count_move += 1
        logging.info(
            "Game ended after %s moves at %s :  %s",
            count_move, self.current_pos(), self.play.message
        )


    def _init_root(self):
        start_x, start_y = self.current_pos()
        if self.root is None:
            self.root = Node(
                Box(start_x, start_y, True, BoxTypeEnum.HOME.value),
                childs = self.discover()
            )
            self.root.visited = True

