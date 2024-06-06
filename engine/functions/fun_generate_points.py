"""
函数：生成散点分布
"""

import logging
from engine.externals import np, njit, Optional
from engine.tools.AlgorithmTools import kmeans_numba


def generate_points(set_densityDistance: float = None, set_numPoints: int = None, set_circleRadius: float = None, circle_origin: np.array = np.array([0, 0]), num_samples=30, distribution='Normal', algorithm: Optional[str] = None, sigma: float = 1):
    """
    根据一系列初始条件与给定分布生成符合要求的散点。

    这里估算的过程中，采用了正方形、立方体作为中间计算量，然后转换为同面积、同体积的圆形、球体。

    散点分布类型：
    - 'Posssion Disk': 生成符合 Poisson Disk 分布的散点。这种分布的特点是，散点之间的距离大致相等，且散点之间的距离大于给定的最小距离。
    - 'Uniform': 生成符合均匀分布的散点。这种分布的特点是，散点之间的距离大致相等，但散点之间的距离不一定大于给定的最小距离。
    - 'Normal': 生成符合正态分布的散点。这种分布的特点是，散点之间的距离大致符合正态分布，但散点之间的距离不一定大于给定的最小距离。

    散点分布相关的算法类型：
    - 'Bridson': 采用 Bridson 算法生成符合 Poisson Disk 分布的散点。该算法的特点是生成的散点距离一定满足不小于最小距离，但是生成的散点数量不一定等于给定的数量；
    - 'cKDTree': 采用 cKDTree 算法生成符合 Poisson Disk 分布的散点。该算法的特点是生成的散点距离一定满足不小于最小距离，但是生成的散点数量不一定等于给定的数量；#BUG 这个还没有适配生成圆形边界的情况。因此不要使用！
    - 'K-means': 采用 K-means 算法生成符合接近 Poisson Disk 分布的散点。该算法的特点是能够生成精确数量的散点，并且生成性能较高；
    - 'annealing': 采用退火算法生成符合 Poisson Disk 分布的散点。该算法的特点是能够生成精确数量的散点，但是生成性能较差； #BUG 还没有测试。因此不要使用！

    Args:
        set_densityDistance: float, 密度距离
        set_numPoints: int, 散点之总数。注意实际生成的数量大约在这个值附近，不会完全等于这个值。
        set_circleRadius: float, 范围半径
        circle_origin: np.array, 圆心坐标
        num_samples: int, 算法每次迭代生成的散点数量
        distribution: str, 期望的散点分布类型
        algorithm: str, 生成散点分布之算法
        sigma: float, 正态分布的标准差


    Returns:
        np.array: 生成的散点

    """
    # 根据给定参数计算其余参数
    # 判断生成的空间维度
    if circle_origin.shape[0] == 2:
        dim = 2
    elif circle_origin.shape[0] == 3:
        dim = 3
    elif circle_origin.shape[0] == 1:
        dim = 1
    else:
        raise ValueError("The dimension of the circle origin must be either 1, 2 or 3.")
    if set_densityDistance is not None and set_numPoints is not None and set_circleRadius is None:  # 如果指定了密度距离、总数，估算范围半径
        if dim == 2:
            a = set_densityDistance * np.sqrt(set_numPoints)
            circle_radius = a / np.sqrt(np.pi)
        elif dim == 3:
            a = set_densityDistance ** 3 * set_numPoints
            circle_radius = a / (4 / 3 * np.pi) ** (1 / 3)
        elif dim == 1:
            circle_radius = set_numPoints * set_densityDistance
            pass  # if
        density_distance = set_densityDistance
        num_points = set_numPoints
    elif set_densityDistance is not None and set_circleRadius is not None and set_numPoints is None:  # 如果指定了密度距离、范围半径，估算总数
        if dim == 2:
            a = set_circleRadius * np.sqrt(np.pi)
            num_points = a / set_densityDistance
        if dim == 3:
            a = set_circleRadius * (4 / 3 * np.pi) ** (1 / 3)
            num_points = a / set_densityDistance
        if dim == 1:
            num_points = set_circleRadius / set_densityDistance
            pass  # if
        density_distance = set_densityDistance
        circle_radius = set_circleRadius
    elif set_numPoints is not None and set_circleRadius is not None and set_densityDistance is None:  # 如果指定了总数、范围半径，估算密度距离
        if dim == 2:
            a = set_circleRadius * np.sqrt(np.pi)
            density_distance = a / set_numPoints
        if dim == 3:
            a = set_circleRadius * (4 / 3 * np.pi) ** (1 / 3)
            density_distance = a / set_numPoints
        if dim == 1:
            density_distance = set_circleRadius / set_numPoints
            pass  # if
        num_points = set_numPoints
        circle_radius = set_circleRadius
    else:
        raise ValueError("Two out of the three parameters (density, total, area) must be provided.")

    logging.info(f"dim: {dim}, density_distance: {density_distance}, num_points: {num_points}, circle_radius: {circle_radius}, circle_origin: {circle_origin}")

    # 生成散点
    if distribution == 'Normal':
        return _generate_points_used_Normal_random_distribution(circle_origin, circle_radius, num_points, sigma)  # DEBUG
    elif distribution == 'Uniform':
        return _generate_points_used_Uniform_random_distribution(circle_origin, circle_radius, num_points)  # DEBUG
    elif distribution == 'Posssion Disk' and algorithm is None:
        if set_numPoints is not None:
            algorithm = 'K-means'
            return _generate_points_used_PoissonDisk_random_distribution_by_Kmeans_algorithm(circle_origin, circle_radius, num_points)
        if set_densityDistance is not None and set_numPoints is not None and set_circleRadius is None:
            algorithm = 'Bridson'
            return _generate_points_used_PoissonDisk_random_distribution_by_Bridson_algorithm(circle_origin, circle_radius, density_distance, num_samples)
        pass  # if

    pass  # function


## #NOTE 生成符合正态分布的散点
@njit
def _generate_points_used_Normal_random_distribution(circle_origin: np.array, circle_radius: float, num_points: int, sigma: float = 1):
    """
    生成符合正态分布的散点。这里采用了简单的方法，即在圆内随机生成一定数量的点。

    Args:
        circle_origin: np.array, 圆心坐标
        circle_radius: float, 圆的半径
        num_points: int, 生成的点的数量
        sigma: float, 正态分布的标准差

    Returns:
        np.array: 生成的散点

    """
    points = np.empty((num_points, 2))
    for i in range(num_points):
        theta = np.random.uniform(0, 2 * np.pi)
        r = np.sqrt(np.random.uniform(0, sigma)) * circle_radius
        points[i] = [r * np.cos(theta) + circle_origin[0], r * np.sin(theta) + circle_origin[1]]
        pass  # for
    return points
    pass  # function


## #NOTE 生成符合随机分布的散点
@njit
def _generate_points_used_Uniform_random_distribution(circle_origin: np.array, circle_radius: float, num_points: int):
    """
    生成符合均匀分布的散点。这里采用了简单的方法，即在圆内随机生成一定数量的点。

    Args:
        circle_origin: np.array, 圆心坐标
        circle_radius: float, 圆的半径
        num_points: int, 生成的点的数量

    Returns:
        np.array: 生成的散点

    """
    points = np.empty((num_points, 2))
    for i in range(num_points):
        theta = np.random.uniform(0, 2 * np.pi)
        r = np.sqrt(np.random.uniform(0, 1)) * circle_radius
        points[i] = [r * np.cos(theta) + circle_origin[0], r * np.sin(theta) + circle_origin[1]]
        pass  # for
    return points
    pass  # function


## #NOTE 采用 Bridson 算法生成符合 Poisson Disk 分布的散点

@njit(parallel=True)
def _generate_points_used_PoissonDisk_random_distribution_by_Bridson_algorithm(origin, radius, min_distance, num_samples=15):
    """
    生成符合 Poisson Disk 分布的散点，这些散点分布在一个圆形区域内。这里采用了著名的 Bridson 算法。该算法的主要步骤是：
    1. 初始化一个网格，网格的大小由输入的半径和最小距离决定。
    2. 随机生成一个初始点，将其添加到网格和活动列表中。
    3. 在活动列表不为空的情况下，随机选择一个点，然后生成一定数量的新点。
    4. 对于每个新生成的点，检查其是否有效（即是否在圆内，与其他点的距离是否大于最小距离）。如果有效，将其添加到网格和活动列表中。
    5. 删除当前选择的点。
    6. 重复步骤 3-5，直到活动列表为空。
    7. 返回生成的点。

    Args:
        origin: np.array, 圆心坐标
        radius: float, 圆的半径
        min_distance: float, 最小距离
        num_samples: int, 每次生成的散点数量

    Returns:
        np.array: 生成的散点
    """

    cell_size = min_distance / np.sqrt(2)
    grid_radius = int(radius / cell_size) + 1
    grid = np.full((2 * grid_radius, 2 * grid_radius), -1)
    active_list = []

    # Initialize a large numpy array to store samples
    samples = np.empty((4 * radius * radius, 2))
    sample_count = 0

    first_sample = np.array([np.random.uniform(-radius, radius), np.random.uniform(-radius, radius)])
    while np.linalg.norm(first_sample - origin) > radius:
        first_sample = np.array([np.random.uniform(-radius, radius), np.random.uniform(-radius, radius)])

    samples[sample_count] = first_sample
    sample_count += 1
    grid_index = (int((first_sample[0] + radius) / cell_size), int((first_sample[1] + radius) / cell_size))
    grid[grid_index] = 0
    active_list.append(grid_index)

    while active_list:
        current_index = np.random.choice(len(active_list))
        current_cell = active_list[current_index]

        for _ in range(num_samples):
            new_sample = _generate_random_point_around_by_Bridson_algorithm(samples[grid[current_cell]], min_distance)
            if np.linalg.norm(new_sample - origin) <= radius and _is_valid_sample_by_Bridson_algorithm(new_sample, origin, radius, min_distance, samples[:sample_count], grid, cell_size):
                samples[sample_count] = new_sample
                sample_count += 1
                new_index = (int((new_sample[0] + radius) / cell_size), int((new_sample[1] + radius) / cell_size))
                grid[new_index] = sample_count - 1
                active_list.append(new_index)

        del active_list[current_index]

    return samples[:sample_count]
    pass  # function


@njit
def _generate_random_point_around_by_Bridson_algorithm(point, min_distance):
    """
    生成一个距离 point 一定距离的随机点。生成一个距离给定点一定距离的随机点。首先生成一个在最小距离和两倍最小距离之间的随机半径，然后生成一个在0和2π之间的随机角度，最后根据半径和角度计算新点的坐标。

    Args:
        point: np.array, 中心点
        min_distance: float, 最小距离

    Returns:
        np.array: 生成的随机点
    """
    r = np.random.uniform(min_distance, 2 * min_distance)
    theta = np.random.uniform(0, 2 * np.pi)
    x = point[0] + r * np.cos(theta)
    y = point[1] + r * np.sin(theta)
    return np.array([x, y])
    pass  # function


@njit
def _is_valid_sample_by_Bridson_algorithm(sample, origin, radius, min_distance, samples, grid, cell_size):
    """
    判断生成的散点是否有效。散点必须满足以下条件：
    1. 位于空间内
    2. 与其他散点的距离大于 min_distance
    3. 与邻居散点的距离大于 min_distance

    Args:
        sample: np.array, 生成的散点
        origin: np.array, 圆心坐标
        radius: float, 圆的半径
        min_distance: float, 最小距离
        samples: np.array, 已生成的散点
        grid: np.array, 网格
        cell_size: float, 网格的大小

    Returns:
        bool: 是否有效
    """
    if np.linalg.norm(sample - origin) > radius:
        return False
    grid_index = (int((sample[0] + radius) / cell_size), int((sample[1] + radius) / cell_size))
    if grid_index[0] < 0 or grid_index[0] >= grid.shape[0] or grid_index[1] < 0 or grid_index[1] >= grid.shape[1]:
        return False
    if grid[grid_index] != -1:
        return False
    for neighbor_index in _get_neighbor_indices(grid_index, grid.shape):
        if grid_index[0] >= 0 and grid_index[0] < grid.shape[0] and \
                grid_index[1] >= 0 and grid_index[1] < grid.shape[1] and \
                grid[neighbor_index] != -1:
            neighbor_sample = samples[grid[neighbor_index]]
            if np.linalg.norm(sample - neighbor_sample) < min_distance:
                return False
    return True


@njit
def _get_neighbor_indices(index, grid_shape):
    """
    获取邻居散点的索引
    """
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbor_index = (index[0] + i, index[1] + j)
            if (0 <= neighbor_index[0] < grid_shape[0]) and (0 <= neighbor_index[1] < grid_shape[1]):
                neighbors.append(neighbor_index)
    return neighbors
    pass  # function


## #NOTE 采用 K-means 算法生成符合 Poisson Disk 分布的散点
def _generate_points_used_PoissonDisk_random_distribution_by_Kmeans_algorithm(circle_origin, circle_radius, num_points):
    """
    生成符合接近 Poisson Disk 分布的散点。这里采用了 K-means 算法。该算法的主要思想是：
    1. 在指定的圆内随机生成大量的点。
    2. 使用 K-means 算法将这些点聚类到指定数量的簇中。
    3. 返回每个簇的质心作为最终的散点。

    Args:
        num_points: int, 目标生成的总点数
        circle_origin: np.array, 圆心坐标
        circle_radius: float, 圆的半径
        num_initial_points: int, 初始生成的点的数量

    Returns:
        np.array: 生成的散点
    """

    # 首先在指定的圆内随机生成大量的点
    num_initial_points = num_points * 20
    initial_points = np.empty((num_initial_points, 2))
    for i in range(num_initial_points):
        theta = np.random.uniform(0, 2 * np.pi)
        r = np.sqrt(np.random.uniform(0, 1)) * circle_radius
        initial_points[i] = [r * np.cos(theta) + circle_origin[0], r * np.sin(theta) + circle_origin[1]]

    # 使用 K-means 算法将这些点聚类到指定数量的簇中
    centroids = kmeans_numba(initial_points, num_points)

    # 返回每个簇的质心作为最终的散点
    return centroids
    pass  # function


## #NOTE 采用退火算法生成符合 Poisson Disk 分布的散点


# def _generate_points_used_PoissonDisk_random_distribution_by_annealing_algorithm(circle_origin, circle_radius, density_distance, num_samples):
def _generate_points_used_PoissonDisk_random_distribution_by_annealing_algorithm(origin, radius, target_num_points, iterations=10, initial_temperature=1.0, cooling_rate=0.99):
    """
    Args:
        origin: np.array, 圆心坐标
        radius: float, 圆的半径
        target_num_points: int, 目标生成的总点数
        iterations: int, 模拟退火的迭代次数
        initial_temperature: float, 初始温度
        cooling_rate: float, 冷却率

    Returns:
        np.array: 生成的节点
    """

    # 首先在圆内随机生成指定数量的点
    points = np.empty((target_num_points, 2))
    for i in range(target_num_points):
        theta = np.random.uniform(0, 2 * np.pi)
        r = radius * np.sqrt(np.random.uniform(0, 1))
        points[i] = [r * np.cos(theta) + origin[0], r * np.sin(theta) + origin[1]]

    # 定义能量函数，这里我们简单地使用所有点之间的距离的总和
    def energy(points):
        return np.sum(np.linalg.norm(points[np.newaxis, :] - points[:, np.newaxis], axis=-1))

    # 模拟退火过程
    temperature = initial_temperature
    current_energy = energy(points)
    for _ in range(iterations):
        # 随机选择一个点和一个新的位置
        point_index = np.random.randint(target_num_points)
        new_point = np.copy(points[point_index])
        theta = np.random.uniform(0, 2 * np.pi)
        r = radius * np.sqrt(np.random.uniform(0, 1))
        new_point[0] = r * np.cos(theta) + origin[0]
        new_point[1] = r * np.sin(theta) + origin[1]

        # 计算新的能量
        new_points = np.copy(points)
        new_points[point_index] = new_point
        new_energy = energy(new_points)

        # 如果新的能量更低，或者满足模拟退火的接受准则，则接受新的位置
        if new_energy < current_energy or np.random.uniform(0, 1) < np.exp((current_energy - new_energy) / temperature):
            points = new_points
            current_energy = new_energy

        # 降低温度
        temperature *= cooling_rate

    return points

    pass  # function


## #NOTE 以下采用 cKDTree 算法生成符合 Poisson Disk 分布的散点

# @njit(parallel=True)
def _generate_points_used_PoissonDisk_random_distribution_by_cKDTree_algorithm(width, height, min_distance, num_samples=30):
    """
    生成符合 Poisson Disk 分布的散点。这里采用了 cKDTree 算法。该算法的主要思想是：
    1. 生成一个网格，将整个空间划分为若干个小格子，每个格子的边长为 min_distance / sqrt(2)。
    2. 从初始散点开始，生成一个散点，将其放入网格中，并将其加入活动列表中。
    3. 从活动列表中随机选择一个散点，生成若干个新散点，将其放入网格中，并将其加入活动列表中。
    4. 重复步骤 3，直到活动列表为空。

    Args:
        width: int, 空间宽度
        height: int, 空间高度
        min_distance: float, 最小距离
        num_samples: int, 每次生成的散点数量


    Returns:
        np.array: 生成的散点
    """
    cell_size = min_distance / np.sqrt(2)
    grid_width = int(width / cell_size) + 1
    grid_height = int(height / cell_size) + 1
    grid = np.full((grid_width, grid_height), -1)
    active_list = []
    samples = []

    first_sample = np.array([np.random.uniform(0, width), np.random.uniform(0, height)])
    samples.append(first_sample)
    grid_index = (int(first_sample[0] / cell_size), int(first_sample[1] / cell_size))
    grid[grid_index] = 0
    active_list.append(grid_index)

    tree = cKDTree(samples)

    while active_list:
        current_index = np.random.choice(len(active_list))
        current_cell = active_list[current_index]

        for _ in range(num_samples):
            new_sample = _generate_random_point_around_by_cKDTree_algorithm(samples[grid[current_cell]], min_distance)
            if _is_valid_sample_by_cKDTree_algorithm(new_sample, width, height, min_distance, samples, grid, cell_size, tree):
                samples.append(new_sample)
                new_index = (int(new_sample[0] / cell_size), int(new_sample[1] / cell_size))
                grid[new_index] = len(samples) - 1
                active_list.append(new_index)
                tree = cKDTree(samples)

        del active_list[current_index]

    return np.array(samples)


# @njit
def _generate_random_point_around_by_cKDTree_algorithm(point, min_distance):
    """
    生成一个距离 point 一定距离的随机点

    Args:
        point: np.array, 中心点
        min_distance: float, 最小距禽

    Returns:
        np.array: 生成的随机点
    """
    r = np.random.uniform(min_distance, 2 * min_distance)
    theta = np.random.uniform(0, 2 * np.pi)
    x = point[0] + r * np.cos(theta)
    y = point[1] + r * np.sin(theta)
    return np.array([x, y])


# @njit
def _is_valid_sample_by_cKDTree_algorithm(sample, width, height, min_distance, samples, grid, cell_size, tree):
    """
    判断生成的散点是否有效。散点必须满足以下条件：
    1. 位于空间内
    2. 与其他散点的距离大于 min_distance
    3. 与邻居散点的距离大于 min_distance

    Args:
        sample: np.array, 生成的散点
        width: int, 空间宽度
        height: int, 空间高度
        min_distance: float, 最小距离
        samples: np.array, 已生成的散点
        grid: np.array, 网格
        cell_size: float, 网格的大小
        tree: cKDTree, KD树

    Returns:
        bool: 是否有效
    """
    if sample[0] < 0 or sample[0] >= width or sample[1] < 0 or sample[1] >= height:
        return False
    grid_index = (int(sample[0] / cell_size), int(sample[1] / cell_size))
    if grid_index[0] < 0 or grid_index[0] >= grid.shape[0] or grid_index[1] < 0 or grid_index[1] >= grid.shape[1]:
        return False
    if grid[grid_index] != -1:
        return False
    distances, indices = tree.query(sample, k=1)
    if distances < min_distance:
        return False
    return True
