import enum
import logging
from datetime import datetime
from typing import List

__all__ = ['Play', 'BoxTypeEnum', 'Box', 'Node']

logging.basicConfig(level="DEBUG", format='%(asctime)s %(levelname)s %(message)s')


class Play:

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.__dict__.update(kwargs)


class BoxTypeEnum(enum.Enum):
    WALL = "wall"
    PATH = "path"
    TRAP = "trap"
    HOME = "home"
    STOP = "stop"


class Box:

    def __init__(self, x:int, y:int, move:bool, role:str):
        self.x = x
        self.y = y
        self.move = move
        self.role = BoxTypeEnum(role).name


    def __str__(self):
        return f"({self.x}, {self.y}):{self.role}"

    def __eq__(self, other):
        if not isinstance(other, Box):
            return False
        if other is None:
            return False
        return self.x == other.x and self.y == other.y

    def is_home(self):
        return self.role == BoxTypeEnum.HOME

    def is_stop(self):
        return self.role == BoxTypeEnum.STOP


class Node:

    def __init__(
        self,
        pos:Box,
        parent: "Node" = None,
        childs : List[Box] = []
    ):
        self.pos = pos
        self.parent = parent
        self.childs = []
        self.set_childs(childs)
        self.last_visited = None
        self.visited = False


    def __str__(self) -> str:
        return f"{ self.pos}, visited: {self.visited}, on: {self.last_visited} \nchilds => { ' - '.join(c.pos.__str__() for c in self.childs)} "


    @property
    def visited(self) -> bool:
        return self._visited

    @visited.setter
    def visited(self, value):
        self._visited = value
        self.last_visited = datetime.now()

    @property
    def last_visited(self) -> datetime:
        return self._last_visited

    @last_visited.setter
    def last_visited(self, value):
        self._last_visited = value

    def parent_pos(self) -> Box:
        return self.parent.pos if self.parent else None

    def set_childs(self, moves : List[Box]) -> None:
        if moves:
            for m in moves:
                if m.move and not m == self.pos and not m in self.previous_pos() :
                    self.add_child(m)

    def add_child(self, child:Box) -> None:
        self.childs.append(Node(child, self))

    def has_childs(self) -> bool:
        return len(self.childs) > 0 if self.childs else False

    def reachable(self) -> bool:
        return self.pos.move

    def choose_path(self) -> "Node":
        paths = list(filter(lambda x : x.reachable() and not x.visited, self.childs))
        return paths[0] if paths else None

    def is_leaf(self) -> bool:
        return self.childs is None or len(self.childs) == 0

    def is_root(self) -> bool:
        return self.parent is None

    def previous_pos(self) -> List[Box]:
        result = []
        s = self.parent
        while s is not None:
            result.append(s.pos)
            s = s.parent
        result.reverse()
        return result






