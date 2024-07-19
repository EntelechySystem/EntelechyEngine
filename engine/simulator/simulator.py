"""
该文件是模拟器的入口文件
"""


def simulator(config: dict):
    """
    Python 版本模拟器入口

    Args:
        config (dict): 配置项

    Returns:
        None

    """

    # global config, para

    # %% 首先导入相关包
    from engine import os, platform, logging, Path, shutil, datetime, time, subprocess, pickle, base64, deepcopy
    from engine.tools.Tools import Tools
    from engine.tools.DataManageTools import DataManageTools

    # %% 初始化
    ## 获取项目路径、模拟器工具路径
    config['folderpath_project'] = Tools.get_project_rootpath()
    config['folderpath_engine'] = Tools.get_project_rootpath(config['foldername_engine'], config['folderpath_relpath_engine'])

    # # %% 由本模拟器复制一份完整的模拟器工程文件夹到项目文件夹中使用 ！HACK 这个很危险，容易删除模拟器工程文件夹！需要谨慎使用！
    # Tools._delete_and_recreate_folder(Path(config['folderpath_project'], r"Engine"), is_auto_confirmation=config['is_auto_confirmation'])
    # Tools._copy_files_from_other_folders(Path(config['folderpath_engine'], r"Engine"), Path(config['folderpath_project'], r"Engine"), is_auto_confirmation=config['is_auto_confirmation'])

    # %% 读写文件夹：如果 Library 之 Config 有内容，那么就删除，否则就从其他文件夹中复制之后再导入
    # Tools._delete_and_recreate_folder(Path(config['folderpath_engine'], r"engine/data/Config").resolve(), is_auto_confirmation=config['is_auto_confirmation'])
    # Tools._copy_files_from_other_folders(Path(config['folderpath_project'], config['folderpath_config']), Path(config['folderpath_engine'], "engine/data/Config").resolve(), is_auto_confirmation=config['is_auto_confirmation'])

    # # %% 运行配置程序
    # Tools.run_python_program_file(Path(config['folderpath_engine'], r"engine/data/Config/config.py").resolve(), [Path(config['folderpath_engine'], r"engine/data/Config").resolve()])

    ## 读取配置文件为字典
    with open(Path(config['folderpath_project'],config['folderpath_config'], r"config.pkl").resolve(), 'rb') as f:
        config = pickle.load(f)

    ## config 赋值给全局变量 globals
    globals = dict()
    globals.update(config)

    ## 设置相关的实验文件夹名称
    # if globals['schedule_operation']['实验组模拟程序'] is True:
    # pass  # if
    globals['foldername_experiments_output'] = Tools.set_foldername_experiments(globals['foldername_prefix_experiments'], globals['foldername_set_manually'], globals['is_datetime'], globals['type_of_experiments_foldername'])

    ## 生成实验相关的文件夹用于本批次运作
    (
        globals['folderpath_project'],
        globals['folderpath_engine'],
        globals['folderpath_experiments_projects'],
        globals['folderpath_experiments_output'],
        globals['folderpath_experiments_output_data'],
        globals['folderpath_experiments_output_log'],
        globals['folderpath_experiments_output_config'],
        globals['folderpath_experiments_output_settings'],
        globals['folderpath_experiments_output_parameters'],
        globals['folderpath_experiments_output_agents'],
        globals['folderpath_experiments_output_models'],
        globals['folderpath_models'],
        globals['folderpath_config'],
        globals['folderpath_settings'],
        globals['folderpath_parameters'],
        globals['folderpath_agents'],
    ) = Tools.set_experiments_folders(
        foldername_experiments_output_data=globals['foldername_experiments_output_data'],
        foldername_experiments_output=globals['foldername_experiments_output'],
        str_folderpath_experiments_projects=globals['folderpath_experiments_projects'],
        str_folderpath_root_experiments_output=globals['folderpath_root_experiments'],
        str_foldername_engine=globals['foldername_engine'],
        str_folderpath_relpath_engine=globals['folderpath_relpath_engine'],
        str_foldername_outputData=globals['foldername_outputData'],
        str_folderpath_relpath_outputData=globals['folderpath_relpath_outputData'],
        str_folderpath_models=globals['folderpath_models'],
        str_folderpath_config=globals['folderpath_config'],
        str_folderpath_settings=globals['folderpath_settings'],
        str_folderpath_parameters=globals['folderpath_parameters'],
        str_folderpath_agents=globals['folderpath_agents'],
    )


    # # %% 运行配置程序
    # Tools.run_python_program_file(Path(globals['folderpath_engine'], r"engine/data/settings/settings.py").resolve(), [Path(globals['folderpath_engine'], r"engine/data/settings").resolve()])

    # ## 读取设置文件为字典
    # settings = DataManageTools.load_PKLs_to_DataFrames(Path(globals['folderpath_engine'], r"engine/data/settings"))

    # globals.update(settings)  # 将 settings 字典中的内容更新到 globals 字典中

    ## 设置参数

    # # 如果参数库当中的参数文件夹中的参数文件有更新，那么就要在后续重新生成参数作业数据
    if Path(globals['folderpath_project'], globals['folderpath_parameters'], r"parameters.xlsx").resolve().exists():
        mtime_of_file_parameters_xlsx = Path(globals['folderpath_project'], globals['folderpath_parameters'], r"parameters.xlsx").resolve().stat().st_mtime
        mtime_of_file_parameters_py = Path(globals['folderpath_project'], globals['folderpath_parameters'], r"parameters.py").resolve().stat().st_mtime
        # filepath_parameters_works_pkl = Path(globals['folderpath_engine'], r"engine/data/parameters/parameters_works.pkl").resolve()
        filepath_parameters_works_pkl = Path(globals['folderpath_experiments_output_parameters'], r"parameters")
        if filepath_parameters_works_pkl.exists():
            # mtime_of_file_parameters_works_pkl = Path(globals['folderpath_engine'], r"engine/data/parameters/parameters_works.pkl").resolve().stat().st_mtime
            mtime_of_file_parameters_works_pkl = Path(globals['folderpath_experiments_output_parameters'], r"parameters").resolve().stat().st_mtime
            # if (mtime_of_file_parameters_xlsx > mtime_of_file_parameters_works_pkl or mtime_of_file_parameters_py > mtime_of_file_parameters_works_pkl) and globals['运行模式'] == '批量实验作业运行模式':
            if (mtime_of_file_parameters_xlsx > mtime_of_file_parameters_works_pkl or mtime_of_file_parameters_py > mtime_of_file_parameters_works_pkl):
                is_generate_parameters_works_data = True
                print("参数文件有更新，需要重新生成参数作业数据。")
            else:
                is_generate_parameters_works_data = False
                print("参数文件没有更新，不需要重新生成参数作业数据。")
                pass  # if
        else:
            is_generate_parameters_works_data = True
            print("参数作业数据文件不存在，需要重新生成参数作业数据。")
            pass  # if

        ## 运行参数作业程序
        if is_generate_parameters_works_data:
            ## 读写文件夹：如果 Library 之 Parameters 有内容，那么就删除，否则就从其他文件夹中复制之后再导入
            Tools._delete_and_recreate_folder(Path(globals['folderpath_experiments_output_parameters']), is_auto_confirmation=globals['is_auto_confirmation'])
            # Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"engine/data/parameters").resolve(), is_auto_confirmation=globals['is_auto_confirmation'])
            Tools._copy_files_from_other_folders(globals['folderpath_parameters'], globals['folderpath_experiments_output_parameters'], is_auto_confirmation=globals['is_auto_confirmation'])  # 导出一份到输出文件夹
            # Tools._copy_files_from_other_folders(Path(globals['folderpath_project'], globals['folderpath_parameters']), Path(globals['folderpath_engine'], "engine/data/parameters").resolve(), is_auto_confirmation=globals['is_auto_confirmation'])  # 复制一份到引擎临时数据文件夹   # #TODO 无用，可以删除
            ## 运行参数作业程序（#NOTE：可选）
            # Tools.run_python_program_file(Path(globals['folderpath_experiments_output_parameters'], r"parameters.py"), [globals['folderpath_experiments_output_parameters']])
            # Tools.run_python_program_file(Path(globals['folderpath_engine'], r"engine/data/parameters/parameters.py").resolve(), [Path(globals['folderpath_engine'], r"engine/data/parameters").resolve()])  # #TODO 无用，可以删除
            pass  # if

        ## 读取参数作业数据
        dict_parameters_works = DataManageTools.load_PKLs_to_DataFrames(globals['folderpath_experiments_output_parameters'])
        # dict_parameters_works = DataManageTools.load_PKLs_to_DataFrames(Path(globals['folderpath_engine'], r"engine/data/parameters"))
        parameters_works = dict_parameters_works['parameters_works']

        ## 导出参数作业信息为 PKL 文件
        with open(Path(globals['folderpath_experiments_output_parameters'], r"parameters_works.pkl").resolve(), 'wb') as f:
            pickle.dump(parameters_works, f)  # 导出一份到输出文件夹
            pass  # with
        # with open(Path(globals['folderpath_engine'], r"engine/data/parameters/parameters_works.pkl").resolve(), 'wb') as f:
        #     pickle.dump(parameters_works, f)  # 导出一份到模拟器库文件夹
        #     pass  # with

        ## 导出参数作业信息为 xlsx 文件
        with open(Path(globals['folderpath_experiments_output_parameters'], r"parameters_works.xlsx").resolve(), 'wb') as f:
            parameters_works.to_excel(f, index=False)
            pass  # with
        # with open(Path(globals['folderpath_engine'], r"engine/data/parameters/parameters_works.xlsx").resolve(), 'wb') as f:
        #     parameters_works.to_excel(f, index=False)
        #     pass  # with
        globals['num_parameters_works'] = parameters_works.shape[0]

        # globals.update(parameters_works)  # 将 parameters 字典中的内容更新到 globals 字典中

        pass  # if

    Tools.flatten_dict(globals, 1)  # 将 globals 字典中的内容扁平化

    ## 导出全局变量 globals 字典为 PKL 文件
    globals_expert = deepcopy(globals)
    Tools.transform_all_Path_value_to_string(globals_expert)  # 转换字典里所有 Path 对象为字符串。
    Tools._delete_and_recreate_folder(globals['folderpath_experiments_output_config'], is_auto_confirmation=globals['is_auto_confirmation'])
    # Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"engine/data/globals").resolve(), is_auto_confirmation=globals['is_auto_confirmation'])
    with open(Path(globals['folderpath_experiments_output_config'], r"globals.pkl").resolve(), 'wb') as f:
        pickle.dump(globals_expert, f)  # 导出一份到输出文件夹
        pass  # with
    # with open(Path(globals['folderpath_engine'], r"engine/data/globals/globals.pkl").resolve(), 'wb') as f:
    #     pickle.dump(globals_expert, f)  # 导出一份到模拟器库文件夹
    #     pass  # with

    # %% 是否运作模拟程序
    if globals['program_实验组模拟程序']:
        ## 导入相关数据
        Tools._delete_and_recreate_folder(globals['folderpath_experiments_output_config'], is_auto_confirmation=globals['is_auto_confirmation'])
        Tools._copy_files_from_other_folders(globals['folderpath_config'], globals['folderpath_experiments_output_config'], is_auto_confirmation=globals['is_auto_confirmation'])  

        Tools._delete_and_recreate_folder(globals['folderpath_experiments_output_settings'], is_auto_confirmation=globals['is_auto_confirmation'])
        # Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"Engine/data/settings").resolve(), is_auto_confirmation=globals['is_auto_confirmation'])
        # Tools._copy_files_from_other_folders(Path(globals['folderpath_project'], globals['folderpath_settings']), Path(globals['folderpath_engine'], "Engine/data/settings").resolve(), is_auto_confirmation=globals['is_auto_confirmation'])
        Tools._copy_files_from_other_folders(globals['folderpath_agents'], globals['folderpath_experiments_output_settings'], is_auto_confirmation=globals['is_auto_confirmation'])  

        Tools._delete_and_recreate_folder(globals['folderpath_experiments_output_parameters'], is_auto_confirmation=globals['is_auto_confirmation'])
        # Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"engine/data/Parameters"), is_auto_confirmation=globals['is_auto_confirmation'])
        # Tools._copy_files_from_other_folders(globals['folderpath_parameters'], Path(globals['folderpath_engine'], r"engine/data/Parameters"), is_auto_confirmation=globals['is_auto_confirmation'])
        Tools._copy_files_from_other_folders(globals['folderpath_parameters'], globals['folderpath_experiments_output_parameters'], is_auto_confirmation=globals['is_auto_confirmation'])  # 导出一份到输出文件夹
        # shutil.copy(Path(globals['folderpath_parameters'], r"set_parameters_variables.py"), globals['folderpath_experiments_output_parameters'])  # 导出一份生成参数的代码文件到输出文件夹

        Tools._delete_and_recreate_folder(globals['folderpath_experiments_output_agents'], is_auto_confirmation=globals['is_auto_confirmation'])
        # Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"engine/data/agents"), is_auto_confirmation=globals['is_auto_confirmation'])
        # Tools._copy_files_from_other_folders(globals['folderpath_agents'], Path(globals['folderpath_engine'], r"engine/data/agents"), is_auto_confirmation=globals['is_auto_confirmation'])
        Tools._copy_files_from_other_folders(globals['folderpath_agents'], globals['folderpath_experiments_output_agents'], is_auto_confirmation=globals['is_auto_confirmation'])  # 导出一份到输出文件夹
        # from Engine.core.define.define_agentsVariables import dict_agent, dict_interagent

        ## 获取一些系统信息
        globals['system_platform'] = platform.system()

        ## 设置日志
        logger = logging.getLogger()
        logger.setLevel(int(globals['test_logging']))
        if Path(globals['folderpath_experiments_output_log'], "outputlog.txt").exists():
            os.remove(Path(globals['folderpath_experiments_output_log'], "outputlog.txt"))  # 如果原来的日志存在，那么就删除重建
            pass  # if
        log_file_handler = logging.FileHandler(Path(globals['folderpath_experiments_output_log'], "outputlog.txt"))
        logger.addHandler(log_file_handler)
        log_console_handler = logging.StreamHandler()
        logger.addHandler(log_console_handler)

        if globals['is_develope_model']:
            logging.info("\n------------ 开发与调试模式！ ---------------\n")
            pass  # if

        logging.info("\n开始记录时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        logging.info("\n实验组名称：" + globals['foldername_experiments_output'] + "\n")
        logging.info("\n模拟器 simulator 版本：" + globals['engine_version'] + "\n")
        logging.info("\n相关实验配置项 globals 文件夹：" + globals['folderpath_config'].name + "\n")
        logging.info("\n相关实验 models 文件夹：" + globals['folderpath_models'].name + "\n")
        # logging.info("\n相关实验 agents 数据文件夹：" + globals['folderpath_agents'].name + "\n")
        logging.info("\n相关实验 settings 文件夹：" + globals['folderpath_settings'].name + "\n")
        logging.info("\n相关实验数据 experiments output data 文件夹：" + globals['folderpath_experiments_output'].name + "\n")
        logging.info("\n相关实验参数 parameters 文件夹：" + globals['folderpath_parameters'].name + "\n")

        ## 部署「运行实验组模拟程序」之相关配置项、文件夹

        # 遍历实验参数作业
        for i in range(globals['num_parameters_works']):
            # 读取一行参数作业数据
            work = parameters_works.iloc[i]
            # 生成每个作业实验之文件夹、文件名（不含后缀名）为作业表的 id 列值（用 0 补齐缺的位数）
            foldername_experiment = str(work['id']).zfill(len(str(len(parameters_works))))
            filename_experiment_prefix = str(work['id']).zfill(len(str(len(parameters_works))))
            filename_experiment_globals = filename_experiment_prefix + "_globals.pkl"
            filename_experiment_parameters_work = filename_experiment_prefix + "_parameters_work.pkl"

            folderpath_experiment = Path(globals['folderpath_experiments_output_data'], foldername_experiment).resolve()  # 生成每个作业实验文件夹路径
            # 从无到有创建每个作业实验文件夹
            folderpath_experiment.mkdir(parents=True, exist_ok=False)
            # 在实验输出数据文件夹中生成每个作业实验的 globals.pkl 文件、parameters_work.pkl 文件
            with open(Path(globals['folderpath_experiments_output_data'], filename_experiment_globals).resolve(), 'wb') as f:
                pickle.dump(globals, f)  # 保存每一个作业实验的 globals.pkl 文件
                pass  # with
            with open(Path(globals['folderpath_experiments_output_data'], filename_experiment_parameters_work).resolve(), 'wb') as f:
                pickle.dump(work, f)  # 保存每一个作业实验的 parameters_work.pkl 文件
                pass  # with
            pass  # for

        ## 运行实验组模拟程序
        if not globals['is_develope_mode']:
            sgv_pkl = pickle.dumps(globals)
            sgv_base64 = base64.b64encode(sgv_pkl).decode('utf-8')
            # para_pkl = pickle.dumps(para)
            # para_base64 = base64.b64encode(para_pkl).decode('utf-8')
            start_time = time.time()
            subprocess.run(["python", str(Path(globals['folderpath_simulator'], 'engine/programs/experiments_program.py')), sgv_base64])
            # subprocess.run(["python", str(Path(sgv['folderpath_simulator'], 'engine/programs/experiments_program.py')), sgv_base64, para_base64])
        else:
            from engine.programs.experiments_program import main
            start_time = time.time()
            main(globals)
            pass  # if

        ## 关闭日志
        logger.removeHandler(log_file_handler)
        pass  # if

    # %% 是否可视化结果程序 #HACK 未开发
    if globals['program_可视化结果程序']:
        sgv_pkl = pickle.dumps(globals)
        sgv_base64 = base64.b64encode(sgv_pkl).decode('utf-8')
        start_time = time.time()
        subprocess.run(["python", str(Path(globals['folderpath_engine'], 'Data/programs/visualize_data_program.py')), sgv_base64])
        end_time = time.time()
        print(f"\n可视化数据运行总时长：{end_time - start_time} 秒。\n")
        pass  # if

    # # %% 清理 #HACK 未开发
    # ## 删除设置文件夹、模型文件夹内的所有文件，但是保留文件夹
    # Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"engine/data/Config"), is_auto_confirmation=globals['is_auto_confirmation'])
    # Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"engine/data/Parameters"), is_auto_confirmation=globals['is_auto_confirmation'])
    # Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"engine/data/agents"), is_auto_confirmation=globals['is_auto_confirmation'])
    # if not globals['is_develope_model']:
    #     Tools._delete_and_recreate_folder(Path(globals['folderpath_engine'], r"engine/data/Models"), is_auto_confirmation=globals['is_auto_confirmation'])
    #     pass  # if
