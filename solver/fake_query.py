import logging
from typing import Dict

from .urls import START_URL

__all__ = ["post", "get"]

logging.basicConfig(
    level="DEBUG", format='%(asctime)s %(levelname)s %(message)s')


class Point(object):

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Maze:

    def __init__(self) -> None:
        self.matrix = [
            ['W', 'P', 'P', 'P', 'P', 'W', 'W', 'P'],
            ['P', 'P', 'T', 'P', 'P', 'P', 'P', 'P'],
            ['H', 'W', 'W', 'T', 'P', 'T', 'W', 'W'],
            ['P', 'W', 'P', 'P', 'S', 'P', 'P', 'T'],
            ['P', 'P', 'P', 'W', 'P', 'W', 'P', 'P'],
            ['P', 'W', 'T', 'W', 'W', 'P', 'W', 'P'],
            ['P', 'W', 'W', 'W', 'W', 'P', 'W', 'P'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
        ]
        self.home = None
        self.exit = None
        self.position = None
        self.dead = False
        self.win = False
        self.player = None
        self.size = len(self.matrix)

    def start(self, player_name):
        self.player = player_name
        if player_name:
            for x in range(self.size):
                for y in range(self.size):
                    if self.matrix[y][x] == 'H':
                        self.home = Point(x, y)
                        self.position = Point(x, y)
                    if self.matrix[y][x] == 'S':
                        self.exit = Point(x, y)
            if self.home is None:
                raise ValueError("Home not set")
            if self.exit is None:
                raise ValueError("Exit not set")

            self.dead = False
            self.win = False

        return self.response()

    def discover(self):
        p1 = self._get(self.position.x - 1, self.position.y)
        p2 = self._get(self.position.x, self.position.y-1)
        p3 = self._get(self.position.x, self.position.y + 1)
        p4 = self._get(self.position.x + 1, self.position.y)
        paths = []
        if p1:
            paths.append(p1)
        if p2:
            paths.append(p2)
        if p3:
            paths.append(p3)
        if p4:
            paths.append(p4)
        return paths

    def response(self, message="Ready to move"):
        return {
            "player": self.player,
            "message": message,
            "position_x": self.position.x if self.position else None,
            "position_y": self.position.y if self.position else None,
            "dead": self.dead,
            "win": self.win,
            "url_move": f"{self.player}/move/",
            "url_discover": f"{self.player}/discover/"
        }

    def move_to(self, x, y):

        if self.win:
            return self.response("You already won !")
        if self.dead:
            return self.response("You already dead !")

        data = self.matrix[y][x]
        if data:

            if data == 'W':
                response = self.response("Cannot go into wall !")
            else:
                self.position = Point(x, y)

            if data == 'T':
                self.dead = True
                response = self.response("You lose :p !")
            if data == 'S':
                self.win = True
                response = self.response("You win dude, congrats !")
            if data == 'P' or data == 'H':
                response = self.response()

            return response

        return self.response()

    def _get(self, x, y):
        if x >= 0 and x < self.size and y >= 0 and y < self.size:
            data = self.matrix[y][x]
            if data == 'W':
                d = "wall"
            elif data == 'H':
                d = "home"
            elif data == 'T':
                d = "trap"
            elif data == 'P':
                d = "path"
            elif data == 'S':
                d = "stop"
            return {
                "x": x,
                "y": y,
                "move": data != 'W',
                "value": d
            }
        else:
            return None


maze = Maze()


def post(url: str, payload=None):
    if url == START_URL:
        return maze.start(payload["player"])
    if "move" in url:
        return maze.move_to(payload["position_x"], payload["position_y"])
    return {}


def get(url: str, payload: Dict = {}):
    if "discover" in url:
        return maze.discover()
    return {}
