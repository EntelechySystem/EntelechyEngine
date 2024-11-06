"""
实验组模拟程序。用于运行实验组。

#BUG 如果运行的文件批量太大，可能存在内存泄露的问题。建议每次运行的文件批量不要超过 10000 个。
"""
from engine.core.collector import Collector
# -*- coding: utf-8 -*-


from engine.externals import warnings, logging, platform, deepcopy, os, Path, timeit, sys, sqlite3, base64, pickle, multiprocessing, Pool, json, np, pd
from engine.tools.DataManageTools import DataManageTools
from engine.tools.Tools import Tools


def main(gb):
    """
    实验组模拟程序。用于运行实验组。
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

    # %% 预安装系统、数据，运行实验组

    # # 设置主进程日志
    # logger = logging.getLogger()
    # logger.setLevel(int(gb['test_logging']))
    # log_file_handler = logging.FileHandler(Path(gb['folderpath_experiments_output_log'], "outputlog.txt"))
    # logger.addHandler(log_file_handler)
    # log_console_handler = logging.StreamHandler()
    # logger.addHandler(log_console_handler)

    # %% 预安装系统、数据，运行实验组

    if gb['is_ignore_warning']:
        warnings.filterwarnings("ignore")  # 忽略警告

    # 初始化、构建、安装系统

    # 读取设置文件为字典
    settings = DataManageTools.load_PKLs_to_DataFrames(Path(gb['folderpath_engine'], r"engine/libraries/Settings"))
    gb.update(settings)  # 将 settings 字典中的内容更新到 gb 字典中

    # 设置参数作业列表
    with open(Path(gb['folderpath_experiments_output_parameters'], "parameters_works.pkl"), 'rb') as f:
        parameters_works = pd.read_pickle(f)
        num_parameters_works = len(parameters_works)
        # SQLite 数据库统计实验组之上一次的作业之完成情况
        time_start_统计实验组作业情况 = timeit.default_timer()  # #DEBUG
        # 如果参数库当中的参数文件夹中的参数文件有更新，那么就要在后续删除原有的作业数据库再重建
        if os.path.exists(Path(gb['folderpath_experiments_output_log'], "experiments_works_status.db")):
            is_exist_experiments_works_status_db = True
            mtime_of_file_parameters_pkl = Path(gb['folderpath_parameters'], "parameters.pkl").resolve().stat().st_mtime
            mtime_of_file_experimentsWorksStatus_db = Path(gb['folderpath_experiments_output_log'], "experiments_works_status.db").resolve().stat().st_mtime
            if mtime_of_file_parameters_pkl > mtime_of_file_experimentsWorksStatus_db:
                is_mtime_of_file_parameters_pkl_changed = True
            else:
                is_mtime_of_file_parameters_pkl_changed = False
                pass  # if
        else:
            is_exist_experiments_works_status_db = False
            is_mtime_of_file_parameters_pkl_changed = True
            pass  # if

        if gb['is_rerun_all_done_works_in_the_same_experiments'] or is_mtime_of_file_parameters_pkl_changed:
            is_recreate_experiments_works_status_db = True
            if is_exist_experiments_works_status_db:
                is_remove_experiments_works_status_db = True
            else:
                is_remove_experiments_works_status_db = False
                pass  # if
        else:
            is_recreate_experiments_works_status_db = False
            is_remove_experiments_works_status_db = False
            pass  # if

        if is_remove_experiments_works_status_db:
            os.remove(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
            pass  # if

        if is_recreate_experiments_works_status_db:  # 创建数据库并初始化表格
            conn = sqlite3.connect(Path(gb['folderpath_experiments_output_log'], "experiments_works_status.db"))
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS experiments
                            (id INTEGER PRIMARY KEY, status_实验组模拟程序 TEXT)""")
            # 根据实验组总数量，生成实验组作业状态信息。其中，所有实验组作业状态为 "RAW"
            for i in range(1, num_parameters_works + 1):
                c.execute("INSERT INTO experiments (id, status_实验组模拟程序) VALUES (?, ?)", (i, "RAW"))
                pass  # for
            conn.commit()
        else:
            # 连接现有数据库
            conn = sqlite3.connect(Path(gb['folderpath_experiments_output_log'], "experiments_works_status.db"))
            c = conn.cursor()
            if gb['is_rerun_all_done_works_in_the_same_experiments']:
                c.execute("UPDATE experiments SET status_实验组模拟程序 = 'RAW'")
                conn.commit()
                pass  # if
            pass  # if
        # 检查实验组作业完成状态
        c.execute("SELECT id, status_实验组模拟程序 FROM experiments")
        rows = c.fetchall()
        list_idsExp_DOING = []
        list_idsExp_DONE = []
        list_idsExp_RAW = []
        for row in rows:
            exp_id, status_实验组模拟程序 = row[0], row[1]
            if status_实验组模拟程序 == "DOING":
                list_idsExp_DOING.append(exp_id)
            elif status_实验组模拟程序 == "DONE":
                list_idsExp_DONE.append(exp_id)
            else:
                list_idsExp_RAW.append(exp_id)
                pass  # if
            pass  # for

        list_idsExp_PLAN = gb['list_idsExperiment_to_run'] if len(gb['list_idsExperiment_to_run']) != 0 else list(range(1, num_parameters_works + 1))
        list_idsExp_TASK = [i for i in list_idsExp_PLAN if i not in list_idsExp_DONE]
        # 保存实验组作业完成状态信息
        with open(Path(gb['folderpath_experiments_output_log'], "outputlog_worksStatesBeforeThisExperiments.json"), 'w') as f:
            json.dump({
                "计划运行的实验组 id": list_idsExp_TASK,
                "未运行过的实验组 id": list_idsExp_RAW,
                "之前运行中被中断的实验组 id": list_idsExp_DOING,
                "已完成的实验组 id": list_idsExp_DONE,
                "完成率": len(list_idsExp_DONE) / num_parameters_works,
                "中断率": len(list_idsExp_DOING) / num_parameters_works,
            }, f)
            logging.info("实验组开始运行前，实验组作业完成状态情况如下:\n" + str({
                "之前运行中被中断的实验组 id": list_idsExp_DOING,
                "完成率": len(list_idsExp_DONE) / num_parameters_works,
                "中断率": len(list_idsExp_DOING) / num_parameters_works,
            }))
            pass  # with

        # 绘制色带分布图，展示实验组 id 分布对应的实验组作业运行之前的作业完成状态信息。#BUG 如果实验组很多，那么绘制图像会占用大量的内存与时间！可以考虑注释不运行这段。
        # ids = [row[0] for row in rows]  # 获取实验组 id
        # status_实验组模拟程序_运行状态 = [row[1] for row in rows]  # 获取实验组作业状态
        # Tools.draw_color_band_before_experiments(ids, status_实验组模拟程序_运行状态, list_idsExp_PLAN, list_idsExp_TASK, Path(gb['folderpath_experiments_output_log'], "color_band_distribution_before_实验组模拟程序.png"))

        time_end_统计实验组作业情况 = timeit.default_timer()  # #DEBUG
        logging.info(f"统计参数数据完成，用时：{time_end_统计实验组作业情况 - time_start_统计实验组作业情况} 秒。")  # #DEBUG

        conn.close()  # 关闭数据库连接
        pass  # with

    # # 导出控制参数数据
    # Collector.export_parameter_data(gb, parameters_works)

    gb['len_parameters_works'] = num_parameters_works

    # 导入本次实验所需的系统


    if not (gb['is_develop_mode'] and gb['is_maintain_files_in_simulator_when_develop_mode']):
        # 如果是应用实验状态，则复制系统到输出文件夹下，另外导出一份到`engine/system`文件夹下
        Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_system'], is_auto_confirmation=gb['is_auto_confirmation'])
        Tools.copy_files_from_other_folders(gb['folderpath_system'], gb['folderpath_experiments_output_system'], is_auto_confirmation=gb['is_auto_confirmation'])
        Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], "engine/libraries/system"), is_auto_confirmation=gb['is_auto_confirmation'])
        Tools.copy_files_from_other_folders(gb['folderpath_system'], Path(gb['folderpath_engine'], "engine/libraries/system"), is_auto_confirmation=gb['is_auto_confirmation'])
    else:
        pass  # if

    # 导入系统集合
    # Builder.build_entities_by_execute(gb)
    systems = Tools.import_modules_from_package(str(Path(gb['folderpath_engine'], r'engine/libraries/system/content')), r"[Ss]ystem", gb['folderpath_engine'])

    # 导出配置数据
    Collector.export_config_data(gb)

    # 运行实验组
    logging.info("\n\n\n实验组开始：\n\n")

    gb['experiments_running_time'] = 0  # 初始化实验组运行总时长
    gb['export_data_running_time'] = 0  # 初始化导出数据运行总时长

    system = list(systems.values())[0]  # 获取当前实验对应的系统。如果一次批处理只有一个系统，那么就用这个。

    # # 连接实验组作业管理数据库
    # conn = sqlite3.connect(Path(gb['folderpath_experiments_output_log'], "experiments_works_status.db"))
    # c = conn.cursor()
    # c.execute("SELECT id,status FROM experiments WHERE status='TASK'")
    # rows = c.fetchall()
    # list_idsExp_TASK = [row[0] for row in rows]  # 获取实际上需要运行的实验组 id 列表
    parameters_works_TASK = parameters_works[parameters_works['exp_id'].isin(list_idsExp_TASK)]  # 获取实际上需要运行的实验组参数作业数据框

    if gb['is_enable_multiprocessing']:
        # ## #NOTE：多进程并行处理 #TODO等到后续需要的时候再进行适配
        # # para = para.to_dict()  # 将参数数据框转换为字典
        # # system = systems[f"system_{para['system_name']}"]  # 获取当前实验对应的系统。如果一次批处理不止一个系统，那么就用这个。
        #
        # ## 并行计算时，关闭主进程日志记录器，改由子进程记录各自的日志
        # log_file_handler.close()
        # logger.removeHandler(log_file_handler)
        #
        # num_cores = int(multiprocessing.cpu_count() * gb['percent_core_for_multiprocessing'])  # 计算 CPU 核心数
        #
        # ## 生成作业组
        # # gb['id_experiment'] = 0  # 设定当前实验编号
        # works = []
        # for i, para in parameters_works_TASK.iterrows():
        #     exp_id = int(parameters_works_TASK.loc[i, 'exp_id'])  # 获取当前实验编号
        #     work = (exp_id, gb, para, system)
        #     works.append(work)
        #     pass  # for
        #
        # ## 并行运行实验作业
        # with Pool(num_cores) as p:
        #     p.starmap(fun_single_experiment_work, works)
        #     pass  # with
        #
        # ## 并行处理之后，读取各个实验日志文件之内容追加到主进程日志文件之内容
        # if gb['is_enable_multiprocessing']:
        #     with open(Path(gb['folderpath_experiments_output_log'], "outputlog.txt"), 'a') as f:
        #         for i, para in parameters_works_TASK.iterrows():
        #             if Path(gb['folderpath_experiments_output_log'], f"outputlog_{i + 1}_exp.txt").exists():
        #                 with open(Path(gb['folderpath_experiments_output_log'], f"outputlog_{i + 1}_exp.txt"), 'r') as f_sub:
        #                     f.write(f_sub.read())
        #                     pass  # with
        #                 pass  # if
        #             pass  # for
        #         pass  # with
        #     pass  # if
        pass

    else:
        # NOTE：串行处理

        gb['simulator_start_time'] = timeit.default_timer()  # 记录串行运行模式下，模拟器开始运行时刻

        for i, para in parameters_works_TASK.iterrows():
            para = para.to_dict()  # 将参数数据框转换为字典
            # system = systems[f"system_{para['system_name']}"]  # 获取当前实验对应的系统。如果一次批处理不止一个系统，那么就用这个。
            system = list(systems.values())[0]  # 获取当前实验对应的系统。如果一次批处理只有一个系统，那么就用这个。
            gb['id_experiment'] = i + 1  # 设定当前实验编号

            # 运行一次实验作业
            fun_single_experiment_work(gb['id_experiment'], gb, para, system)
            pass  # for

        gb['simulator_end_time'] = timeit.default_timer()  # 记录串行运行模式下，记录模拟器结束运行时刻
        gb['simulator_running_time'] = gb['simulator_end_time'] - gb['simulator_start_time']  # 记录串行运行模式下，模拟器运行时长

        logging.info(f"实验组结束。\n实验组运行总时长：{gb['experiments_running_time']} 秒。\n导出数据运行总时长：{gb['export_data_running_time']} 秒。\n模拟器运行总时长：{gb['simulator_running_time']}秒。")

        # 默认程序打开输出文件查看
        if gb['is_auto_open_outputlog']:
            system = platform.system()
            if system == 'Darwin':
                os.system(r"open " + str(Path(gb['folderpath_experiments_output_log'], r"outputlog.txt")))
            elif system == 'Windows':
                os.startfile(str(Path(gb['folderpath_experiments_output_log'], r"outputlog.txt")))
            elif system == 'Linux':
                os.system('xdg-open ' + str(Path(gb['folderpath_experiments_output_log'], r"outputlog.txt")))  # #BUG 还没测试过
            else:
                print("Unsupported operating system")
                pass  # if
            pass  # if

        if gb['is_ignore_warning']:
            warnings.filterwarnings("default")  # 恢复警告
            pass  # if

        # ## 关闭日志
        # log_file_handler.close()
        # logger.removeHandler(log_file_handler)
        # log_console_handler.close()
        # logger.removeHandler(log_console_handler)

        pass  # if

    # 连接 SQLite 数据库，统计实验组之本次作业之完成情况
    num_parameters_works = len(parameters_works)
    time_start_统计实验组作业情况 = timeit.default_timer()  # #DEBUG
    conn = sqlite3.connect(Path(gb['folderpath_experiments_output_log'], "experiments_works_status.db"))
    c = conn.cursor()
    # 检查实验组作业完成状态
    c.execute("SELECT id, status_实验组模拟程序 FROM experiments")
    rows = c.fetchall()
    list_idsExp_DOING = []
    list_idsExp_DONE = []
    list_idsExp_RAW = []
    for row in rows:
        exp_id, status_实验组模拟程序 = row
        if status_实验组模拟程序 == "DOING":
            list_idsExp_DOING.append(exp_id)
        elif status_实验组模拟程序 == "DONE":
            list_idsExp_DONE.append(exp_id)
        else:
            list_idsExp_RAW.append(exp_id)
            pass  # if
        pass  # for
    # 保存实验组作业完成状态信息
    with open(Path(gb['folderpath_experiments_output_log'], "outputlog_worksStatesBeforeThisExperiments.json"), 'w') as f:
        json.dump({
            "计划运行的实验组 id": list_idsExp_TASK,
            "未运行过的实验组 id": list_idsExp_RAW,
            "之前运行中被中断的实验组 id": list_idsExp_DOING,
            "已完成的实验组 id": list_idsExp_DONE,
            "完成率": len(list_idsExp_DONE) / num_parameters_works,
            "中断率": len(list_idsExp_DOING) / num_parameters_works,
        }, f)
        logging.info("实验组开始运行前，实验组作业完成状态情况如下:\n" + str({
            "之前运行中被中断的实验组 id": list_idsExp_DOING,
            "完成率": len(list_idsExp_DONE) / num_parameters_works,
            "中断率": len(list_idsExp_DOING) / num_parameters_works,
        }))
        pass  # with

    # 绘制色带分布图，展示实验组 id 分布对应的实验组作业运行之后的作业完成状态信息。#BUG 如果实验组很多，那么绘制图像会占用大量的内存与时间！可以考虑注释不运行这段。
    # ids = [row[0] for row in rows]  # 获取实验组 id
    # status_实验组模拟程序_运行状态 = [row[1] for row in rows]  # 获取实验组作业状态
    # Tools.draw_color_band_after_experiments(ids, status_实验组模拟程序_运行状态, Path(gb['folderpath_experiments_output_log'], "color_band_distribution_after_实验组模拟程序.png"))

    time_end_统计实验组作业情况 = timeit.default_timer()  # #DEBUG
    logging.info(f"统计参数数据完成，用时：{time_end_统计实验组作业情况 - time_start_统计实验组作业情况} 秒。")  # #DEBUG

    conn.close()  # 关闭数据库连接

    pass  # main


def fun_single_experiment_work(exp_id: int, globals_original: dict, para, system: dict):
    """
    实验模拟程序。用于运行单个实验。

    Args:
        exp_id (int): 实验编号
        gb (dict): 模拟器全局变量（原始的）
        para (pandas.Series): 实验参数
        system (dict): 系统

    Returns:
        None
    """
    gb = deepcopy(globals_original)  # 复制全局变量，保证不同实验的全局变量的独立性
    gb['id_experiment'] = exp_id  # 设定当前实验编号

    # 运行系统
    system(para, gb)

    pass  # function


if __name__ == '__main__':
    # 从命令行参数获取配置字典
    globals_base64 = sys.argv[1]
    globals_pkl = base64.b64decode(globals_base64)
    gb = pickle.loads(globals_pkl)

    main(gb)
