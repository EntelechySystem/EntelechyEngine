"""
各种工具集
"""

from engine.externals import sys, os, logging, time, Path, itertools, pkgutil, importlib, re, np, pd, random, string, shutil, locale, Union, DataFrame, pickle, base64, subprocess, chardet

pass  # end import


class Tools:

    @classmethod
    def setup_working_directory(cls):
        """
        设置工作目录。 #BUG 无用

        检查是否在控制台运行，如果是，则切换到脚本所在的文件夹然后执行，如果不是，则通过主程序调用该程序。

        Returns:
            folderpath_settings (str) 文件夹路径字符串

        """
        # 检查是否在控制台运行
        if Path(sys.argv[0]).name == Path(__file__).name:
            # 在控制台运行，切换到脚本所在的文件夹
            folderpath_settings = Path(__file__).resolve().parent
            os.chdir(folderpath_settings)
        else:
            # 通过其他脚本运行，执行特定的代码
            list_args = Tools.decode_args([*sys.argv[1:]])
            folderpath_settings = list_args[0]
            pass  # if
        return folderpath_settings

    @classmethod
    def extract_number(pattern, filename):
        match = re.search(pattern, filename)
        if match:
            return int(match.group(1))
        else:
            return 0

    @classmethod
    def _check_and_install_packages(cls, list_packages_name: list):
        """
        检查并安装列表中指定的工具包名的工具包。

        Args:
            list_packages_name (list): 待安装的工具包名列表

        Returns:
            (bool) 是否已经安装全部工具包

        """
        list_is_installed = list()
        for package_name in list_packages_name:
            try:
                module = importlib.import_module(package_name)
                logging.info(f"已经安装过了模块{package_name}")
                del module  # BUG 这个可能存在误删除当前命名空间同名的其它模块的风险
                list_is_installed.append(True)
            except ImportError:
                print(f"{package_name} 未安装，正在进行安装...")
                try:
                    import subprocess

                    subprocess.check_call(['pip3', 'install', package_name])
                    print(f"{package_name} 安装成功")
                    list_is_installed.append(True)
                except Exception as e:
                    print(f"{package_name} 安装失败: {e}")
                    list_is_installed.append(False)
            pass  # for

        return all(list_is_installed)
        pass  # function

    @classmethod
    def _check_and_install_package(cls, str_package_name: str):
        try:
            importlib.import_module(str_package_name)
            print(f"{str_package_name} is already installed")
            return True
        except ImportError:
            print(f"{str_package_name} is not installed, installing...")
            try:
                import subprocess
                subprocess.check_call(["pip", "install", str_package_name])
                print(f"{str_package_name} has been installed")
                return True
            except Exception as e:
                print(f"Failed to install {str_package_name}: {e}")
                return False

    @classmethod
    def dict_to_product_list(cls, d: dict) -> list:
        """
        将字典的值转换为字典列表，其中列表的元素表示字典的笛卡尔积。输入字典中的每个值都应该是一个列表。

        Args:
            d (dict): 要转换的字典。

        Returns:
            list: 表示笛卡尔积的字典列表。

        Example:
            ```python
             d = {'a': [1, 2], 'b': [3, 4]}
             Tools.dict_to_product_list(d)
            [{'a': 1, 'b': 3}, {'a': 1, 'b': 4}, {'a': 2, 'b': 3}, {'a': 2, 'b': 4}]
            ```
        """
        t = list(d.values())
        l = list(itertools.product(*t, repeat=1))
        pdl = [dict(zip(d.keys(), v)) for v in l]
        return pdl
        pass  # function

    @classmethod
    def dict_to_product_dataFrame(cls, d: dict) -> DataFrame:
        """
        将字典的值转换为数据框，其中列表的元素表示字典的笛卡尔积。输入字典中的每个值都应该是一个列表。

        Args:
            d (dict): 要转换的字典。

        Returns:
            (pd.DataFrame): 表示笛卡尔积的字典列表。

        Example:
            ```python
            d = {'a': [1, 2], 'b': [3, 4]}
            dict_to_product_dataFrame(d)
            ```
            输出结果：
            ```text
                a  b
            0  1  3
            1  1  4
            2  2  3
            3  2  4
            ```
        """
        t = list(d.values())
        l = list(itertools.product(*t, repeat=1))
        # pd_combination_of_para = [dict(zip(d.keys(), v)) for v in l]
        pd_combination_of_para = pd.DataFrame(l, columns=d.keys())
        return pd_combination_of_para
        pass  # function

    @classmethod
    def set_experiments_folders(
            cls,
            foldername_experiments_output_data: str,
            foldername_experiments_output: str,
            str_folderpath_experiments_projects: str,
            str_folderpath_root_experiments_output: str,
            str_foldername_engine: str,
            str_folderpath_relpath_engine: str,
            str_foldername_outputData: str,
            str_folderpath_relpath_outputData: str,
            str_folderpath_models: str,
            str_folderpath_config: str,
            str_folderpath_settings: str,
            str_folderpath_parameters: str,
            str_folderpath_agents: str
    ):
        """
        设置实验相关的文件夹路径。包括实验设置项文件夹、模型文件夹、实验导出数据文件夹、引擎工具所在的文件夹等。

        根据【实验导出数据文件夹名称】、【实验文件夹名称】等，生成【项目文件夹路径】、【引擎工具文件夹路径】、【实验项目文件夹路径】、【实验输出文件夹路径】、【实验导出数据文件夹路径】、【模型文件夹路径】、【实验配置项设置项文件夹路径】、【实验参数设置项文件夹路径】、【实验实验个体众数据初始化设置项文件夹路径】等。

        Args:
            foldername_experiments_output_data (str): 实验导出数据文件夹名称
            foldername_experiments_output (str): 实验输出文件夹名称
            str_folderpath_experiments_projects (str): 实验项目文件夹相对路径字符串
            str_folderpath_root_experiments_output (str): 实验输出文件夹根相对路径字符串
            str_foldername_engine (str): 引擎所在的项目之名称
            str_folderpath_relpath_engine (str): 当前项目根路径到引擎所在的项目之相对路径
            str_foldername_outputData (str): 输出数据所在的主文件夹之名称
            str_folderpath_relpath_outputData (str): 当前项目根路径到输出数据所在的主文件夹之相对路径
            str_folderpath_models (str): 模型文件夹相对路径字符串
            str_folderpath_config (str): 实验配置项文件夹相对路径字符串
            str_folderpath_settings (str): 实验设置项文件夹相对路径字符串
            str_folderpath_parameters (str): 实验参数项文件夹相对路径字符串
            str_folderpath_agents (str): 实验实验个体众数据初始化设置项文件夹相对路径字符串

        Returns:

            folderpath_project (Path): 项目文件夹路径

            folderpath_engine (Path): 引擎工具文件夹路径

            folderpath_experiments_projects (Path): 实验项目所在文件夹路径

            folderpath_experiments_output (Path): 实验导出文件夹路径

            folderpath_experiments_output_data (Path): 实验导出数据文件夹路径

            folderpath_experiments_output_log (Path): 实验输出日志文件夹路径

            folderpath_experiments_output_config (Path): 实验输出配置项设置文件夹路径

            folderpath_experiments_output_settings (Path): 实验输出设置项文件夹路径

            folderpath_experiments_output_parameters (Path): 实验输出参数项文件夹路径

            folderpath_experiments_output_agents (Path): 实验输出实验个体众数据初始化设置项文件夹路径

            folderpath_experiments_output_models (Path): 实验输出模型文件夹路径

            folderpath_models (Path): 模型文件夹路径

            folderpath_config (Path): 实验配置项文件夹路径

            folderpath_settings (Path): 实验设置项文件夹路径

            folderpath_parameters (Path): 实验参数项文件夹路径

            folderpath_agents (Path): 实验实验个体众数据初始化设置项文件夹路径
        """

        ## 设置项目文件夹路径
        folderpath_project = Tools._get_current_project_rootpath()
        folderpath_engine = Tools.get_project_rootpath(str_foldername_engine, str_folderpath_relpath_engine)
        folderpath_outputData = Tools.get_project_rootpath(str_foldername_outputData, str_folderpath_relpath_outputData)

        folderpath_experiments_projects = Path(folderpath_project, str_folderpath_experiments_projects)

        folderpath_experiments_output = Path(folderpath_outputData, str_folderpath_root_experiments_output, foldername_experiments_output)

        folderpath_experiments_output.mkdir(parents=True, exist_ok=True)

        if foldername_experiments_output_data is not None:
            folderpath_experiments_output_data = Path(folderpath_experiments_output, foldername_experiments_output_data)
            folderpath_experiments_output_data.mkdir(parents=True, exist_ok=True)  # 创建文件夹，以导出实验输出数据
        else:
            folderpath_experiments_output_data = None
            pass

        folderpath_experiments_output_log = Path(folderpath_experiments_output, "outputlog")
        folderpath_experiments_output_log.mkdir(parents=True, exist_ok=True)  # 创建文件夹，以导出实验输出日志

        folderpath_experiments_output_config = Path(folderpath_experiments_output, "config")
        folderpath_experiments_output_config.mkdir(parents=True, exist_ok=True)  # 创建文件夹，以导出实验输出配置项设置

        folderpath_experiments_output_settings = Path(folderpath_experiments_output, "settings")
        folderpath_experiments_output_settings.mkdir(parents=True, exist_ok=True)  # 创建文件夹，以导出实验输出配置项设置

        folderpath_experiments_output_parameters = Path(folderpath_experiments_output, "parameters")
        folderpath_experiments_output_parameters.mkdir(parents=True, exist_ok=True)  # 创建文件夹，以导出实验输出参数项设置

        folderpath_experiments_output_agents = Path(folderpath_experiments_output, "agents")
        folderpath_experiments_output_agents.mkdir(parents=True, exist_ok=True)  # 创建文件夹，以导出实验输出实验个体众数据初始化设置

        folderpath_experiments_output_models = Path(folderpath_experiments_output, "models")
        folderpath_experiments_output_models.mkdir(parents=True, exist_ok=True)  # 创建文件夹，以导出实验输出模型文件夹

        ## 设定实验相关的一些重要的文件夹
        folderpath_models = Path(folderpath_project, str_folderpath_models)  # 设定模型文件夹
        folderpath_config = Path(folderpath_project, str_folderpath_config)  # 设定实验配置项文件夹
        folderpath_settings = Path(folderpath_project, str_folderpath_settings)  # 设定实验设置项文件夹
        folderpath_parameters = Path(folderpath_project, str_folderpath_parameters)  # 设定实验参数项文件夹
        folderpath_agents = Path(folderpath_project, str_folderpath_agents)  # 设定实验实验个体众数据初始化设置项文件夹

        return (
            folderpath_project,
            folderpath_engine,
            folderpath_experiments_projects,
            folderpath_experiments_output,
            folderpath_experiments_output_data,
            folderpath_experiments_output_log,
            folderpath_experiments_output_config,
            folderpath_experiments_output_settings,
            folderpath_experiments_output_parameters,
            folderpath_experiments_output_agents,
            folderpath_experiments_output_models,
            folderpath_models,
            folderpath_config,
            folderpath_settings,
            folderpath_parameters,
            folderpath_agents,
        )

        pass  # function

    @classmethod
    def set_foldername_experiments(cls, foldername_prefix_experiments: str, foldername_set_manually: str, is_datetime: bool, type_of_experiments_foldername: str):
        """
        设定实验文件夹名称。

        Args:
            foldername_prefix_experiments (str): 实验文件夹前缀名称。默认"default"。用于 `type_of_experiments_foldername=r"default"`；；
            foldername_set_manually (str): 手动设置生成的实验文件夹全名。用于 `type_of_experiments_foldername=r"set manually"`；
            is_datetime (bool): 是否使用日期时间字符串。默认True；
            type_of_experiments_foldername (str): 实验文件夹名称类型。取值："default"、"set manually"。默认"default"；

        Returns:

        """

        ## 设定实验结果导出文件夹
        if type_of_experiments_foldername == "default":  # 设定前缀字符串
            str_manuallyName = foldername_prefix_experiments
            if is_datetime is True:  # 设定日期时间字符串
                str_datetime = "_" + time.strftime("%Y%m%d%H%M%S")
            else:
                str_datetime = ""
                pass  # if
            foldername_experiments_output = str_manuallyName + str_datetime
        elif type_of_experiments_foldername == "set manually":
            foldername_experiments_output = foldername_set_manually
        else:
            raise Exception("关键词取值错误！".format(type_of_experiments_foldername))
            pass  # if
        return foldername_experiments_output

    @classmethod
    def _get_current_project_rootpath(cls):
        """
        获取当前项目根目录。此函数的能力体现在，不论当前module被import到任何位置，都可以正确获取项目根目录。

        > 借鉴来源：
        > [PyCharm 项目获取项目路径的方法](https://blog.csdn.net/weixin_42787086/article/details/124625385)

        Returns:
           project_path (Path): 当前项目根路径

        """
        is_OK = False
        path = Path.cwd().resolve()
        while True:
            for subpath in path.iterdir():
                if '.idea' in subpath.name:  # 如果是 PyCharm 项目中，那么该名称是必然存在的，且名称唯一
                    project_path = path
                    is_OK = True
                elif '.vscode' in subpath.name:  # 如果是 vscode 项目中，那么该名称有可能是存在的
                    project_path = path
                    is_OK = True
                elif '.git' in subpath.name:  # 如果有 Git 托管，那么该名称是必然存在的，且名称唯一
                    project_path = path
                    is_OK = True
                elif 'SystemicRiskEngine' in subpath.name:  # 这个是本工具包之项目对应之工具包之文件夹之名称。# NOTE 如果更改了工具包之文件夹名称，那么这里也要做相应的修改。
                    project_path = path
                    is_OK = True
                    pass  # if
                if is_OK:
                    return project_path
                pass  # for
            path = path.parent
            pass  # while
        if ~is_OK:
            raise Exception("找不到当前项目之根路径！")
        pass  # function

    @classmethod
    def get_project_rootpath(cls, foldername_project: str = None, folderpath_relpath_project: str = None):
        """
        获取指定的项目根路径。

        如果参数栏不指定项目名称，也不指定项目相对路径，则默认为获取当前项目根路径。

        Args:
            foldername_project (str): 项目名称
            folderpath_relpath_project (str): 当前项目到指定项目之相对路径

        Returns:
            folderpath_project (Path): 项目根路径


        """
        if foldername_project is None and folderpath_relpath_project is None:  # 如果不指定项目名称，也不指定项目相对路径，则默认为当前项目
            current_project_rootpath = Tools._get_current_project_rootpath()
            folderpath_project = current_project_rootpath
            return folderpath_project
        else:  # 获取指定项目之根路径
            current_project_rootpath = Tools._get_current_project_rootpath()
            folderpath_relpath_project = Path(folderpath_relpath_project)
            folderpath_project = (current_project_rootpath / Path(folderpath_relpath_project, foldername_project)).resolve()
            return folderpath_project
            pass  # if
        pass  # function

    @classmethod
    def _copy_files_from_other_folders(cls, folderpath_source: Path, folderpath_target: Path, is_auto_confirmation: bool = False):
        """
        从指定的文件夹复制其全部的子文件夹及其子文件到目标文件夹。

        一些特殊文件夹会被忽略：
        - `__pycache__`：Python 编译之后的文件夹

        这个功能比较危险，因为可能会出现复制文件夹到其它位置的操作，所以要求用户确认操作。

        Args:
            folderpath_source (Path): 源文件夹相对路径字符串或者Path对象
            folderpath_target (Path): 目标文件夹相对路径字符串或者Path对象
            is_auto_confirmation (bool): 是否自动确认操作。默认False。

        Returns:
            None
        """

        confirmation = 'n'

        # folderpath_project = Tools.get_project_rootpath('SystemicRiskEngine', folderpath_relpath_project)

        # if isinstance(folderpath_source, str):
        #     folderpath_source = Path(folderpath_project, folderpath_source)
        # if isinstance(folderpath_target, str):
        #     folderpath_target = Path(folderpath_project, folderpath_target)

        if folderpath_source.exists() and folderpath_source.is_dir():
            if is_auto_confirmation == True:
                confirmation = 'y'
            else:
                confirmation = input(rf"确认要复制文件夹 {folderpath_source} 及其内容到 {folderpath_target} 吗？(y/[n]): ")

            if confirmation.lower() == 'y':
                for file in folderpath_source.iterdir():
                    if file.is_dir():
                        if file.name == "__pycache__":  # 忽略特殊文件夹
                            continue
                        shutil.copytree(file, Path(folderpath_target, file.name))
                    else:
                        if not file.name.startswith('~$'):  # 检查文件名是否以 '~$' 开头
                            shutil.copy(file, Path(folderpath_target))
                        else:
                            print(f"文件 {file} 被忽略，跳过复制。")
                            pass  # if
                        pass  # if
                    pass  # for
                print(f"文件夹 {folderpath_source.name} 已成功复制到 {folderpath_target.name} ！")
            else:
                print("复制操作已取消！")
                pass  # if
        else:
            print(f"文件夹 {folderpath_source.name} 不存在！")
            pass  # if

        pass  # function

    @classmethod
    def import_modules_from_package(cls, str_folderpath: str, pattern: str, str_folderpath_project: str):
        """
        从包批量导入模块与方法

        Args:
            str_folderpath (str): 包所在路径字符串
            pattern (str): 匹配模式
            str_folderpath_project (str): 项目文件夹路径字符串

        Returns:
            list_contents: 内容列表
        """

        # str_folderpath = cls._translate_package_form_path_to_folder_form_path(str_package_form_path) # NOTE 仅当如果用到以模块形式的包之路径的时候启用。
        module_form_path_package = cls._translate_folder_form_path_to_package_form_path(str_folderpath, str_folderpath_project)

        ## 遍历以导入内容函数
        idx_file = 0
        list_files = []  # 文件列表
        list_contents = {}  # 内容列表

        for module_finder_01, name_01, is_pkg in pkgutil.walk_packages([str_folderpath.__str__()]):
            if is_pkg:  # 如果路径下面还有一级子文件夹
                for module_finder_02, name_02, _ in pkgutil.iter_modules([Path(module_finder_01.path).joinpath(name_01).__str__()]):
                    list_files.append(importlib.import_module("." + name_02, module_form_path_package + "." + Path(module_finder_02.path).name))
                    if re.search(pattern, Path(list_files[idx_file].__str__()).name) is not None:
                        for content in dir(list_files[idx_file]):
                            if re.search(pattern, content.__str__()) is not None:
                                list_contents.update({name_02: list_files[idx_file].__dict__.get(content)})
                    idx_file += 1
            else:  # 如果路径下面没有子文件夹
                list_files.append(importlib.import_module("." + name_01, module_form_path_package))
                if re.search(pattern, Path(list_files[idx_file].__str__()).name) is not None:
                    for content in dir(list_files[idx_file]):
                        if re.search(pattern, content.__str__()) is not None:
                            list_contents.update({name_01: list_files[idx_file].__dict__.get(content)})
                idx_file += 1

        return list_contents

        pass  # function

    @classmethod
    def _translate_folder_form_path_to_package_form_path(cls, str_folder_form_path: str, str_folderpath_project: str):
        """
        转换文件夹形式的包之相对路径为模块形式的包之相对路径

        Args:
            str_folder_form_path (str): 文件夹形式的包之路径字符串
            str_folderpath_project (str): 项目文件夹路径字符串

        Returns: 模块形式的包之相对路径

        """
        str_folder_form_path = Path(str_folder_form_path)  # 获取包文件夹路径
        pattern = r"[\/\\]"
        repl = r"."
        return re.sub(pattern, repl, Path(str_folder_form_path).relative_to(str_folderpath_project).__str__())
        pass  # function

    @classmethod
    def _translate_package_form_path_to_folder_form_path(cls, str_package_form_path: str):
        """
        转换模块形式的包之相对路径为文件夹形式的包之绝对路径

        Args:
            str_package_form_path (str): 以模块形式的包之路径字符串

        Returns: 包所在的绝对路径

        """
        pattern = r"\."
        repl = r"/"
        result = re.sub(pattern, repl, str_package_form_path)
        return Path(result).resolve()
        pass  # function

    @classmethod
    def _delete_and_recreate_folder(cls, folderpath_target: Path, is_auto_confirmation: bool = False):
        """
        删除非空文件夹并重新创建文件夹。

        这个功能比较危险，因为会删除非空文件夹，所以要求用户确认操作。

        Args:
            folderpath_target (Path): 文件夹相对路径字符串或者Path对象
            is_auto_confirmation (bool): 是否自动确认操作。默认False。

        """
        # folderpath_project = Tools.get_project_rootpath("SystemicRiskEngine", foldername_project, folderpath_relpath_project)

        # if isinstance(folderpath_target, str):
        #     folderpath_target = Path(folderpath_project, folderpath_target)

        confirmation = 'n'
        # folder_path = folderpath_target
        if folderpath_target.exists() and folderpath_target.is_dir():
            if len(list(folderpath_target.glob('*'))) > 0:
                if is_auto_confirmation == True:
                    confirmation = 'y'
                else:
                    confirmation = input(rf"确认要删除文件夹 {folderpath_target} 及其内容吗？(y/[n]): ")

                if confirmation.lower() == 'y':
                    shutil.rmtree(folderpath_target)
                    folderpath_target.mkdir()
                    print(f"文件夹 {folderpath_target.name} 已成功删除并重新创建！")
                else:
                    print("删除重建操作已取消！")
            else:
                print(f"文件夹 {folderpath_target.name} 为空，无需删除！")
        else:
            print(f"文件夹 {folderpath_target.name} 不存在！直接新建一个文件夹。")
            folderpath_target.mkdir(parents=True, exist_ok=True)
        pass  # function

    @classmethod
    def MinMaxScaler(cls, data: Union[list, np.ndarray], min_max_range: tuple) -> np.ndarray:
        """
        指定范围，归一化数组之各元素到范围内。

        Args:
            data (Union[list, np.ndarray]): 待处理的数组
            min_max_range (tuple): 范围，(最小范围, 最大范围)

        Returns: 列表形式的归一化数组。
        """
        if len(data) == 0:
            raise Exception("列表为空！")
            pass  # if

        if isinstance(data, list):
            is_list = True
            data_numpy = np.asarray(data)
        elif isinstance(data, np.ndarray):
            is_list = False
            data_numpy = data
        else:
            raise Exception("错误的数据类型！")
            pass  # if

        transformed_data = ((data_numpy - np.min(data_numpy) + 0.0001) / (np.max(data_numpy) - np.min(data_numpy) + 0.0001)) * (min_max_range[1] - min_max_range[0]) + min_max_range[0]

        return transformed_data
        # if is_list:
        #     return list(transformed_data)
        # else:
        #     return transformed_data
        pass  # function

    @classmethod
    def generate_unique_identifier(cls):
        """
        随机生成一个8位的英文大小写字母和阿拉伯数字混合的字符串作为id。

        注意，区分大小写。

        Returns:
            str: id字符串
        """
        while True:
            # 生成一个随机的字符串
            new_identifier = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            return new_identifier
        pass  # function

    @classmethod
    def get_folder_info(cls, work_address, folder_source, folder_target, suffix_source, suffix_target):
        """
        获取文件夹及其子文件信息

        Args:
            work_address (str): 工作路径
            folder_source (str): 源文件夹名称
            folder_target (str): 目标文件夹名称
            suffix_source (str): 源文件后缀名
            suffix_target (str): 目标文件后缀名

        Returns:
            dict: 文件夹及其子文件信息
        """
        locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')  # 设置中文拼音排序
        rootPath_source = Path(work_address, folder_source)  # 原始文件根路径
        rootPath_target = Path(work_address, folder_target)  # 目标文件根路径
        fileNamesWithSuffix = [f.name for f in rootPath_source.glob(f'*{suffix_source}')]  # 文件名含后缀名 #DEBUG 还没有测试过
        regularPattern = re.compile(f".*[^(\\.{suffix_source})]")
        fileNames = [re.search(regularPattern, f).group() for f in fileNamesWithSuffix]  # 纯文件名
        filePath_source = [Path(rootPath_source, f) for f in fileNamesWithSuffix]  # 文件路径
        filePath_target = [Path(rootPath_target, f"{name}{suffix_target}") for name in fileNames]  # 目标文件路径
        # 排序列表
        fileNames.sort(key=locale.strxfrm)
        fileNamesWithSuffix.sort(key=locale.strxfrm)
        filePath_source.sort(key=locale.strxfrm)
        filePath_target.sort(key=locale.strxfrm)

        results = {
            "fileNames": fileNames,
            "fileNamesWithSuffix": fileNamesWithSuffix,
            "filePath_source": filePath_source,
            "filePath_target": filePath_target
        }

        return results
        pass  # function

    @classmethod
    def get_fields_info(cls, list_tibble):
        """
        获取表头字段

        Args:
            list_tibble (list): 表格列表

        Returns:
            list: 表头字段列表
        """
        list_string_field = []
        for i in range(len(list_tibble)):
            list_string_field.append(list_tibble[i].iloc[0, :].astype(str).tolist())
        return list_string_field
        pass  # function

    @classmethod
    def transform_one_of_expOutputData_from_panel_form_to_ndarray(cls, input_data: pd.Series, shape: tuple):
        """
        转换实验输出的数据当中的其中一个类别的数据，从序列形式转换成 ndarray 形式。
        Args:
            input_data (pd.Series): 待转换的数据
            shape (tuple): 需要转换的数据形状

        Returns:
            result (np.ndarray): 转换后的数据

        """

        if shape == ('time', 'agents'):
            arrays_list = []
            for array in input_data:
                arrays_list.append(array.flatten())
            result = np.vstack(arrays_list)
        return result
        pass  # function

    @classmethod
    def run_python_program_file(cls, filepath_python_program: Path, list_args: list = None):
        """
        运行指定的Python程序文件。参数代入方式为通过pickle序列化后的 base64 编码字符串。

        Args:
            filepath_python_program (Path): Python程序文件路径
            list_args (list): 参数列表，其中每个参数都是一个pickle序列化后的 base64 编码字符串，默认为None。

        Returns:

        """
        if list_args is not None:
            list_args_base64 = cls.encode_args(list_args)
            subprocess.run(["python", str(filepath_python_program), *list_args_base64])
        else:
            subprocess.run(["python", str(filepath_python_program)])
            pass  # if

        print(f"运行{filepath_python_program.name}！")

        pass  # function

    @classmethod
    def encode_args(cls, list_args: list):
        """
        对参数列表进行 pickle 序列化后的 base64 编码。

        Args:
            list_args (list): 参数列表

        Returns:
            list_args_base64 (list): pickle 序列化后的 base64 编码字符串列表

        """
        list_args_base64 = []
        if list_args is not None:
            for args in list_args:
                if args is not None:
                    args_pkl = pickle.dumps(args)
                    args_base64 = base64.b64encode(args_pkl).decode('utf-8')
                    list_args_base64.append(args_base64)
        return list_args_base64

    @classmethod
    def decode_args(cls, list_args_base64: list):
        """
        对 pickle 序列化后的 base64 编码字符串列表进行解码。

        Args:
            list_args_base64 (list): pickle 序列化后的 base64 编码字符串列表

        Returns:
            list_args (list): 参数列表

        """
        list_args = []
        for args_base64 in list_args_base64:
            args_pkl = base64.b64decode(args_base64)
            args = pickle.loads(args_pkl)
            list_args.append(args)
        return list_args

    @classmethod
    def flatten_dict(cls, d, depth, parent_key='', sep='_', current_depth=1):
        """
        将嵌套的字典扁平化。

        Args:
            d (dict): 待扁平化的字典
            depth (int): 扁平化的深度
            parent_key (str): 父键
            sep (str): 分隔符
            current_depth (int): 当前深度

        Returns:
            dict: 扁平化后的字典

        Example:
            ```python
            # 定义一个嵌套的字典
            nested_dict = {"a": {"b": 1, "c": {"d": 2, "e": 3}}, "f": 4}

            # 使用 flatten_dict 函数将嵌套的字典扁平化
            flattened_dict = flatten_dict(nested_dict, 1)

            # 打印扁平化后的字典
            print(flattened_dict)
            ```
            输出结果：
            ```text
            {'a_b': 1, 'a_c_d': 2, 'a_c_e': 3, 'f': 4}
            ```
        """
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict) and current_depth < depth:
                items.update(cls.flatten_dict(v, depth, new_key, sep, current_depth + 1))
            else:
                items[new_key] = v
                pass  # if
            pass  # for
        return items
        pass  # function

    @classmethod
    def transform_all_Path_value_to_string(cls, dict: dict):
        """
        转换字典里所有 Path 对象为字符串。

        Args:
            dict (dict): 待转换的字典

        Returns:
            None
        """
        for key, value in dict.items():
            if isinstance(value, Path):
                dict[key] = str(value)
                pass  # if
            pass  # for
        pass  # function

    @classmethod
    def detect_encoding(cls, file_path):
        """
        检测文件编码。

        Args:
            file_path (str): 文件路径

        Returns:
            str: 文件编码
        """
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding']

        pass  # function

    @classmethod
    def generate_agents_definitions_from_dicts_to_new_classes_as_python_file(cls, filepath_dicts: str, filepath_classes: str):
        """
        从初始化 Agents 的字典生成对应的类，但是不做设置。该类导出为一个 Python文件。DEBUG 还没有做任何测试！

        Warnings:
            警告：这个功能会直接改写文件，所以请务必做好备份！

        Args:
            filepath_dicts (str): 字典文件路径
            filepath_classes (str): 类文件路径

        Returns:
            None

        """
        import numpy as np
        import ast
        import re

        # 读取set_agents_variables.py文件
        with open('libraries/agents_library/agents_test/set_agents_variables.py', 'r') as file:
            lines = file.readlines()

        # 使用正则表达式和ast模块找到字典定义
        dict_strings = re.findall(r'set_agents_variables = (.*?)\n\nset_interagents_variables', ''.join(lines), re.DOTALL)
        dicts = [ast.literal_eval(dict_string) for dict_string in dict_strings]

        # 获取每个键值对后面的注释
        comments = re.findall(r'# (.*?)\n', ''.join(lines))

        # 创建新的Python文件
        with open('new_classes.py', 'w') as file:
            for i, dict_ in enumerate(dicts):
                # 写入类定义的开始部分
                file.write(f'class agent{i + 1}:\n')
                file.write('    def __init__(self):\n')

                # 为每个键生成一个类属性
                for j, key in enumerate(dict_.keys()):
                    file.write(f'        self.{key} = np.NaN  # {comments[j]}\n')

                # 在类之间添加空行
                file.write('\n')

            pass  # with

        pass  # function


    @classmethod
    def draw_color_band_before_experiments(ids: list, process_status: list, plans_status: list, tasks_status: list, filepath_to_save: Path):
        """
        绘制实验组的状态分布图

        Args:
            ids (list): 实验组 id
            process_status (list): 实验组的处理状态
            plans_status (list): 实验组的计划状态
            tasks_status (list): 实验组的任务状态
            filepath_to_save (Path): 保存文件路径

        Returns:

        """
        import matplotlib.pyplot as plt
        color_mapping_01 = {"RAW": "yellow", "DOING": "red", "DONE": "gray"}  # 创建状态颜色映射
        color_mapping_02 = {"PLAN": "blue"}
        color_mapping_03 = {"TASK": "green"}
        fig, axs = plt.subplots(3, 1, figsize=(10, 6))  # 创建图形和子图
        colors_01 = [color_mapping_01[status] for status in process_status]  # 绘制第一行彩条
        axs[0].bar(ids, [1] * len(ids), color=colors_01, width=1.0)
        axs[0].set_xticks([])
        axs[0].set_yticks([])
        colors_02 = [color_mapping_02[status] for status in plans_status]  # 绘制第二行彩条
        axs[1].bar(ids, [1] * len(ids), color=colors_02, width=1.0)
        axs[1].set_xticks([])
        axs[1].set_yticks([])
        colors_03 = [color_mapping_03[status] for status in tasks_status]  # 绘制第三行彩条
        axs[2].bar(ids, [1] * len(ids), color=colors_03, width=1.0)
        axs[2].set_xticks([])
        axs[2].set_yticks([])
        plt.savefig(filepath_to_save, bbox_inches='tight', pad_inches=0)  # 保存图形

        pass  # function

    @classmethod
    def draw_color_band_after_experiments(ids: list, process_status: list, filepath_to_save: Path):
        """
        绘制实验组 id 分布对应的实验组作业运行之前的作业完成状态信息。

        Args:
            ids (list): 实验组 id
            process_status (list): 实验组的处理状态
            plans_status (list): 实验组的计划状态
            tasks_status (list): 实验组的任务状态
            filepath_to_save (Path): 保存文件路径

        Returns:

        """
        import matplotlib.pyplot as plt
        color_mapping_01 = {"RAW": "yellow", "DOING": "red", "DONE": "gray"}  # 创建状态颜色映射
        fig, axs = plt.subplots(1, 1, figsize=(10, 2))  # 创建图形和子图
        colors_01 = [color_mapping_01[status] for status in process_status]  # 绘制第一行彩条
        axs[0].bar(ids, [1] * len(ids), color=colors_01, width=1.0)
        axs[0].set_xticks([])
        axs[0].set_yticks([])
        plt.savefig(filepath_to_save, bbox_inches='tight', pad_inches=0)  # 保存图形

        pass  # function

    pass  # class
