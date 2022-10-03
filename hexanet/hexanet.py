"""
    Navigation through a hexagonal network.

    Functions
    ---------
    highway_path(depth)
        Returns a default path for a full rotation of a highway at a given depth.
    alt_map(depth)
        Assigns a number to each move, depending on depth.
    alt_index(path, depth)
        Returns the alternative index of the destination node.
    alt_net(path)
        Returns a collection of highways each containing nodes with alternative indices.
    shortcut(path)
        Returns the length of the shortest path from a node to the base node.
    normal_net(depth)
        Returns a collection of highways each containing nodes with normal indices.
    normal_index(path)
        Returns the normal index of a node.
    navigate(path)
        Prints destination and the shortcut to base node from a given path.
"""


def highway_path(depth: int) -> str:
    """
    Returns a default path for a full rotation of a highway at a given depth.

    Parameters
    ----------
    depth: int
        The number of highways.
    """

    default_path = 'ACDEFAB'
    default_path_list = [move*depth for move in default_path]

    return ''.join(default_path_list)


def alt_map(depth: int) -> dict:
    """
    Assigns a number to each move, depending on depth.

    Parameters
    ----------
    depth: int
        The number of highways.

    Returns
    -------
    dict
        A dictionary of moves with their assigned numbers.
    """

    map = {'A': 1}
    map['B'] = depth*2 + 1
    map['C'] = map['B'] - 1
    map['D'] = -map['A']
    map['E'] = -map['B']
    map['F'] = -map['C']

    return map


def alt_index(path: str, depth: int) -> int:
    """
    Returns the alternative index of the destination node.

    Parameters
    ----------
    path: str
        A string of legal moves.
    depth: int
        The number of highways.
    """

    map = alt_map(depth)

    alternative_index = 0
    for move in path:
        alternative_index += map[move]

    return alternative_index


def alt_net(path: str) -> list:
    """
    Returns a collection of highways each containing nodes with alternative indices.

    Parameters
    ----------
    path: str
        A string of legal moves.
    """

    depth = len(path)
    destination = alt_index(path, depth)
    alt_net = [[0]]

    counter = 0
    while counter < depth:
        counter += 1
        default_path = highway_path(counter)
        # passed depth to alt_index(), to uniformly obtain the alternative indices of the default paths.
        highway = [alt_index(default_path[:i+counter], depth)
                   for i in range(len(default_path) - counter)]

        alt_net.append(highway)
        if destination in highway:
            return alt_net

    return alt_net


def shortcut(path: str) -> int:
    """
    Returns the length of the shortest path from a node to the base node.

    Parameters
    ----------
    path: str
        A string of legal moves.
    """

    depth = len(path)
    anet = alt_net(path)
    destination = alt_index(path, depth)

    for highway_index in range(len(anet)):
        if destination in anet[highway_index]:
            return highway_index


def normal_net(depth: int) -> list:
    """
    Returns a collection of highways each containing nodes with normal indices.

    Parameters
    ----------
    depth: int
        The number of highways.
    """

    nnet = [[0]]

    counter = 0
    control = 1
    while counter < depth:
        counter += 1
        highway = []

        for i in range(control, 6*counter+control):
            highway.append(i)

        control = highway[-1] + 1
        nnet.append(highway)

    return nnet


def normal_index(path: str) -> int:
    """
    Returns the normal index of a node.

    Parameters
    ----------
    path: str
        A string of legal moves.
    """

    depth = len(path)
    anet = alt_net(path)
    nnet = normal_net(len(anet)-1)
    destination = alt_index(path, depth)
    indices = [(anet.index(highway), highway.index(destination))
               for highway in anet if destination in highway]

    return nnet[indices[0][0]][indices[0][1]]


def navigate(path: str) -> None:
    """
    Prints path, destination and the shortcut to base node.

    Parameters
    ----------
    path: str
        A string of legal moves.
    """

    print(f"Path: {path}\n")
    print(f"Destination: Node({normal_index(path)})\n")
    print(f"Shortcut to Base Node: {shortcut(path)}")
