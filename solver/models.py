import enum
import posix
from datetime import datetime
from operator import attrgetter
from typing import List

__all__ = ['Play', 'BoxTypeEnum', 'Box', 'Node']


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

    def __init__(self, x:int, y:int, move:bool, box_type:str):
        self.x = x
        self.y = y
        self.move = move
        self.box_type = BoxTypeEnum(box_type).name


    def __str__(self):
        return f"({self.x}, {self.y}):{self.box_type}"

    def __eq__(self, other):
        if not isinstance(other, Box):
            return False
        if other is None:
            return False
        return self.x == other.x and self.y == other.y


class Node:

    def __init__(
        self,
        pos:Box,
        parent: Box = None,
        moves : List[Box] = [],
        visited: bool = False,
        last_visited = None
    ):
        self.pos = pos
        self.parent = parent
        self.childs = []
        self.set_childs(moves)
        self.visited = visited
        self.last_visited = last_visited


    def __str__(self) -> str:
        return f"{ self.pos}, visited: {self.visited}, on: {self.last_visited} \nchilds => { ' - '.join(c.pos.__str__() for c in self.childs)} "

    def set_childs(self, moves : List[Box]) -> None:
        if moves:
            for m in moves:
                parent_pos = self.parent.pos if self.parent else None
                if not m == parent_pos and not m == self.pos:
                    self.add_child(m)

    def add_child(self, child:Box) -> None:
        self.childs.append(Node(child, self))

    def has_childs(self) -> bool:
        return len(self.childs) > 0 if self.childs else False

    def reachable(self) -> bool:
        return self.pos.move

    def choose_path(self) -> "Node":
        paths = list(filter(lambda x : x.reachable(), self.childs))
        paths  = sorted(paths, key = lambda x : (x.visited, x.last_visited))
        for p in paths:
            print(p.pos)
        return paths[0] if paths else None


    @property
    def visited(self) -> bool:
        return self._visited

    @visited.setter
    def visited(self, value):
        self._visited = value

    @property
    def last_visited(self) -> datetime:
        return self._last_visited

    @last_visited.setter
    def last_visited(self, value):
        self._last_visited = value


