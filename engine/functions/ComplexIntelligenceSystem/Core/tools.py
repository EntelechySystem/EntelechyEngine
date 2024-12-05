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
    def generate_unique_identifier(length=64):
        """
        随机生成一个指定位数的英文大小写字母、阿拉伯数字、下划线、横杠符共 64 种符号混合的 uuid 字符串。默认长度为 64 位。

        注意，区分大小写。

        Args:
            length (int): 字符串长度。默认值为 64。

        Returns:
            str: id字符串
        """

        return base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').rstrip('=')[:length]
        pass  # function

    @classmethod
    def encode_ascii_string_array_to_pytorch_tensor(cls, strings, max_len=256):
        """
        将 ASCII 字符串数组编码为一个 tensor，每个字符串转换为 ASCII 数值表示

        Args:
            strings (List[str]): 字符串数组
            max_len (int): 每个字符串的最大长度。默认值为 128。如果字符串长度小于 max_len，则用空格填充

        Returns:
            torch.Tensor: 编码后的 tensor

        Examples:
            # 示例
            strings = ['unit1', 'unit2', 'unit_longer_name']
            max_len = 10
            encoded_tensor = encode_ascii_string_array_to_pytorch_tensor(strings, max_len)
            print(encoded_tensor)

        """
        # 创建一个 tensor，存储字符串的 ASCII 数值表示，空位用 ASCII 码 32 (空格) 填充
        encoded_array = np.full(max_len, 32, dtype=np.uint8)

        for i, s in enumerate(strings):
            # 将每个字符串的前 max_len 个字符转换为 ASCII 值
            # ascii_values = [ord(c) for c in s[:max_len]]
            # encoded_array[i, :len(ascii_values)] = ascii_values
            ascii_values = ord(s[:max_len])
            encoded_array[i] = ascii_values

        # 转换为 PyTorch tensor
        return torch.tensor(encoded_array, dtype=torch.uint32)
        pass  # function

    @classmethod
    def decode_pytorch_tensor_to_ascii_string_array(cls, encoded_tensor):
        """
        将存储 ASCII 字符串的 PyTorch 张量解码为 ASCII 字符串数组

        Args:
            encoded_tensor (torch.Tensor): 存储字符串的 tensor

        Returns:
            List[str]: 字符串数组

        Examples:
            # 示例解码
            decoded_strings = decode_pytorch_tensor_to_ascii_string_array(encoded_tensor)
            print(decoded_strings)
        """
        decoded_strings = []

        # 遍历 tensor，逐个元素转换回字符串
        for row in encoded_tensor:
            chars = chr(row.item())  # 32 是空格的 ASCII
            decoded_strings.append(''.join(chars))

        return ''.join(decoded_strings)
        pass  # function

    @classmethod
    def encode_unicode_string_to_pytorch_tensor(cls, s, max_len=256):
        """
        将 Unicode 字符串编码为一个指定长度的 PyTorch 数组

        Args:
            s: 字符串
            max_len: 数组长度

        Returns:
            torch.Tensor: 编码后的数组


        Examples:
            # 示例用法
            s = "你好，世界！"
            length = 32
            fixed_length_array = encode_unicode_string_to_pytorch_tensor(s, length)
            print(fixed_length_array)

        """
        # 将字符串编码为字节数组
        byte_array = np.frombuffer(s.encode('utf-8'), dtype=np.uint8)
        # 创建一个指定长度的数组，填充为0
        fixed_length_array = np.zeros(max_len, dtype=np.uint32)
        # 将字节数组复制到定长数组中
        fixed_length_array[:len(byte_array)] = byte_array
        return torch.from_numpy(fixed_length_array)
        pass  # function

    @classmethod
    def decode_pytorch_tensor_to_unicode_string(cls, array):
        """
        将定长的 PyTorch 张量解码为 Unicode 字符串

        Args:
            array (torch.Tensor): 编码后的数组

        Returns:
            str: 解码后的字符串

        Examples:
            # 示例用法
            encoded_array = Tools.encode_unicode_string_to_pytorch_tensor("你好，世界！", 32)
            decoded_string = Tools.decode_pytorch_tensor_to_unicode_string(encoded_array)
            print(decoded_string)

        """
        # 将 PyTorch 数组转换为 numpy 数组
        byte_array = array.numpy().astype(np.uint8)
        # 找到第一个 0 的位置，表示字符串结束
        end_index = np.where(byte_array == 0)[0]
        if len(end_index) > 0:
            byte_array = byte_array[:end_index[0]]
        # 将字节数组解码为字符串
        return byte_array.tobytes().decode('utf-8')
        pass  # function

    @classmethod
    def print_units_values(cls, units, is_decode=False):
        """
        打印各单位值

        Args:
            units: 单位
            is_decode: 是否解码字符串。默认值为 False

        """
        for field_name, field_value in units.__dict__.items():
            if is_decode and field_name in ['units_name', 'units_type']:
                decoded_values = [cls.decode_pytorch_tensor_to_ascii_string_array(v) for v in field_value]
                logging.info(f'{field_name}:{decoded_values}')
            else:
                logging.info(f'{field_name}:{field_value}')
                pass  # if
            pass  # for

        pass  # function

    pass  # class


if __name__ == '__main__':
    # 生成一个随机的字符串
    new_identifier = Tools.generate_unique_identifier()
    print(f'\n{new_identifier}')
    # 编码字符串数组
    encoded_array = Tools.encode_ascii_string_array_to_pytorch_tensor(new_identifier)
    print(encoded_array)
    # 解码字符串数组
    decoded_strings = Tools.decode_pytorch_tensor_to_ascii_string_array(encoded_array)
    print(decoded_strings)
    # 编码 Unicode 字符串
    encoded_array = Tools.encode_unicode_string_to_pytorch_tensor("你好，世界！")
    print(encoded_array)
    # 解码 Unicode 字符串
    decoded_string = Tools.decode_pytorch_tensor_to_unicode_string(encoded_array)
    print(decoded_string)
    pass  # function
