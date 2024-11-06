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
    from engine.core.define_engineGlobalVariables import gb

    # %% 初始化
    # 获取项目路径、模拟器工具路径
    config['folderpath_project'] = Tools.get_project_rootpath()
    config['folderpath_engine'] = Tools.get_project_rootpath(config['foldername_engine'], config['folderpath_relpath_engine'])

    # %% 运行配置程序
    if config['is_prerun_config_program']:
        result = Tools.run_python_program_file(Path(config['folderpath_project'], config['folderpath_config'], r"config_program.py").resolve(), [Path(config['folderpath_engine'], r"engine/libraries/Config").resolve()])

    # 读取配置文件为字典
    if config['is_prerun_config_program'] or config['is_use_xlsx_as_config_file']:
        is_load_config_from_pickle_file = True
        is_load_config_from_python_file = False
    else:
        is_load_config_from_pickle_file = False
        is_load_config_from_python_file = True
        pass  # if

    if is_load_config_from_pickle_file:
        with open(Path(config['folderpath_project'], config['folderpath_config'], r"config.pkl").resolve(), 'rb') as f:
            config = pickle.load(f)

    if is_load_config_from_python_file:
        config = (Tools.import_modules_from_package(str(Path(config['folderpath_project'], config['folderpath_config'])), r'config', config['folderpath_project']))['config']

    # config 赋值给全局变量 gb
    gb.update(config)

    # 设置相关的实验文件夹名称
    gb['foldername_experiments_output'] = Tools.set_foldername_experiments(gb['foldername_prefix_experiments'], gb['foldername_set_manually'], gb['is_datetime'], gb['type_of_experiments_foldername'])

    # 生成实验相关的文件夹用于本批次运作
    (
        gb['folderpath_project'],
        gb['folderpath_engine'],
        gb['folderpath_experiments_projects'],
        gb['folderpath_system'],
        gb['folderpath_config'],
        gb['folderpath_parameters'],
        gb['folderpath_models'],
        gb['folderpath_settings'],
        gb['folderpath_world_conception_knowledge'],
        gb['folderpath_world_environment'],
        gb['folderpath_agents'],
        gb['folderpath_data'],
        gb['folderpath_experiments_output'],
        gb['folderpath_experiments_output_data'],
        gb['folderpath_experiments_output_log'],
        gb['folderpath_experiments_output_system'],
        gb['folderpath_experiments_output_config'],
        gb['folderpath_experiments_output_parameters'],
        gb['folderpath_experiments_output_models'],
        gb['folderpath_experiments_output_settings'],
        gb['folderpath_experiments_output_world_conception_knowledge'],
        gb['folderpath_experiments_output_world_environment'],
        gb['folderpath_experiments_output_agents'],
    ) = (Tools.set_experiments_folders(
        str_folderpath_experiments_projects=gb['folderpath_experiments_projects'],
        str_folderpath_system=gb['folderpath_system'],
        str_folderpath_config=gb['folderpath_config'],
        str_folderpath_parameters=gb['folderpath_parameters'],
        str_foldername_engine=gb['foldername_engine'],
        str_folderpath_relpath_engine=gb['folderpath_relpath_engine'],
        str_folderpath_relpath_CIS=gb['folderpath_relpath_CIS'],
        str_folderpath_models=gb['folderpath_models'],
        str_folderpath_settings=gb['folderpath_settings'],
        str_folderpath_relpath_ECS=gb['folderpath_relpath_ECS'],
        str_folderpath_world_conception_knowledge=gb['folderpath_world_conception_knowledge'],
        str_folderpath_relpath_AWS=gb['folderpath_relpath_AWS'],
        str_folderpath_world_environment=gb['folderpath_world_environment'],
        str_folderpath_agents=gb['folderpath_agents'],
        str_folderpath_relpath_LMS=gb['folderpath_relpath_LMS'],
        str_folderpath_root_experiments_output=gb['folderpath_root_experiments'],
        str_folderpath_relpath_outputData=gb['folderpath_relpath_outputData'],
        str_foldername_outputData=gb['foldername_outputData'],
        foldername_experiments_output=gb['foldername_experiments_output'],
        foldername_experiments_output_data=gb['foldername_experiments_output_data']
    ))

    Tools.flatten_dict(gb, 1)  # 将 gb 字典中的内容扁平化

    # 导出全局变量 gb 字典为 PKL 文件
    globals_expert = deepcopy(gb)
    Tools.transform_all_Path_value_to_string(globals_expert)  # 转换字典里所有 Path 对象为字符串。
    Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_config'], is_auto_confirmation=gb['is_auto_confirmation'])
    with open(Path(gb['folderpath_experiments_output_config'], r"gb.pkl").resolve(), 'wb') as f:
        pickle.dump(globals_expert, f)  # 导出一份到输出文件夹
        pass  # with

    # %% 是否运作预加载相关的实验和库文件程序
    if gb['program_预加载相关的实验和库文件程序']:
        # 导入相关配置项
        Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_config'], is_auto_confirmation=gb['is_auto_confirmation'])
        Tools.copy_files_from_other_folders(gb['folderpath_config'], gb['folderpath_experiments_output_config'], is_auto_confirmation=gb['is_auto_confirmation'])
        Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], "engine/libraries/config"), is_auto_confirmation=config['is_auto_confirmation'])
        Tools.copy_files_from_other_folders(gb['folderpath_config'], Path(gb['folderpath_engine'], "engine/libraries/config"), is_auto_confirmation=gb['is_auto_confirmation'])

        # 导入智能模型（模型）
        if (gb['is_develop_mode'] and gb['is_maintain_files_in_simulator_when_develop_mode']):
            # 导入相关设置项
            Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_settings'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_settings'], gb['folderpath_experiments_output_settings'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/settings").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_settings'], Path(gb['folderpath_engine'], "engine/libraries/settings").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])

            # 如果是应用实验状态，则复制模型数据与内容到输出文件夹下，另外导出一份到`engine/models`文件夹下
            Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_models'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_models'], gb['folderpath_experiments_output_models'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], "engine/libraries/models"), is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_models'], Path(gb['folderpath_engine'], "engine/libraries/models"), is_auto_confirmation=gb['is_auto_confirmation'])

            # 导入相关个体众数据库
            Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_agents'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_agents'], gb['folderpath_experiments_output_agents'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/agents").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_agents'], Path(gb['folderpath_engine'], "engine/libraries/agents").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])

            # 导入相关世界环境模型
            Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_world_environment'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_world_environment'], gb['folderpath_experiments_output_world_environment'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/world_environment").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_world_environment'], Path(gb['folderpath_engine'], "engine/libraries/world_environment").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])

            # 导入相关世界概念知识模型
            Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_world_conception_knowledge'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_world_conception_knowledge'], gb['folderpath_experiments_output_world_conception_knowledge'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/world_conception_knowledge").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_world_conception_knowledge'], Path(gb['folderpath_engine'], "engine/libraries/world_conception_knowledge").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])

        else:
            pass  # if

        ## 运行预加载相关的实验和库文件程序。
        if not gb['is_develop_mode']:
            globals_pkl = pickle.dumps(gb)
            globals_base64 = base64.b64encode(globals_pkl).decode('utf-8')
            # para_pkl = pickle.dumps(para)
            # para_base64 = base64.b64encode(para_pkl).decode('utf-8')
            start_time = time.time()
            subprocess.run(["python", str(Path(gb['folderpath_agents'], 'engine/programs/preload_libraries_program.py')), globals_base64])
            # subprocess.run(["python", str(Path(gb['folderpath_agents'], 'engine/programs/preload_libraries_program.py')), globals_base64, para_base64])
        else:
            from engine.programs.preload_libraries_program import main
            start_time = time.time()
            main(gb)
            pass  # if

        pass  # if

    # %% 是否运作模拟程序
    if gb['program_实验组模拟程序']:
        # 导入相关配置项
        Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_config'], is_auto_confirmation=gb['is_auto_confirmation'])
        Tools.copy_files_from_other_folders(gb['folderpath_config'], gb['folderpath_experiments_output_config'], is_auto_confirmation=gb['is_auto_confirmation'])
        Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], "engine/libraries/config"), is_auto_confirmation=config['is_auto_confirmation'])
        Tools.copy_files_from_other_folders(gb['folderpath_config'], Path(gb['folderpath_engine'], "engine/libraries/config"), is_auto_confirmation=gb['is_auto_confirmation'])

        # 导入相关文件到实验台
        if not (gb['is_develop_mode'] and gb['is_maintain_files_in_simulator_when_develop_mode']):
            # 导入相关系统项
            Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_system'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_system'], gb['folderpath_experiments_output_system'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], "engine/libraries/system"), is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_system'], Path(gb['folderpath_engine'], "engine/libraries/system"), is_auto_confirmation=gb['is_auto_confirmation'])

            # 导入相关设置项
            Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_settings'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_settings'], gb['folderpath_experiments_output_settings'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/settings").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_settings'], Path(gb['folderpath_engine'], "engine/libraries/settings").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])

            # 如果是应用实验状态，则复制模型数据与内容到输出文件夹下，另外导出一份到`engine/models`文件夹下
            Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_models'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_models'], gb['folderpath_experiments_output_models'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], "engine/libraries/models"), is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_models'], Path(gb['folderpath_engine'], "engine/libraries/models"), is_auto_confirmation=gb['is_auto_confirmation'])

            # 导入相关个体众数据库
            Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_agents'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_agents'], gb['folderpath_experiments_output_agents'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/agents").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_agents'], Path(gb['folderpath_engine'], "engine/libraries/agents").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])

            # 导入相关世界环境模型
            Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_world_environment'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_world_environment'], gb['folderpath_experiments_output_world_environment'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/world_environment").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_world_environment'], Path(gb['folderpath_engine'], "engine/libraries/world_environment").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])

            # 导入相关世界概念知识模型
            Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_world_conception_knowledge'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_world_conception_knowledge'], gb['folderpath_experiments_output_world_conception_knowledge'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/world_conception_knowledge").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_world_conception_knowledge'], Path(gb['folderpath_engine'], "engine/libraries/world_conception_knowledge").resolve(), is_auto_confirmation=gb['is_auto_confirmation'])

        else:
            pass  # if

        # 获取一些系统信息
        gb['system_platform'] = platform.system()

        ## 设置日志
        if gb['is_rerun_all_done_works_in_the_same_experiments']:
            # 删除原有的主日志文件
            for file in Path(gb['folderpath_experiments_output_log']).glob("outputlog.txt"):
                file.unlink()
            # 删除原有的各子实验日志文件，但是保留作业状态标记日志文件。
            for file in Path(gb['folderpath_experiments_output_log']).glob("outputlog_*exp.txt"):
                file.unlink()
            pass  # if

        # 打开日志
        logger = logging.getLogger()
        logger.setLevel(int(gb['test_logging']))

        log_file_handler = logging.FileHandler(Path(gb['folderpath_experiments_output_log'], "outputlog.txt"))
        logger.addHandler(log_file_handler)
        log_console_handler = logging.StreamHandler()
        logger.addHandler(log_console_handler)

        if gb['is_develop_mode']:
            logging.info("\n------------ 开发与调试模式！ ---------------\n")
            pass  # if
        logging.info("\n开始记录时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        logging.info("\n实验组名称：" + gb['foldername_experiments_output'] + "\n")
        logging.info("\n引擎版本：" + gb['engine_version'] + "\n")
        logging.info("\n实验项目文件夹：" + gb['folderpath_project'].name + "\n")
        logging.info("\n相关系统文件夹：" + gb['folderpath_system'].name + "\n")
        logging.info("\n相关实验配置项文件夹：" + gb['folderpath_config'].name + "\n")
        logging.info("\n相关实验参数作业文件夹：" + gb['folderpath_parameters'].name + "\n")
        logging.info("\n相关实验智能模型文件夹：" + gb['folderpath_models'].name + "\n")
        logging.info("\n相关实验设置文件夹：" + gb['folderpath_settings'].name + "\n")
        logging.info("\n相关实验世界概念知识文件夹：" + gb['folderpath_world_conception_knowledge'].name + "\n")
        logging.info("\n相关实验世界环境文件夹：" + gb['folderpath_world_environment'].name + "\n")
        logging.info("\n相关实验智能体众数据文件夹：" + gb['folderpath_agents'].name + "\n")
        logging.info("\n相关实验结果数据文件夹：" + gb['folderpath_experiments_output'].name + "\n")

        # 部署「运行实验组模拟程序」之相关配置项、文件夹
        # 设置参数

        # # 如果参数库当中的参数文件夹中的参数文件有更新，那么就要在后续重新生成参数作业数据
        if Path(gb['folderpath_parameters'], r"parameters.xlsx").resolve().exists():
            mtime_of_file_parameters_xlsx = Path(gb['folderpath_project'], gb['folderpath_parameters'], r"parameters.xlsx").resolve().stat().st_mtime
            mtime_of_file_parameters_py = Path(gb['folderpath_project'], gb['folderpath_parameters'], r"parameters_program.py").resolve().stat().st_mtime  # #HACK 事实上现在还没有用到
            filepath_parameters_works_pkl = Path(gb['folderpath_experiments_output_parameters'], r"parameters")
            if filepath_parameters_works_pkl.exists():
                mtime_of_file_parameters_works_pkl = Path(gb['folderpath_experiments_output_parameters'], r"parameters").resolve().stat().st_mtime
                if (mtime_of_file_parameters_xlsx > mtime_of_file_parameters_works_pkl or mtime_of_file_parameters_py > mtime_of_file_parameters_works_pkl):
                    is_mtime_of_file_parameters_pkl_changed = True
                    logging.info("参数文件有更新。")
                else:
                    is_mtime_of_file_parameters_pkl_changed = False
                    logging.info("参数文件没有更新。")
                    pass  # if
            else:
                is_exist_experiments_works_status_db = False
                is_mtime_of_file_parameters_pkl_changed = True
                logging.info("参数作业数据文件不存在。")
                pass  # if
            pass  # if

        # 运行参数作业程序
        if is_mtime_of_file_parameters_pkl_changed:
            Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/parameters"), is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_parameters'], Path(gb['folderpath_engine'], r"engine/libraries/parameters"), is_auto_confirmation=gb['is_auto_confirmation'])

            if not gb['is_prerun_parameters_program']:  # 如果没有在实验主程序之前，预先运行了参数库相关的生成参数的程序，则运行生成参数的程序
                Tools.run_python_program_file(Path(gb['folderpath_engine'], r"engine/libraries/parameters", r"parameters.py"), [gb['folderpath_experiments_output_parameters']])  # 运行参数作业程序 #BUG 无法运行

            Tools.delete_and_recreate_folder(gb['folderpath_experiments_output_parameters'], is_auto_confirmation=gb['is_auto_confirmation'])
            Tools.copy_files_from_other_folders(gb['folderpath_parameters'], gb['folderpath_experiments_output_parameters'], is_auto_confirmation=gb['is_auto_confirmation'])
            pass  # if

        # 读取参数作业数据
        dict_parameters_works = DataManageTools.load_PKLs_to_DataFrames(gb['folderpath_experiments_output_parameters'])
        parameters_works = dict_parameters_works['parameters_works']

        # 导出参数作业信息为 PKL 文件
        with open(Path(gb['folderpath_experiments_output_parameters'], r"parameters_works.pkl").resolve(), 'wb') as f:
            pickle.dump(parameters_works, f)  # 导出一份到输出文件夹
            pass  # with
        # with open(Path(gb['folderpath_engine'], r"engine/libraries/parameters/parameters_works.pkl").resolve(), 'wb') as f:
        #     pickle.dump(parameters_works, f)  # 导出一份到模拟器库文件夹
        #     pass  # with

        # 导出参数作业信息为 xlsx 文件
        with open(Path(gb['folderpath_experiments_output_parameters'], r"parameters_works.xlsx").resolve(), 'wb') as f:
            parameters_works.to_excel(f, index=False)
            pass  # with
        gb['num_parameters_works'] = parameters_works.shape[0]

        # gb.update(parameters_works)  # 将 parameters 字典中的内容更新到 gb 字典中

        pass  # if

        # 遍历实验参数作业
        for i in range(gb['num_parameters_works']):
            # 读取一行参数作业数据
            work = parameters_works.iloc[i]
            # 生成每个作业实验之文件夹、文件名（不含后缀名）为作业表的 id 列值（用 0 补齐缺的位数）
            foldername_experiment = str(work['exp_id']).zfill(len(str(len(parameters_works))))
            filename_experiment_prefix = str(work['exp_id']).zfill(len(str(len(parameters_works))))
            filename_experiment_globals = filename_experiment_prefix + "_globals.pkl"
            filename_experiment_parameters_work = filename_experiment_prefix + "_parameters_work.pkl"

            folderpath_experiment = Path(gb['folderpath_experiments_output_data'], foldername_experiment).resolve()  # 生成每个作业实验文件夹路径
            # 从无到有创建每个作业实验文件夹
            folderpath_experiment.mkdir(parents=True, exist_ok=False)
            # 在实验输出数据文件夹中生成每个作业实验的 gb.pkl 文件、parameters_work.pkl 文件
            with open(Path(gb['folderpath_experiments_output_data'], filename_experiment_globals).resolve(), 'wb') as f:
                pickle.dump(gb, f)  # 保存每一个作业实验的 gb.pkl 文件
                pass  # with
            with open(Path(gb['folderpath_experiments_output_data'], filename_experiment_parameters_work).resolve(), 'wb') as f:
                pickle.dump(work, f)  # 保存每一个作业实验的 parameters_work.pkl 文件
                pass  # with
            pass  # for

        # # 关闭日志
        # log_file_handler.close()
        # logger.removeHandler(log_file_handler)
        # log_console_handler.close()
        # logger.removeHandler(log_console_handler)

        ## 运行实验组模拟程序
        if not gb['is_develop_mode']:
            globals_pkl = pickle.dumps(gb)
            globals_base64 = base64.b64encode(globals_pkl).decode('utf-8')
            # para_pkl = pickle.dumps(para)
            # para_base64 = base64.b64encode(para_pkl).decode('utf-8')
            start_time = time.time()
            subprocess.run(["python", str(Path(gb['folderpath_agents'], 'engine/programs/experiments_program.py')), globals_base64])
            # subprocess.run(["python", str(Path(gb['folderpath_agents'], 'engine/programs/experiments_program.py')), globals_base64, para_base64])
        else:
            from engine.programs.experiments_program import main
            start_time = time.time()
            main(gb)
            pass  # if

        # # 继续打开日志
        # logger.addHandler(log_file_handler)
        # logger.addHandler(log_console_handler)

        end_time = time.time()
        logging.info(f"\n模拟器运行时长：{end_time - start_time} 秒。\n")

        # 关闭日志
        log_file_handler.close()
        logger.removeHandler(log_file_handler)
        log_console_handler.close()
        logger.removeHandler(log_console_handler)

        pass  # if

    # %% 是否可视化结果程序 #HACK 未开发
    if gb['program_可视化结果程序']:
        globals_pkl = pickle.dumps(gb)
        globals_base64 = base64.b64encode(globals_pkl).decode('utf-8')
        start_time = time.time()
        subprocess.run(["python", str(Path(gb['folderpath_engine'], 'libraries/programs/visualize_data_program.py')), globals_base64])
        end_time = time.time()
        print(f"\n可视化数据运行总时长：{end_time - start_time} 秒。\n")
        pass  # if

    # %% 清理 #HACK 未开发
    ## 删除设置文件夹、模型文件夹内的所有文件，但是保留文件夹
    Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/config"), is_auto_confirmation=gb['is_auto_confirmation'])
    Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/parameters"), is_auto_confirmation=gb['is_auto_confirmation'])
    Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/agents"), is_auto_confirmation=gb['is_auto_confirmation'])
    Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/settings"), is_auto_confirmation=gb['is_auto_confirmation'])
    if not (gb['is_develop_mode'] and gb['is_maintain_files_in_simulator_when_develop_mode']):
        Tools.delete_and_recreate_folder(Path(gb['folderpath_engine'], r"engine/libraries/models"), is_auto_confirmation=gb['is_auto_confirmation'])
        pass  # if
