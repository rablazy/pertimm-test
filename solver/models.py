import enum
import logging
from typing import Generator, Iterable, List

__all__ = ['Play', 'BoxTypeEnum', 'Box', 'Node', 'get_unvisited_leaves', 'printTree']

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


    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
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
        self.visited = False


    def __repr__(self) -> str:
        return f"{ self.pos}, parent: {self.parent_pos()}, visited: {self.visited} \nchilds => { ' - '.join(c.pos.__str__() for c in self.childs)} "


    @property
    def visited(self) -> bool:
        return self._visited

    @visited.setter
    def visited(self, value):
        self._visited = value

    def add_child(self, child:Box) -> None:
        self.childs.append(Node(child, self))

    def choose_path(self) -> "Node":
        paths = list(filter(lambda x : x.reachable() and not x.visited, self.childs)) #
        return paths[0] if paths else None

    def is_leaf(self) -> bool:
        return self.childs is None or len(self.childs) == 0

    def is_root(self) -> bool:
        return self.parent is None

    def has_childs(self) -> bool:
        return len(self.childs) > 0 if self.childs else False

    def parent_pos(self) -> Box:
        return self.parent.pos if self.parent else None

    def ancestor_pos(self) -> List[Box]:
        result = []
        s = self.parent
        while s is not None:
            result.append(s.pos)
            s = s.parent
        result.reverse()
        return result

    def reachable(self) -> bool:
        return self.pos.move

    def set_childs(self, moves : Iterable[Box]) -> None:
        for m in moves:
            if not m == self.pos and not m == self.parent_pos() :
                self.add_child(m)


def get_unvisited_leaves(node: Node) -> Generator[Node, None, None]:
    if not node.childs and not node.visited and node.pos.move:
        yield node

    for child in node.childs:
        for leaf in get_unvisited_leaves(child):
            yield leaf


def printTree(root: Node, level=0):
    print("  " * level, root.pos.__repr__())
    for child in root.childs:
        printTree(child, level + 1)













