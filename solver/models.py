import enum
from typing import Generator, Iterable, List

__all__ = ['Player', 'CellType', 'Cell', 'Node',
           'get_unvisited_leaves', 'printTree']


class Player:

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.__dict__.update(kwargs)


class CellType(enum.StrEnum):
    WALL = "wall"
    PATH = "path"
    TRAP = "trap"
    HOME = "home"
    STOP = "stop"


class Cell:

    def __init__(self, x: int, y: int, move: bool = True, role: str = "path"):
        self.x = x
        self.y = y
        self.move = move
        self.role = CellType(role)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}):{self.role}"

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        if other is None:
            return False
        return self.x == other.x and self.y == other.y

    def at(self, x: int, y: int) -> bool:
        return self.x == x and self.y == y

    def is_home(self):
        return self.role == CellType.HOME

    def is_stop(self):
        return self.role == CellType.STOP

    def is_trap(self):
        return self.role == CellType.TRAP


class Node:

    def __init__(
        self,
        pos: Cell,
        parent: "Node" = None,
        childs: List[Cell] = []
    ):
        self.pos: Cell = pos
        self.parent: Node = parent
        self.track_pos = None
        self.childs: List[Node] = []
        self.set_childs(childs)
        self.visited = False

    @property
    def visited(self) -> bool:
        return self._visited

    @visited.setter
    def visited(self, value):
        self._visited = value

    def add_child(self, child: Cell) -> None:
        if not child in self.ancestor_pos():
            self.childs.append(Node(child, self))

    def ancestor_pos(self) -> List[Cell]:
        """All positions from root to this current node position"""
        if not self.track_pos:
            result = [self.pos]
            s = self.parent
            while s is not None:
                result.append(s.pos)
                s = s.parent
            result.reverse()
            self.track_pos = result
        return self.track_pos

    def child(self, n):
        return self.childs[n] if self.childs else None

    def choose_path(self) -> "Node":
        paths = list(filter(lambda x: x.reachable()
                     and not x.visited and not x.pos in self.ancestor_pos(), self.childs))
        return paths[0] if paths else None

    def has_childs(self) -> bool:
        return len(self.childs) > 0 if self.childs else False

    def is_leaf(self) -> bool:
        return self.childs is None or len(self.childs) == 0

    def is_root(self) -> bool:
        return self.parent is None

    def parent_pos(self) -> Cell:
        return self.parent.pos if self.parent else None

    def reachable(self) -> bool:
        return self.pos.move

    def set_childs(self, moves: Iterable[Cell]) -> None:
        for m in moves:
            self.add_child(m)

    def __repr__(self) -> str:
        return f"""
            {self.pos},
            parent: {self.parent_pos()},
            visited: {self.visited}
            childs => { ' - '.join(c.pos.__repr__() for c in self.childs)}
        """


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
