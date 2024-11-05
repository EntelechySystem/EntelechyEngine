"""
各种处理数据的工具
"""
from engine.tools.Tools import Tools
from engine.externals import re, np, csv, pd, Path, load_workbook, dataclass, ast, builtins


# from engine.Core.Tools.Tools import Tools


@dataclass()
class DataManageTools:
    """
    处理数据的工具
    """

    @classmethod
    def precompile_Excel_to_CSVs_and_PKLs(cls, folderpath_Excel: Path):
        """
        预处理 Excel 原始数据部，转换并导出为 CSV 格式、PKL 格式的数据表，同时返回对应的数据表数据框。

        Args:
            folderpath_Excel (Path): Excel 文件的路径。

        Returns:
            dataframes (dict): 一个 DataFrame 字典，字典的键是文件名的中间部分，字典的值是对应的 DataFrame。

        """
        # from Core.Tools.DataManageTools import DataManageTools
        # %%
        # folderpath_project = Tools.get_project_rootpath()
        # %%
        # 列举指定路径下所有的 Excel 文件
        list_filepath_Excel = [f for f in folderpath_Excel.glob('*.xlsx') if not f.name.startswith("~$")]

        # 依次读取 Excel 文件并转换为 CSV 文件
        for filepath_Excel in list_filepath_Excel:
            cls._convert_excel_sheets_to_csv(filepath_Excel)
            pass

        # %%
        # 预处理文件夹内的每一个原始的前缀名为 'am_' 的 CSV 格式的邻接矩阵数据表，生成对应的带索引的关系型数据表
        cls._preprocess_original_adjacency_matrix_database_to_indexed_relational_table_database(folderpath_Excel)

        # 预处理文件夹内的每一个前缀名为 'rt_' 的 CSV 格式的关系型数据表，生成对应的带索引的关系型数据表
        cls._preprocess_original_relational_table_database_to_indexed_relational_table_database(folderpath_Excel)

        # 预处理文件夹内的每一个前缀名为 'rt_' 的且与前缀名为 'am_' 的 CSV 格式的文件同名的文件，其内容是一个关系型数据表，将其转换为二维矩阵形式，导出为 PKL 格式的文件
        cls._preprocess_indexed_relational_table_database_to_matrix_array(folderpath_Excel)

        # TODO 【主键】、【名键】已经发挥作用。最后，重命名【主键】前缀名为【索引键】，重命名【名键】前缀名为【值键】；

        # 预处理文件夹内的每一个前缀名为 'rt_' 的 CSV 格式的关系型数据表，转换各列数据为相关的数据类型，另外导出为 PKL 格式的文件
        df_settings_data = DataManageTools._preprocess_data_type_of_relational_table_database(folderpath_Excel)

        # df_settings_data = cls._load_CSVs_to_DataFrames(str(Path(str_filepath_Excel).parent))
        return df_settings_data
        pass  # function

    @classmethod
    def _convert_excel_sheets_to_csv(cls, filepath_excel: Path):
        """
        将 Excel 文件中的所有表格转换为 CSV 文件。

        读取 Excel 文件的时候，预处理为不带有任何公式的只包含计算结果的形式。

        Args:
            filepath_excel (str): Excel 文件的路径。

        Returns:

        """
        # filepath_excel = Path(filepath_excel)
        if not filepath_excel.exists():
            raise FileNotFoundError(f"表格 Excel 文件没找到！: {filepath_excel}")

        # Load the workbook and calculate the formulas
        workbook = load_workbook(filename=str(filepath_excel), data_only=True)

        # Iterate through each sheet in the workbook
        for sheet in workbook.sheetnames:
            if sheet.startswith("meta_"):  # 如果表格名的前缀是 'meta_'，那么就是一个给 Excel 表本身作配置的内部的数据表，不需要转换为 CSV 文件
                continue
            csv_file_path = filepath_excel.parent / f"csv_{sheet}.csv"

            with open(csv_file_path, 'w', newline="") as f:
                c = csv.writer(f)
                for r in workbook[sheet].iter_rows():
                    c.writerow([cell.value for cell in r])

        print("转换完成！")

        pass  # function

    @classmethod
    def _preprocess_original_adjacency_matrix_database_to_indexed_relational_table_database(cls, folderpath_csv: Path):
        """
        预处理文件夹内的每一个原始的前缀名为 'am_' 的 CSV 格式的邻接矩阵数据表，生成对应的带索引的关系型数据表，再次导出为前缀名为 'rt_' 的 CSV 格式文件。

        Args:
            folderpath_csv (Path): 原始的 CSV 文件所在的路径。

        Returns:

        """
        # folderpath_csv = Path(folderpath_csv)
        list_filepath_csv = list(folderpath_csv.glob('csv_am_*.csv'))

        for filepath_csv in list_filepath_csv:
            table_name = filepath_csv.stem

            if table_name.startswith("csv_am_"):
                # numpy 读取 csv 文件

                encoding_format = Tools.detect_encoding(str(filepath_csv))

                mat_adjacencyMatrix = pd.read_csv(filepath_csv, header=None, index_col=None, encoding=encoding_format).values  # 读取 CSV 文件，不设置表头，不设置索引

                df_panel = pd.DataFrame()  # 新建面板形式的 DataFrame

                titles_value = mat_adjacencyMatrix[0, 0]  # 提取 mat_adjacencyMatrix 首行首列元素的值

                # 计算 mat_adjacencyMatrix 里的矩阵的行数、列数分别是表格的行数、列数去掉首行首列元素后的值
                row_num = mat_adjacencyMatrix.shape[0] - 1
                col_num = mat_adjacencyMatrix.shape[1] - 1

                titles = titles_value.split('_')  # 按照下划线分割首行首列元素的值为字符串列表

                if titles[0] == 'mat':  # 判断 titles[0] 是否是'mat'，如果是，那么就是一个邻接矩阵表
                    is_adjacencyMatrix = True
                else:
                    is_adjacencyMatrix = False
                    pass  # if

                if is_adjacencyMatrix:
                    row_key = 'val_row_' + titles[1]  # 将 titles[1] 的值前面加上前缀 'val_row'，作为 df_panel 的第 1 列表头名

                    col_key = 'val_col_' + titles[2]  # 将 titles[2] 的值前面加上前缀 'val_col'，作为 df_panel 的第 2 列表头名

                    value_key = 'val_' + titles[3]  # 将 titles[3] 的值前面加上前缀 'con'，作为 df_panel 的第 3 列表头名

                    # 新建面板形式的 DataFrame。将 row_key、col_key、value_key 作为 df_panel 的列表头，分别对应 df_adjacencyMatrix 的【行值】、【列值】、【元素值】
                    df_panel = pd.DataFrame(columns=[row_key, col_key, value_key])

                    # 遍历邻接矩阵的第一列的从第二个元素开始的所有元素，然后复制 row_num 份，作为 df_panel 【行值】列的值
                    df_panel[row_key] = mat_adjacencyMatrix[1:, 0].repeat(row_num)

                    # 遍历邻接矩阵的第一行的从第二个元素开始的所有元素，然后以所有元素为一组，复制 col_num 份，作为 df_panel 【行值】列的值
                    df_panel[col_key] = np.tile(mat_adjacencyMatrix[0, 1:], col_num)

                    # 遍历邻接矩阵的从第二行开始的第二列开始的所有元素，作为 df_panel 【元素值】列的值
                    df_panel[value_key] = mat_adjacencyMatrix[1:, 1:].flatten()

                    pass  # if

                filename_csv_new = filepath_csv.name.replace("csv_am_", "csv_rt_")  # 新的文件名是原文件名的前缀名由 'csv_am_' 改为 'csv_rt_'。
                filepath_csv_new = Path(folderpath_csv) / filename_csv_new
                df_panel.to_csv(filepath_csv_new, index=False)
                pass  # if
            pass  # for

        pass  # function

    @classmethod
    def _preprocess_original_relational_table_database_to_indexed_relational_table_database(cls, folderpath_csv: Path):
        """
            预处理文件夹内的每一个前缀名为 'rt_' 的 CSV 格式的关系型数据表，生成对应的带索引的关系型数据表，再次导出为 CSV 格式的文件，覆盖原文件。

            预处理过程如下：
              1. 遍历各表格的字段名称，判断哪些字段是主键，哪些是主键对应的惟一的值，哪些是值键。这里定义字段名称前缀是 `'key_'` 的字段为【主键】。定义字段名称前缀是 `'name_'` 的字段为非前缀名称一致的主键对应的惟一的【名键】。定义字段名称前缀是 `'val_'` 的字段为非前缀名称一致的主键对应的【值键】（又称为【外键】）。定义除了上述三种字段之外其余的字段是【普通字段】；
              2. 查找索引：对于【值键】的每一个数据值，分别获取与【名键】数据值相同值对应的【主键】的值；
              3. 在【值键】之后插入一个新列，新的字段名非前缀与该【值键】之非前缀名同名，前缀名为 `'id_'` 。定义该新的字段为【索引键】。【索引键】之键值就是上一个步骤获取的那些值；


        Args:
            folderpath_csv (Path): 原始的 CSV 文件所在的路径。

        Returns:

        """
        dataframes, folderpath_csv = cls._load_CSVs_to_DataFrames(folderpath_csv, prefix='csv_rt_')

        # 遍历各个目标 DataFrame
        for target_table_name, df_target in dataframes.items():
            for column_name in df_target.columns:
                if column_name.startswith("val_"):
                    middle_string = ""
                    if (column_name.startswith("val_row_") or column_name.startswith("val_col_")):
                        if "row_" in column_name:
                            middle_string = "row_"
                        elif "col_" in column_name:
                            middle_string = "col_"
                            pass  # if
                    else:
                        # 匹配后缀名是任意位数字的字符串
                        suffix_string = re.search(r'_\d+$', column_name)
                        # if column_name
                        pass  # if

                    prefix_length = 4 if column_name.startswith("val_") else 3
                    middle_length = len(middle_string)
                    suffix_length = len(suffix_string.group()) if suffix_string else 0

                    valuekey_column_name = "val_" + middle_string + column_name[prefix_length + middle_length:] if suffix_length == 0 else "val_" + middle_string + column_name[prefix_length + middle_length:-suffix_length]
                    indexkey_column_name = "id_" + middle_string + column_name[prefix_length + middle_length:]
                    namekey_column_name = "name_" + column_name[prefix_length + middle_length:]
                    primarykey_column_name = "key_" + column_name[prefix_length + middle_length:]

                    # 遍历各个源 DataFrame
                    for source_table_name, df_source in dataframes.items():
                        if namekey_column_name in df_source.columns and primarykey_column_name in df_source.columns:
                            namekey_column_values = df_source[namekey_column_name].tolist()
                            primarykey_column_values = df_source[primarykey_column_name].tolist()

                            df_target[indexkey_column_name] = df_target[valuekey_column_name].map(
                                dict(zip(namekey_column_values, primarykey_column_values)))
                            pass  # if
                        pass  # for
                    pass  # if
                pass  # for

            df_target = df_target.loc[:, ~df_target.columns.str.contains('^Unnamed')]
            df_target = df_target.loc[:, df_target.columns.str.contains('_')]
            dataframes[target_table_name] = df_target
            pass  # for

        # 导出各个 DataFrame 为同名的 CSV 文件，覆盖原文件
        for table_name, df_target in dataframes.items():
            df_target.to_csv(Path(folderpath_csv, f'csv_rt_{table_name}.csv'), index=False)
            pass  # for

        pass  # function

    @classmethod
    def _preprocess_indexed_relational_table_database_to_matrix_array(cls, folderpath_csv: Path):
        """
        转换关系型数据表为二维矩阵形式

        预处理文件夹内的每一个前缀名为 'rt_' 的且与前缀名为 'am_' 的 CSV 格式的文件同名的文件，其内容是一个关系型数据表，将其转换为二维矩阵形式，导出为 NPY 格式的文件

        Args:
            folderpath_csv (Path): 原始的 CSV 文件所在的路径。

        Returns:

        """
        # 寻找文件夹内的每一个前缀名为 'rt_' 的且与前缀名为 'am_' 的 CSV 格式的文件同名的文件
        list_filepath_am_csv = list(folderpath_csv.glob('csv_am_*.csv'))
        list_table_middle_name = [filepath_csv.stem.split('_')[2] for filepath_csv in list_filepath_am_csv]
        list_filepath_rt_csv = [folderpath_csv / f'csv_rt_{middle_name}.csv' for middle_name in list_table_middle_name]

        # 遍历 list_filepath_rt_csv 每一个文件
        for filepath_rt_csv in list_filepath_rt_csv:
            df = pd.read_csv(filepath_rt_csv)
            list_column_names_with_id = [column for column in df.columns if column.startswith('id_')]  # 提取前缀名为 'id' 的列
            column_name_with_id_row = [column for column in list_column_names_with_id if 'row' in column][0]  # 获取前缀名为 'id' ，中缀名为 'row' 的列（唯一的列）
            column_name_with_id_col = [column for column in list_column_names_with_id if 'col' in column][0]  # 获取前缀名为 'id' ，中缀名为 'col' 的列（唯一的列）
            column_name_with_id_value = [column for column in list_column_names_with_id if column not in [column_name_with_id_row, column_name_with_id_col]][0]  # 从 list_column_names_with_id 中提取不包括 column_name_with_id_row 和 column_name_with_id_col 的列（唯一的列）
            # 使用 pivot 函数重塑数据
            df = df[list_column_names_with_id]
            df_pivot = df.pivot(index=column_name_with_id_row, columns=column_name_with_id_col, values=column_name_with_id_value)
            # 转换为 Numpy 数组
            array_pivot = df_pivot.values

            # 导出 Numpy 数组为 NPY 文件，文件名前缀名为 'am_'
            filepath_am_npy = Path(str(filepath_rt_csv).replace('csv_rt_', '')).with_suffix('')
            np.save(filepath_am_npy, array_pivot)

            # df_pivot.to_pickle(filepath_rt_csv.replace('csv_rt_', 'pkl_am_'))

            pass  # for

        pass  # function

    @classmethod
    def _preprocess_data_type_of_relational_table_database(cls, folderpath_csv: Path):
        """
        预处理文件夹内的每一个前缀名为 'rt_' 的 CSV 格式的关系型数据表，预处理各表格数据类型，然后分别导出为 CSV 格式的文件（覆盖原文件）、PKL 格式的文件，同时返回对应的数据表数据框。

        Args:
            folderpath_csv (Path): 原始的 CSV 文件所在的路径。

        Returns:
            dataframes (dict): 一个 DataFrame 字典，字典的键是文件名的中间部分，字典的值是对应的 DataFrame。
            folderpath_csv (Path): 文件夹的路径。

        """

        dataframes, folderpath_csv = cls._load_CSVs_to_DataFrames(folderpath_csv, prefix='csv_rt_')

        # 遍历各个目标 DataFrame
        for target_table_name, df_target in dataframes.items():
            for column in df_target.columns:
                # 获取列名前缀，分隔符为下划线
                column_prefix = column.split('_')[0]

                # 根据列名前缀，判断所需转换的列数据的数据类型（如果遇到公式则先计算公式获取结果）
                if column_prefix == 'f':  # 转换为浮点数类型
                    df_target[column] = df_target[column].apply(lambda x: pd.eval(x.split('=')[1]) if isinstance(x, str) and x.startswith('=') else x).astype(float)
                elif column_prefix in ['s', 'val', 'con']:  # 转换为字符串类型
                    df_target[column] = df_target[column].apply(lambda x: pd.eval(x.split('=')[1]) if isinstance(x, str) and x.startswith('=') else x).astype(str)
                elif column_prefix in ['u', 'id', 'ref']:  # 转换为无符号整数类型  #HACK 本来应该是无符号整形数据，但是因为在实际使用过程中难以使用这种类型，所以使用有符号整形代替。
                    df_target[column] = df_target[column].apply(lambda x: pd.eval(x.split('=')[1]) if isinstance(x, str) and x.startswith('=') else x).astype(np.int64)
                elif column_prefix == 'i':  # 转换为整数类型
                    df_target[column] = df_target[column].apply(lambda x: pd.eval(x.split('=')[1]) if isinstance(x, str) and x.startswith('=') else x).astype(np.int64)
                elif column_prefix == 'b':  # 转换为布尔类型
                    df_target[column] = df_target[column].apply(lambda x: pd.eval(x.split('=')[1]) if isinstance(x, str) and x.startswith('=') else x).astype(bool)
                elif column_prefix == 't':  # 转换为文本类型
                    df_target[column] = df_target[column].apply(lambda x: pd.eval(x.split('=')[1]) if isinstance(x, str) and x.startswith('=') else x).astype(str)
                else:
                    pass  # 如果前缀不匹配任何已知类型，不进行转换

                pass  # for

            dataframes[target_table_name] = df_target  # 更新 DataFrame
            pass  # for

        # 导出各个 DataFrame 为同名的 CSV 文件，覆盖原文件
        for table_name, df_target in dataframes.items():
            df_target.to_csv(Path(folderpath_csv, f'csv_rt_{table_name}.csv'), index=False)
            pass  # for

        # 导出各个 DataFrame 为同名的 pickles 文件
        for table_name, df_target in dataframes.items():
            df_target.to_pickle(Path(folderpath_csv, table_name + '.pkl'))
            pass  # for

        # # 导出各个 DataFrame 为同名的 HDF5 文件  #HACK 由于 HDF5 文件的导出功能暂时不可用，所以暂时注释掉这部分代码
        # for table_name, df_target in dataframes.items():
        #     df_target.to_hdf(Path(folderpath_csv, table_name + '.h5'), key='df', mode='w')  # 导出 DataFrame 数据表为 HDF5 文件
        #     pass  # for

        return dataframes, folderpath_csv

        pass  # function

    @classmethod
    def _load_CSVs_to_DataFrames(cls, folderpath_csv: Path, prefix='csv_rt_'):
        """
        从文件夹中加载所有的 CSV 文件，返回一个 DataFrames 字典，字典的键是文件名的中间部分，字典的值是对应的 DataFrame。

        Args:
            folderpath_csv (Path): 文件夹的路径。

        Returns:
            dataframes (dict): 一个字典，字典的键是文件名的中间部分，字典的值是对应的 DataFrame。
            folderpath_csv (Path): 文件夹的路径。

        """
        dataframes = {}
        # folderpath_csv = Path(folderpath_csv)
        list_filepath_csv = list(folderpath_csv.glob(f'{prefix}*.csv'))
        for filepath_csv in list_filepath_csv:
            table_name = filepath_csv.stem
            if table_name.startswith(prefix):  # 如果文件名的前缀是 'csv_rt_'，那么就是一个关系型数据表
                encoding = Tools.detect_encoding(filepath_csv)
                df = pd.read_csv(filepath_csv, encoding=encoding)
                table_middle_name = table_name.split("_")[2]
                dataframes[table_middle_name] = df
                pass  # if
            pass  # for
        return dataframes, folderpath_csv

        pass  # function

    @classmethod
    def load_PKLs_to_DataFrames(cls, folderpath: Path):
        """
        从文件夹中加载所有的 pkl 文件，返回一个 DataFrames 字典，字典的键是文件名的中间部分，字典的值是对应的 DataFrame。

        Args:
            folderpath (Path): 文件夹的路径。

        Returns:
            dataframes (dict): 一个字典，字典的键是文件名的中间部分，字典的值是对应的 DataFrame。
        """
        dataframes = {}

        # 导入 PKL 文件
        for filepath in folderpath.glob('*.pkl'):
            df = pd.read_pickle(filepath)
            table_middle_name = filepath.stem
            dataframes[table_middle_name] = df
            pass  # for

        # # 导入 NPY 文件 #HACK 如果需要高性能，则启用这部分代码
        # for filepath in folderpath.glob('*.npy'):
        #     array = np.load(filepath)
        #     table_middle_name = filepath.stem
        #     dataframes[table_middle_name] = array
        #     pass  # for

        return dataframes

    @classmethod
    def load_configs_from_excel_file_then_save_as_python_file(cls, folderpath_Excel: Path, filepath_python: Path = None):
        """
        从 Excel 文件中读取配置项和配置值，然后返回一个字典，根据配置项和配置值生成一个 Python 文件。该文件内容为一个字典，字典变量名为 config ，其中配置项是键，配置值是值。

        Args:
            folderpath_Excel (Path): Excel 文件的路径。
            filepath_python (str): 导出的 Python 文件的路径。默认相同于 Excel 路径，文件名为 config_dict.py 。

        Returns:
            result_dict (dict): 一个字典，其中配置项是键，配置值是值。

        """
        # df = pd.read_excel(folderpath_Excel)  # 读取 Excel 文件

        list_filepath_Excel = [f for f in folderpath_Excel.glob('*.xlsx') if not f.name.startswith("~$")]
        for filepath_Excel in list_filepath_Excel:
            xls = pd.ExcelFile(filepath_Excel)
            dict_df = {}
            for sheet_name in xls.sheet_names:
                dict_df[sheet_name] = xls.parse(sheet_name)
                pass  # for

            df_config = dict_df['config']

            # 提取需要的列
            keys = df_config['配置项']
            values = df_config['配置值']
            data_types = df_config['数据类型']
            config_types = df_config['配置类别']
            notes = df_config['备注']

            result_dict = {}  # 创建一个字典，其中配置项是键，配置值是值

            # 数据类型到处理函数的映射
            map_types_to_functions = {
                '路径字符串': lambda x: r'{}'.format(x),
                '字符串': lambda x: '{}'.format(x),
                '布尔值': lambda x: True if x == 'TRUE' else False if x == 'FALSE' else x,
                '代码段': lambda x: x,  # 这里我们只是存储代码段，不执行它
                '整数': lambda x: np.int64(x),
                '浮点数': lambda x: float(x),
                '引用': lambda x: dict_df[x],  # 如果数据类型是引用，那么就返回对应的 DataFrame
            }

            # 遍历所有的键、值和数据类型
            for key, value, data_type in zip(keys, values, data_types):
                if data_type in map_types_to_functions:  # 根据数据类型处理值
                    result_dict[key] = map_types_to_functions[data_type](value)
                else:
                    result_dict[key] = value  # 如果数据类型未知，只存储原始值
                    pass  # if
                pass  # for

            # 保存为 Python 文件，文件是一个字典 config，其中配置项是键，配置值是值
            filepath_python = filepath_python if filepath_python else Path(folderpath_Excel, r"config.py")
            modules = set()
            with open(filepath_python, 'w') as f:
                for key, value, data_type in zip(keys, values, data_types):
                    if data_type == '代码段':  # 如果数据满足以下条件，就解析代码，找出所有的模块名
                        tree = ast.parse(value)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Store) and node.id not in dir(builtins):
                                modules.add(node.id)
                                pass  # if
                            pass  # for
                        pass  # if
                    pass  # for
                pass  # with
                # 在文件的开头添加 import 语句
                for module in modules:
                    f.write(f"import {module}\n")
                    pass  # for
                # 写入字典
                f.write('\nconfig = dict(\n')
                for key, value, data_type, config_type, note in zip(keys, values, data_types, config_types, notes):
                    if data_type == '代码段' or data_type == '布尔值' or data_type == '整数' or data_type == '浮点数':  # 如果数据类型满足以下条件，就特殊处理，否则作为字符串处理
                        data_value = value
                        # f.write(f"    {key}={value},\n")
                    else:  # 否则，就将值作为字符串处理
                        data_value = rf"'{value}'"  # #BUG 可能存在转义字符的问题
                        # f.write(f"    {key}=r'{value}',\n")
                        pass  # if
                    # 将【配置项】、【配置值】以键值对形式作为代码内容写入文件行，将【数据类型】、【配置类别】、【备注】作为注释写入文件行
                    f.write(f"    {key}={data_value},  # 数据类型：{data_type}，配置类别：{config_type}。{note}\n")
                    pass  # for
                f.write(')\n')
                pass  # with
            pass  # for

        return result_dict
        pass  # function

    pass  # class
