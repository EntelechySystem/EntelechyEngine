"""
实体命令。包括：
    - add_syms: 给指定的查询添加指定的信号
"""

import numpy as np
# import torch

from engine.libraries.models.model import Model

class Commands:
    # @njit
    def add_unit(units, uid: np.uint64):
        """
        添加一个单元
        Args:
            units (np.ndarray): 单元众
            uid (np.uint64): 单元之 ID
        """
        units_dtype = units.dtype
        new_unit = np.zeros(1, dtype=units_dtype)
        new_unit['uid'] = uid
        return np.concatenate((units, new_unit))
        pass  # function

    # @njit
    def delete_unit(units, uid: np.uint64):
        """
        删除一个单元

        Args:
            units (np.ndarray): 单元众
            uid (np.uint64): 单元之 ID

        Returns:

        """
        return np.delete(units, uid)
        pass  # function

    # @njit
    def query_unit(units, uid):
        """
        查找一个单元

        Args:
            units (np.ndarray): 单元众
            uid (np.uint64): 单元之 ID

        Returns:

        """
        return np.where(units['uid'] == uid)[0]
        pass  # function

    # @njit
    def move_uint(uid, pos_x, pos_y, pos_z, input_units, output_units, dx, dy, dz):
        """
        根据递增量更新一个单元之位置

        Args:
            uid ():
            pos_x ():
            pos_y ():
            pos_z ():
            input_units ():
            output_units ():
            dx ():
            dy ():
            dz ():

        Returns:

        """
        pos_x += dx
        pos_y += dy
        pos_z += dz

    def step_units(units, uids):
        """
        步进运行指定的单元

        Args:
            units (np.ndarray): 单元众
            uids (np.ndarray): 单元 ID 众

        Returns:

        """



        pass  # function


    pass  # class
