"""
预加载相关的实验和库文件程序。从各个工程项目预加载相关的功能库文件到引擎当中，用于后续开发、实验、运行等工作。
"""
from engine.externals import warnings, logging, platform, deepcopy, os, Path, timeit, sys, sqlite3, base64, pickle, multiprocessing, Pool, json, np, pd


def main(gb):
    """
    预加载相关的实验和库文件程序。从各个工程项目预加载相关的功能库文件到引擎当中，用于后续开发、实验、运行等工作。  #TODO 暂时还没有开发完成、引入使用。
    """
    # # %% 设置工作目录。 #FIXME #TODO
    # # folderpath_settings=Tools.setup_working_directory()
    # if Path(sys.argv[0]).name == Path(__file__).name:
    #     # 在控制台运行，切换到脚本所在的文件夹
    #     folderpath = Path(__file__).resolve().parent
    #     os.chdir(folderpath)
    # else:
    #     # 通过其他脚本运行，执行特定的代码
    #     list_args = Tools.decode_args([*sys.argv[1:]])
    #     folderpath = list_args[0]
    #     pass  # if
    #
    # # folderpath_parameters = folderpath


if __name__ == '__main__':
    # 从命令行参数获取配置字典
    globals_base64 = sys.argv[1]
    globals_pkl = base64.b64decode(globals_base64)
    gb = pickle.loads(globals_pkl)

    main(gb)

