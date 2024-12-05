"""
@Desc   :  矩阵数据结构互换工具
"""

import numpy as np
from scipy.sparse import coo_matrix


def linksConnectionMatrix_to_denseMatrix_numpy(connections, N):
    """
    将连接接口矩阵转换为传统稠密邻接矩阵。

    Args:
        connections (numpy.ndarray): 连接接口矩阵 N × M
        N (int): agent 的总数

    Returns:
        numpy.ndarray: 稠密邻接矩阵 (N × N)
    """
    denseMatrix_matrix = np.zeros((N, N), dtype=int)  # 初始化稠密矩阵
    for i, row in enumerate(connections):
        for target in row:
            if target != -1:  # 忽略未连接的部分
                denseMatrix_matrix[i, target] = 1
    return denseMatrix_matrix


def denseMatrix_to_linksConnectionMatrix_numpy(denseMatrix_matrix, M):
    """
    将传统稠密邻接矩阵转换为连接接口矩阵。

    Args:
        denseMatrix_matrix (numpy.ndarray): 稠密邻接矩阵 (N × N)
        M (int): 每个 agent 的最大连接数

    Returns:
        numpy.ndarray: 连接接口矩阵 N × M

    Raises:
        ValueError: 如果 agent 的连接数超过了方法 2 矩阵的最大连接数 M
    """
    N = denseMatrix_matrix.shape[0]
    connections = np.full((N, M), -1, dtype=int)  # 初始化连接接口矩阵
    for i in range(N):
        targets = np.where(denseMatrix_matrix[i] > 0)[0]  # 获取第 i 行中所有连接的目标
        if len(targets) > M:
            raise ValueError(f"Agent {i} 的连接数超过了方法 2 矩阵的最大连接数 M={M}")
        connections[i, :len(targets)] = targets
    return connections


def linksConnectionMatrix_to_sparseMatrix_numpy(connections, N):
    """
    将连接接口矩阵转换为稀疏矩阵 (COO 格式)。

    Args:
        connections (numpy.ndarray): 连接接口矩阵 N × M
        N (int): agent 的总数

    Returns:
        scipy.sparse.coo_matrix: 稀疏矩阵 (COO 格式)
    """
    rows, cols = [], []
    for i, row in enumerate(connections):
        for target in row:
            if target != -1:  # 忽略未连接的部分
                rows.append(i)
                cols.append(target)
    return coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N))


def sparseMatrix_to_linksConnectionMatrix_numpy(sparseMatrix_matrix, M):
    """
    将稀疏矩阵 (COO 格式) 转换为连接接口矩阵。

    Args:
        sparseMatrix_matrix (scipy.sparse.coo_matrix): 稀疏矩阵 (COO 格式)
        M (int): 每个 agent 的最大连接数

    Returns:
        numpy.ndarray: 连接接口矩阵 N × M

    Raises:
        ValueError: 如果 agent 的连接数超过了方法 2 矩阵的最大连接数 M
    """
    connections = np.full((sparseMatrix_matrix.shape[0], M), -1, dtype=int)  # 初始化连接接口矩阵
    row, col = sparseMatrix_matrix.nonzero()  # 获取所有非零元素的行列索引
    for i, target in zip(row, col):
        for k in range(M):
            if connections[i, k] == -1:  # 找到第一个空位
                connections[i, k] = target
                break
        else:
            raise ValueError(f"Agent {i} 的连接数超过了方法 2 矩阵的最大连接数 M={M}")
    return connections


import torch


def linksConnectionMatrix_to_denseMatrix(connections, N):
    """
    将连接接口矩阵转换为稠密邻接矩阵。

    Args:
        connections (torch.Tensor): 连接接口矩阵 的 N × M 矩阵
        N (int): agent 总数

    Returns:
        torch.Tensor: 稠密邻接矩阵 (N × N)
    """
    dense_matrix = torch.zeros((N, N), dtype=torch.float32)
    for i in range(connections.size(0)):  # 遍历每个 agent
        for target in connections[i]:
            if target != -1:  # 忽略未连接部分
                dense_matrix[i, target] = 1
    return dense_matrix


def denseMatrixto_linksConnectionMatrix(dense_matrix, M):
    """
    将稠密邻接矩阵转换为连接接口矩阵。

    Args:
        dense_matrix (torch.Tensor): 稠密邻接矩阵 (N × N)
        M (int): 每个 agent 的最大连接数

    Returns:
        torch.Tensor: 连接接口矩阵 的 N × M 矩阵

    Raises:
        ValueError: 如果 agent 的连接数超过了 M
    """
    N = dense_matrix.size(0)
    connections = torch.full((N, M), -1, dtype=torch.int64)  # 初始化连接接口矩阵
    for i in range(N):
        targets = torch.nonzero(dense_matrix[i] > 0).squeeze(1)  # 获取连接的目标
        if len(targets) > M:
            raise ValueError(f"Agent {i} 的连接数超过了 M={M}")
        connections[i, :len(targets)] = targets
    return connections


def linksConnectionMatrix_to_sparseMatrix(connections):
    """
    将连接接口矩阵转换为 PyG 的 edge_index 和 edge_weight。

    Args:
        connections (torch.Tensor): 连接接口矩阵 的 N × M 矩阵

    Returns:
        torch.Tensor: edge_index (2 × num_edges)
        torch.Tensor: edge_weight (num_edges)
    """
    rows, cols = [], []
    for i in range(connections.size(0)):
        for target in connections[i]:
            if target != -1:
                rows.append(i)
                cols.append(target)
    edge_index = torch.tensor([rows, cols], dtype=torch.int64)
    edge_weight = torch.ones(len(rows), dtype=torch.float32)  # 默认权重为 1
    return edge_index, edge_weight


def sparse_to_linksConnectionMatrix(edge_index, N, M):
    """
    将 PyG 的 edge_index 和 edge_weight 转换为连接接口矩阵。

    Args:
        edge_index (torch.Tensor): 形状为 (2 × num_edges) 的张量
        N (int): agent 总数
        M (int): 每个 agent 的最大连接数

    Returns:
        torch.Tensor: 连接接口矩阵 的 N × M 矩阵

    Raises:
        ValueError: 如果 agent 的连接数超过了 M
    """
    connections = torch.full((N, M), -1, dtype=torch.int64)
    for i, target in zip(edge_index[0], edge_index[1]):
        for k in range(M):
            if connections[i, k] == -1:  # 找到第一个空位
                connections[i, k] = target
                break
        else:
            raise ValueError(f"Agent {i} 的连接数超过了 M={M}")
    return connections
