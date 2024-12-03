"""
定义单元众 Units 及其相关操作
"""
from dataclasses import dataclass

import numpy as np
# from numba import njit

from engine.functions.ComplexIntelligenceSystem.Core.tools import Tools
from engine.functions.ComplexIntelligenceSystem.Core.settings import Settings


# class InitUnits():
#     """
#     定义全局单元众 #HACK 未开发，暂时不使用
#     """
#
#     @classmethod
#     def __init__(cls, init_dict, N_units: int, max_num_links: int, unit_type: int):
#         guid = 0
#         while guid < N_units:
#             pass  # while
#         pass  # function
#
#     pass  # class



import torch

@dataclass
class NeuronsUnits():
    """
    定义神经单元之结构化数组的数据类型。基于 PyTorch 的版本
    """

    gid: torch.Tensor  # 单元之全局 ID（N）
    uid: torch.Tensor  # 单元之 ID（N）
    units_name: torch.Tensor  # 单元之名称（N×K）
    units_type: torch.Tensor  # 单元之类型（N）
    pos_x: torch.Tensor  # 单元之物理空间之 X 坐标
    pos_y: torch.Tensor  # 单元之物理空间之 Y 坐标
    # pos_z: torch.Tensor  # 单元之物理空间之 Z 坐标 #NOTE 如果需要启用再用
    input_units: torch.Tensor  # 单元之输入
    output_units: torch.Tensor  # 单元之输出
    # contents_obj: torch.Tensor  # 单元之内容
    # containers_obj: torch.Tensor  # 单元之容器
    # nodes_obj: torch.Tensor  # 单元之节点
    links: torch.Tensor  # 单元之连接

    def __init__(self, N_units: int, max_N_links: int):
        self.gid = torch.arange(N_units, dtype=torch.int64)
        self.uid = torch.arange(N_units, dtype=torch.int64)
        self.pos_x = torch.zeros(N_units, dtype=torch.float64)
        self.pos_y = torch.zeros(N_units, dtype=torch.float64)
        # self.pos_z = torch.zeros(N_units, dtype=torch.float64)
        self.input_units = torch.empty((N_units), dtype=torch.float32)
        self.output_units = torch.empty((N_units), dtype=torch.float32)
        # self.contents_obj = torch.empty((N_units), dtype=torch.string)
        # self.containers_obj = torch.empty((N_units), dtype=torch.string)
        # self.nodes_obj = torch.empty((N_units), dtype=torch.string)
        self.links = torch.empty((N_units, max_N_links), dtype=torch.int32)
        pass  # function

    pass  # class


@dataclass
class NeuronsUnits_ForHumanRead():
    """
    定义专门用于人类观察可读的神经单元之结构化数组的数据类型。基于 PyTorch 的版本
    """

    gid: torch.Tensor  # 单元之全局 ID（N）
    # uid: torch.uint64  # 单元之 ID（N）
    # units_type: np.dtype['S32']  # 单元之类型（N）
    units_type: torch.uint8  # 单元之类型（N）

    def __init__(self, N_units: int, max_num_links: int):
        """
        初始化可人类观察的神经单元之结构化数组的数据类型

        Args:
            N_units:
            max_num_links:
        """
        self.gid = torch.arange(N_units, dtype=torch.int64)
        # self.uid = torch.arange(N_units, dtype=torch.uint64)
        self.units_name = np.array([Tools.generate_unique_identifier() for i in range(N_units)], np.dtype('S32'))
        self.units_type = torch.from_numpy(np.full(N_units, Settings.dict_written_type_of_Units['neuron']))
        pass  # function

    pass  # class


# import jax.numpy as jnp
#
# @dataclass
# class NeuronsUnits():
#     """
#     定义神经单元之结构化数组的数据类型。基于 JAX 的版本
#     """
#
#     gid: jnp.ndarray  # 单元之全局 ID（N）
#     uid: jnp.ndarray  # 单元之 ID（N）
#     units_name: jnp.ndarray  # 单元之名称（N×K）
#     units_type: jnp.ndarray  # 单元之类型（N）
#     pos_x: jnp.ndarray  # 单元之物理空间之 X 坐标
#     pos_y: jnp.ndarray  # 单元之物理空间之 Y 坐标
#     # pos_z: jnp.ndarray  # 单元之物理空间之 Z 坐标 #NOTE 如果需要启用再用
#     input_units: jnp.ndarray  # 单元之输入
#     output_units: jnp.ndarray  # 单元之输出
#     # contents_obj: jnp.ndarray  # 单元之内容
#     # containers_obj: jnp.ndarray  # 单元之容器
#     # nodes_obj: jnp.ndarray  # 单元之节点
#     links: jnp.ndarray  # 单元之连接
#
#     def __init__(self, N_units: int, max_N_links: int):
#         self.gid = jnp.arange(N_units, dtype=jnp.int64)
#         self.uid = jnp.arange(N_units, dtype=jnp.int64)
#         self.pos_x = jnp.zeros(N_units, dtype=jnp.float64)
#         self.pos_y = jnp.zeros(N_units, dtype=jnp.float64)
#         # self.pos_z = jnp.zeros(N_units, dtype=jnp.float64)
#         self.input_units = jnp.empty((N_units), dtype=jnp.float32)
#         self.output_units = jnp.empty((N_units), dtype=jnp.float32)
#         # self.contents_obj = jnp.empty((N_units), dtype=jnp.string)
#         # self.containers_obj = jnp.empty((N_units), dtype=jnp.string)
#         # self.nodes_obj = jnp.empty((N_units), dtype=jnp.string)
#         self.links = jnp.empty((N_units, max_N_links), dtype=jnp.int32)
#         pass  # function
#
#     pass  # class
#
#
# @dataclass
# class NeuronsUnits_ForHumanRead():
#     """
#     定义专门用于人类观察可读的神经单元之结构化数组的数据类型。基于 JAX 的版本
#     """
#
#     gid: jnp.ndarray  # 单元之全局 ID（N）
#     # uid: jnp.uint64  # 单元之 ID（N）
#     # units_type: np.dtype['S32']  # 单元之类型（N）
#     units_type: jnp.uint8  # 单元之类型（N）
#
#     def __init__(self, N_units: int, max_num_links: int):
#         """
#         初始化可人类观察的神经单元之结构化数组的数据类型
#
#         Args:
#             N_units:
#             max_num_links:
#         """
#         self.gid = jnp.arange(N_units, dtype=jnp.int64)
#         # self.uid = jnp.arange(N_units, dtype=jnp.uint64)
#         self.units_name = np.array([Tools.generate_unique_identifier() for i in range(N_units)], np.dtype('S32'))
#         self.units_type = jnp.array(np.full(N_units, Settings.dict_written_type_of_Units['neuron']), dtype=jnp.uint8)
#         pass  # function
#
#     pass  # class


# @dataclass()
# class OperationUnits(): # HACK 暂时不继续
#     """
#     定义运作单元（机器件）之结构化数组的数据（PyTorch 版本）
#     """
#
#     uid: torch.Tensor  # 运作单元之 ID
#     units_name: torch.Tensor  # 运作单元之名称
#     units_type: torch.Tensor  # 运作单元之类型
#     input_units: torch.Tensor  # 运作单元之输入
#     output_units: torch.Tensor  # 运作单元之输出
#     links: torch.Tensor  # 运作单元之连接（N×M）
#
#     def __init__(self, N_units: torch.int64, max_N_links: torch.int32, unit_type: torch.uint8):
#         self.uid = torch.arange(N_units, dtype=torch.int64)
#         self.units_name = torch.from_numpy(np.array([Tools.generate_unique_identifier() for i in range(N_units)]))
#         self.units_type = torch.from_numpy(np.array(Tools.encode_string_array(unit_type)))
#         self.input_units = torch.empty((N_units), dtype=torch.float32)
#         self.output_units = torch.empty((N_units), dtype=torch.float32)
#         self.links = torch.ones((N_units, max_N_links), dtype=torch.int32) * -1
#         pass  # function
#
#     pass  # class


@dataclass()
class OperationUnits():
    """
    定义运作单元（机器件）之结构化数组的数据（Numpy 版本）

    注意，连接的数据类型为 int32，因为连接的值可能为负数。值为 -1 表示未连接。
    """

    def __init__(self, N_units: np.uint32, max_N_links: np.uint32, unit_type: np.uint8, init_gid: np.uint32):
        self.gid = np.arange(init_gid, init_gid + N_units)  # 单元之全局 ID
        self.uid = np.arange(N_units)  # 单元之 ID
        self.state_on = np.full(N_units, False)  # 运作单元在物理层面上是否被启用，True 表示启用，False 表示未启用
        self.uid_name = np.array([Tools.generate_unique_identifier() for i in range(N_units)])  # 运作单元之名称
        self.units_type = np.full(N_units, unit_type)  # 运作单元之类型
        self.input_units = np.full(N_units, ' ', np.dtype('S128'))  # 运作单元之输入
        self.output_units = np.full(N_units, ' ', np.dtype('S128'))  # 运作单元之输出
        self.links_softs = -np.ones((N_units, max_N_links), np.dtype(np.int32))  # 运作单元之软连接（N×M）
        self.links_id = -np.ones((N_units, max_N_links), np.dtype(np.int32))  # 运作单元之 id 硬连接（N×M）
        self.content = np.full(N_units, ' ', np.dtype('S128'))  # 运作单元之内容

        pass  # function


@dataclass()
class OperationUnitsForHuman():
    """
    定义可用于人类观察可读的运作单元（机器件）之结构化数组的数据（Numpy 版本）

    注意，连接的数据类型为 int32，因为连接的值可能为负数。值为 -1 表示未连接。
    """

    def __init__(self, N_units: np.uint32, max_N_links: np.uint32, unit_type: np.uint8, init_gid: np.uint32):
        self.gid = np.arange(init_gid, init_gid + N_units)  # 单元之全局 ID
        self.explaination = np.full(N_units, ' ', np.dtype('S128'))  # 运作单元之解释
        self.notes = np.full(N_units, ' ', np.dtype('S4096'))  # 运作单元之备注
        pass  # function

    pass  # class


@dataclass()
class KeyData():
    """
    #TODO 定义匹配钥匙对数据结构
    """
    pass  # class
