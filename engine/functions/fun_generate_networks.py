"""
函数：生成网络功能
"""

from engine.externals import np, plt, njit
from engine.functions.fun_generate_points import generate_points
from scipy.spatial import Voronoi, voronoi_plot_2d


# 生成连边、路由点，以生成图网络

def generate_network(
        nodes_pos: np.array,
        set_num_edges: int,
        set_num_interpolated_density_distance: float,
        num_edges_per_node: int,
        num_neighbors: int,
        network_machanism: str = 'Voronoi',
):
    """
    生成图网络。

    这个方法的步骤是：
    1. 获取节点之坐标；
    2. 根据网络生成机制生成网络之连边；

    - 网络生成机制有以下可选项：#HACK 现在只做了加权的 Voronoi 图生成网络
        - 'Random': 随机生成网络
        - 'Voronoi': 使用 Voronoi 图生成网络；
        - 'Complete': 使用完全图生成网络；
        - 'Random': 使用随机图生成网络；
        - 'Community Structure': 使用社区结构生成网络；
        - 'Small World': 使用小世界网络生成网络；
        - 'Scale Free': 使用无标度网络生成网络；
        - 'Hierarchical': 使用分层网络生成网络；
        - 'Regular': 使用规则网络生成网络；
        - 'Grid': 使用网格网络生成网络；
        - 'Scale Free': 使用无标度网络生成网络；




    Args:
        nodes_pos (np.array): 节点坐标
        set_num_edges (int): 设置边数量
        num_edges_per_node (int): 每个节点的边数量
        num_neighbors (int): 邻居节点数量

    Returns:
        edges (np.array): 边

    """
    # TODO 调用不同的网络生成机制

    return nodes, edges, infos
    pass  # function


## #NOTE 使用普通的邻居节点生成网络

def generate_neighbors_network(nodes_pos, num_edges_per_node, num_neighbors):
    """
    生成图网络。

    这个方法的步骤是：
    1. 获取节点之坐标；
    2. 计算节点之间的距离；
    3. 选择邻居节点；
    4. 生成边；

    Args:
        nodes_pos (np.array): 节点坐标
        set_num_edges (int): 设置边数量
        num_edges_per_node (int): 每个节点的边数量
        num_neighbors (int): 邻居节点数量

    Returns:
        edges (np.array): 边

    """
    distance_matrix = _calculate_distance_matrix(nodes_pos)  # 计算节点之间的距离
    neighbors = _select_neighbors(distance_matrix, len(nodes_pos), num_neighbors)  # 选择邻居节点
    edges = _create_edges(nodes_pos, neighbors, num_edges_per_node)  # 生成边

    return edges
    pass  # function


# @njit
def _calculate_distance_matrix(nodes):
    """
    计算节点之间的距离矩阵

    Args:
        nodes (np.array): 节点坐标

    Returns:
        np.array: 距离矩阵

    """
    num_nodes = nodes.shape[0]
    distance_matrix = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            distance_matrix[i, j] = np.linalg.norm(nodes[i] - nodes[j])
            distance_matrix[j, i] = distance_matrix[i, j]  # 对称矩阵
    return distance_matrix
    pass  # function


# @njit
def _select_neighbors(distance_matrix, num_nodes, num_neighbors):
    """
    根据节点之间的距离选择邻居节点

    Args:
        distance_matrix (np.array): 距离矩阵
        num_nodes (int): 节点数量
        num_neighbors (int): 邻居节点数量

    Returns:
        neighbors: list, 邻居节点索引
    """
    neighbors = []
    for i in range(num_nodes):
        sorted_indices = np.argsort(distance_matrix[i])
        neighbors.append(sorted_indices[1:num_neighbors + 1])  # 排除自己，选择距离最近的 num_neighbors 个节点
    return neighbors
    pass  # function


# 根据邻居节点生成边


# @njit
def _create_edges(nodes, neighbors, num_edges):
    num_nodes = nodes.shape[0]
    edges = []
    for i in range(num_nodes):
        for _ in range(num_edges):
            neighbor_index = np.random.choice(neighbors[i])
            edges.append((i, neighbor_index))
    return np.array(edges)
    pass  # function


@njit
def _calculate_weighted_distances(nodes_pos, weights):
    """
    计算节点之间的加权距离。

    Args:
        nodes_pos (np.array): 节点坐标
        weights (np.array): 权重

    Returns:
        np.array: 加权距离矩阵
    """
    num_nodes = nodes_pos.shape[0]
    weighted_distances = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            distance = np.linalg.norm(nodes_pos[i] - nodes_pos[j])
            weighted_distance = distance / weights[i]
            weighted_distances[i, j] = weighted_distance
            weighted_distances[j, i] = weighted_distance  # 对称矩阵
    return weighted_distances
    pass  # function


## #NOTE 使用 Voronoi 图生成网络

def _generate_weighted_voronoi_network(nodes_pos: np.array, weights: np.array = None):
    """
    生成加权的 Voronoi 图网络。#TODO 现在生成的仅仅是非加权的 Voronoi 图。后续再增加加权功能

    Args:
        nodes_pos (np.array): 节点坐标
        weights (np.array): 权重

    Returns:
        edges (np.array): 边
        vor (Voronoi): Voronoi 图

    """
    # 默认加权都是 1
    if weights is None:
        weights = np.ones(nodes_pos.shape[0])

    vor = Voronoi(nodes_pos)

    # #DEBUG Plot Voronoi diagram
    fig, ax = plt.subplots()
    voronoi_plot_2d(vor, ax=ax)

    # Colorize Voronoi cells according to weights
    for region, weight in zip(vor.regions, weights):
        if not -1 in region:
            polygon = [vor.vertices[i] for i in region]
            ax.fill(*zip(*polygon), color=plt.cm.viridis(weight))

    plt.show()

    # 根据 vor 图将节点连接起来
    edges = vor.ridge_points

    return edges, vor
    pass  # function
