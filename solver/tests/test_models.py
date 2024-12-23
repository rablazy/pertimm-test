from ..models import Cell, CellType, Node, get_unvisited_leaves


def test_cell():
    home = Cell(1, 2, True, CellType.HOME.value)
    stop = Cell(10, 4, True, CellType.STOP.value)
    assert (home.is_home())
    assert (stop.is_stop())
    assert (home != stop)


def test_node():

    root = Node(
        Cell(1, 2, True, CellType.HOME),
        childs=[
            Cell(0, 1, False, CellType.WALL.value),
            Cell(1, 1, False, CellType.WALL.value),
            Cell(1, 3, True, CellType.PATH.value),
            Cell(2, 2, True, CellType.PATH.value),
        ]
    )

    assert (root.is_root())
    assert (root.has_childs())
    assert (len(root.childs) == 4)
    assert (all([isinstance(n, Node) for n in root.childs]) is True)
    assert (root.child(0).has_childs() is False)
    assert (root.child(0).reachable() is False)
    assert (root.child(0).pos.role == CellType.WALL)
    assert (root.child(1).is_leaf())

    root.child(2).visited = True  # cell(1,3)
    root.child(2).add_child(Cell(1, 4, False, CellType.WALL))

    path = root.choose_path()  # should return unvisited cell of type PATH
    assert (path is not None)
    assert (path.pos == Cell(2, 2))

    path.add_child(Cell(3, 2, True))
    path.add_child(Cell(2, 3, True))
    leaf1 = path.child(0)
    leaf2 = path.child(1)
    assert (leaf1.parent_pos().at(2, 2))
    assert (leaf1.pos.at(3, 2))

    path_to_leaf1 = leaf1.ancestor_pos()
    assert (path_to_leaf1 is not None and len(path_to_leaf1) == 3)
    assert (path_to_leaf1[0].at(1, 2))
    assert (path_to_leaf1[1].at(2, 2))

    unvisited_leaves = list(get_unvisited_leaves(root))
    assert (unvisited_leaves is not None and len(unvisited_leaves) == 2)
    assert (unvisited_leaves[0] == leaf1)
    assert (unvisited_leaves[1] == leaf2)
    assert (unvisited_leaves[0].visited is False)
