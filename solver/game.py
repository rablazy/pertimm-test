import logging

from .models import Box, Play
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
            return True
        return False

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
