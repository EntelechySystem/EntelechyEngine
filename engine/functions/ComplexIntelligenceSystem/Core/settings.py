"""
模型通用设置
"""
from dataclasses import dataclass


@dataclass
class Settings():
    """
    模型通用设置

    Returns:

    """

    # 用于让人类写入的，编码的单元类型（键是文本标记值，值是编号标记值）
    dict_written_type_of_Units = {
        'container': 0,  # 容器类型
        'goal': 1,  # 目标类型
        'control': 2,  # 控制类型
        'task': 3,  # 任务类型
        'state': 4,  # 状态类型
        'sensor': 5,  # 感知类型
        'question': 6,  # 问题类型
        'language': 7,  # 语言类型
        'conception': 8,  # 概念类型
        'neuron': 9,  # 神经元类型
    }

    # 用于让人类读取的，解码的单元类型字典（键是编号标记值，值是文本标记值）。注意，该字典与 dict_written_type_of_Units 是反向的。
    dict_decode_type_of_Units_reverse = {v: k for k, v in dict_written_type_of_Units.items()}

    pass  # class
