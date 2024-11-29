"""
常用工具
"""
import logging

import numpy as np
import uuid
import base64
import torch


class Tools:
    @staticmethod
    def generate_unique_identifier(length=32):
        """
        随机生成一个指定位数的英文大小写字母、阿拉伯数字、下划线、横杠符共 64 种符号混合的 uuid 字符串。默认长度为 32 位。

        注意，区分大小写。

        Args:
            length (int): 字符串长度。默认值为 8。

        Returns:
            str: id字符串
        """

        return base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').rstrip('=')[:length]
        pass  # function

    @classmethod
    def encode_string_array(cls, strings, max_len=128):
        """
        将字符串数组编码为一个 tensor，每个字符串转换为 ASCII 数值表示

        Args:
            strings (List[str]): 字符串数组
            max_len (int): 每个字符串的最大长度。默认值为 128。如果字符串长度小于 max_len，则用空格填充

        Returns:

        """
        # 创建一个 tensor，存储字符串的 ASCII 数值表示，空位用 ASCII 码 32 (空格) 填充
        encoded_array = np.full(max_len, 32, dtype=np.int32)

        for i, s in enumerate(strings):
            # 将每个字符串的前 max_len 个字符转换为 ASCII 值
            # ascii_values = [ord(c) for c in s[:max_len]]
            # encoded_array[i, :len(ascii_values)] = ascii_values
            ascii_values = ord(s[:max_len])
            encoded_array[i] = ascii_values

        # 转换为 PyTorch tensor
        return torch.tensor(encoded_array, dtype=torch.int32)

    # # 示例
    # strings = ['unit1', 'unit2', 'unit_longer_name']
    # max_len = 10
    # encoded_tensor = encode_string_array(strings, max_len)
    # print(encoded_tensor)

    @classmethod
    def decode_string_array(cls, encoded_tensor):
        """
        将存储字符串的 tensor 解码为字符串数组

        Args:
            encoded_tensor (torch.Tensor): 存储字符串的 tensor

        Returns:
            List[str]: 字符串数组
        """
        decoded_strings = []

        # 遍历 tensor，逐个元素转换回字符串
        for row in encoded_tensor:
            chars = chr(row.item())  # 32 是空格的 ASCII
            decoded_strings.append(''.join(chars))

        return ''.join(decoded_strings)

    # # 示例解码
    # decoded_strings = decode_string_array(encoded_tensor)
    # print(decoded_strings)

    @classmethod
    def print_units_values(cls, units, is_decode=False):
        """
        打印各单位值

        Returns:

        """
        for field_name, field_value in units.__dict__.items():
            if is_decode and field_name in ['units_name', 'units_type']:
                decoded_values = [cls.decode_string_array(v) for v in field_value]
                logging.info(f'{field_name}:{decoded_values}')
            else:
                logging.info(f'{field_name}:{field_value}')
                pass  # if
            pass  # for

        pass  # function


if __name__ == '__main__':
    # 生成一个随机的字符串
    new_identifier = Tools.generate_unique_identifier()
    print(f'\n{new_identifier}')
    # 编码字符串数组
    encoded_array = Tools.encode_string_array(new_identifier)
    print(encoded_array)
    # 解码字符串数组
    decoded_strings = Tools.decode_string_array(encoded_array)
    print(decoded_strings)
    pass  # function
