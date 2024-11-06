"""
收集数据
"""

import numpy as np

# from scipy.sparse import csr_array
from engine.externals import pickle, pd, Path, Optional, logging
# from engine.core.define_agentDataCollection import AgentDataCollection
# from engine.core.define.define_enum import ScheduleState
# from engine.core.define.define_type import *
from engine.tools import Tools

pass  # end import


class Collector:

    #
    # ## NOTE 当用 Pandas 之数据结构时：
    # @classmethod
    # def init_agent_data_collection(cls, A: pd.Series, gb: dict):
    #     """
    # 
    #     Args:
    #         A (pd.Series): 个体众
    #         gb (dict): 引擎全局变量
    # 
    #     Returns:
    #         A_data: 待收集的数据
    # 
    #     """
    # 
    #     ## 初始化数据框用以存储agent数据
    #     agent_data = pd.DataFrame()
    #     interagent_data = pd.DataFrame()
    #     A_data = AgentDataCollection(agent_data, interagent_data)
    # 
    #     # gb['series_agents'] = pd.Series()
    #     # for i in A.agents.index:
    #     #     gb['series_agents'][i] = A.agents[i].copy()
    #     # gb['df_agents'] = gb['series_agents'].to_frame().transpose()
    #     # gb['df_agents'].insert(loc=0, column='process_name', value=gb['process_name'])
    #     # gb['df_agents'].insert(loc=1, column='step', value=gb['step'])
    #     # gb['df_agents'].insert(loc=2, column='turn', value=gb['turn'])
    #     # gb['df_agents'].insert(loc=3, column='phase', value=gb['phase'])
    #     # # agent_data = pd.concat([agent_data, gb['df_agents']], ignore_index=True)
    #     # A_data.agents = pd.concat([A_data.agents, gb['df_agents']], ignore_index=True)
    #     #
    #     # gb['series_interagent'] = pd.Series()
    #     # for i in A.interagent.index:
    #     #     gb['series_interagent'][i] = A.interagent[i].copy()
    #     # gb['df_interagent'] = gb['series_interagent'].to_frame().transpose()
    #     # gb['df_interagent'].insert(loc=0, column='process_name', value=gb['process_name'])
    #     # gb['df_interagent'].insert(loc=1, column='step', value=gb['step'])
    #     # gb['df_interagent'].insert(loc=2, column='turn', value=gb['turn'])
    #     # gb['df_interagent'].insert(loc=3, column='phase', value=gb['phase'])
    #     # # interagent_data = pd.concat([interagent_data, gb['df_interagent']], ignore_index=True)
    #     # A_data.interagent = pd.concat([A_data.interagent, gb['df_interagent']], ignore_index=True)
    #     #
    #     # # A_data = pd.Series([agent_data, interagent_data], index=['agents', 'interagent'])
    # 
    #     return A_data
    #     pass  # function
    # 
    # @classmethod
    # def collect_agent_data(cls, A: Agents, A_data: AgentDataCollection, gb: dict):
    #     """
    #     收集数据并存储
    # 
    #     Args:
    #         A (Agents): 个体众
    #         A_data (AgentDataCollection): 个体众数据集
    #         gb: 引擎全局变量
    # 
    #     Returns:
    #         A_data: 待收集的数据
    # 
    #     """
    #     # agent_data, interagent_data = A_data.agents, A_data.interagent
    # 
    #     # agent_df = A.agents.to_frame().transpose()
    #     # agents = deepcopy(A.agents)
    #     # gb['series_agents'] = pd.Series()
    #     series_agents = pd.Series()
    #     for i in A.agents.index:
    #         series_agents[i] = A.agents[i].copy()
    #     df_agents = series_agents.to_frame().transpose()
    #     df_agents.insert(loc=0, column='process_name', value=gb['process_name'])
    #     df_agents.insert(loc=1, column='step', value=gb['step'])
    #     df_agents.insert(loc=2, column='turn', value=gb['turn'])
    #     df_agents.insert(loc=3, column='phase', value=gb['phase'])
    #     A_data.agents = pd.concat([A_data.agents, df_agents], ignore_index=True)
    #     # agent_data = pd.concat([agent_data, gb['df_agents']], ignore_index=True)
    # 
    #     # interagent_df = A.interagent.to_frame().transpose()
    #     # interagent = deepcopy(A.interagent)
    #     series_interagent = pd.Series()
    #     for i in A.interagent.index:
    #         series_interagent[i] = A.interagent[i].copy()
    #     df_interagent = series_interagent.to_frame().transpose()
    #     df_interagent.insert(loc=0, column='process_name', value=gb['process_name'])
    #     df_interagent.insert(loc=1, column='step', value=gb['step'])
    #     df_interagent.insert(loc=2, column='turn', value=gb['turn'])
    #     df_interagent.insert(loc=3, column='phase', value=gb['phase'])
    #     A_data.interagent = pd.concat([A_data.interagent, df_interagent], ignore_index=True)
    #     # interagent_data = pd.concat([interagent_data, interagent_df], ignore_index=True)
    # 
    #     # A_data.agents, A_data.interagent = agent_data, interagent_data
    #     # return A_data
    #     pass  # function
    # 
    # @classmethod
    # def export_agent_data(cls, A_data: AgentDataCollection, gb: dict):
    #     """
    #     HACK导出实验结果数据
    # 
    #     NOTE：查询列具有的数据类型可以用以下语句：
    # 
    #     ```python
    #     list_type_of_columns_01 = [A_data.agents[v].dtype for v in A_data.agents.columns]
    #     list_type_of_columns_02 = [A_data.agents[v][0].dtype for v in A_data.agents.columns]
    #     list_type_of_columns_01 = [A_data.interagent[v].dtype for v in A_data.interagent.columns]
    #     list_type_of_columns_02 = [A_data.interagent[v][0].dtype for v in A_data.interagent.columns]
    #     ```
    # 
    #     Args:
    #         A_data: 个体众数据集
    #         gb(dict): 引擎全局变量
    # 
    #     """
    # 
    #     ## 压缩数据
    #     if gb['is_compress_result_data']:
    #         A_data.agents, A_data.interagent = cls.compress_result_data(A_data.agents, A_data.interagent)
    #         pass  # if
    # 
    #     # # 解压数据 #DEBUG 以下用于测试解压后的数据是否与原始数据一致
    #     # if gb['is_compress_result_data']:
    #     #     agent_decompress, interagent_decompress = cls.decompress_result_data(A_data.agents, A_data.interagent)
    #     #     pass  # if
    #     #
    #     #     A_data.agents = agent_decompress
    #     #     A_data.interagent = interagent_decompress
    #     #     pass  # if
    #     # compare = []  # 验证解压后的数据是否与原始数据一致
    #     # for i in range(len(A_data.agents)):
    #     #     # compare.append(A_data.agents['Loss_t'][i] - agent_decompress['Loss_t'][i])
    #     #     compare.append(A_data.interagent['Shock_interagent_def'][i] - interagent_decompress['Shock_interagent_def'][i])
    #     #     # compare.append(A_data.agents['hel'][i] ^ agent_decompress['hel'][i])
    #     #     # compare.append(A_data.interagent['hel'][i] ^ interagent_decompress['hel'][i])
    # 
    #     ## 导出为pkl格式
    #     pd.to_pickle(A_data.agents, Path(gb['folderpath_experiments_output_data'], r"agent_exp=" + str(gb['id_experiment']) + r".pkl"))  # 导出为pkl格式
    #     pd.to_pickle(A_data.interagent, Path(gb['folderpath_experiments_output_data'], r"interagent_exp=" + str(gb['id_experiment']) + r".pkl"))  # 导出为pkl格式
    # 
    #     pass  # function
    # 
    # # ## NOTE 当用对象字段数据结构时：
    # # @classmethod
    # # def init_agent_data_collection(cls, A: Agents, gb: dict):
    # #     """
    # #
    # #     Args:
    # #         A (Agents): 个体众
    # #         gb (dict): 引擎全局变量
    # #
    # #     Returns:
    # #         A_data: 待收集的
    # #         数据
    # #
    # #     """
    # #     agent_data_item = dict(
    # #         {
    # #             list(gb.keys())[list(gb.keys()).index('process_name')]: gb['process_name'],
    # #             list(gb.keys())[list(gb.keys()).index('step')]: gb['step'],
    # #             list(gb.keys())[list(gb.keys()).index('turn')]: gb['turn'],
    # #             list(gb.keys())[list(gb.keys()).index('phase')]: gb['phase'],
    # #             'dataagents': deepcopy(A.agents)
    # #         }
    # #     )
    # #     agent_data = tuple(
    # #
    # #     )
    # #     agent_data.append(agent_data_item)  # 初始化 agents  之数据为一字典数组
    # #
    # #     interagent_data_item = dict(
    # #         {
    # #             list(gb.keys())[list(gb.keys()).index('process_name')]: gb['process_name'],
    # #             list(gb.keys())[list(gb.keys()).index('step')]: gb['step'],
    # #             list(gb.keys())[list(gb.keys()).index('turn')]: gb['turn'],
    # #             list(gb.keys())[list(gb.keys()).index('phase')]: gb['phase'],
    # #             'datainteragent': deepcopy(A.interagent)
    # #         }
    # #     )
    # #     interagent_data = []
    # #     interagent_data.append(interagent_data_item)  # 初始化interagent之数据为一字典数组
    # #
    # #     A_data = AgentDataCollection(deepcopy(agent_data), deepcopy(interagent_data))
    # #     return A_data
    # #     pass
    # #
    # # @classmethod
    # # def collect_agent_data(cls, A: Agents, A_data: AgentDataCollection, gb: dict):
    # #     """
    # #     收集数据并存储
    # #
    # #     Args:
    # #         A (Agents):
    # #         A_data (AgentDataCollection):
    # #         gb:
    # #
    # #     Returns:
    # #         A_data: 待收集的数据
    # #
    # #     """
    # #     agent_data_item = dict(
    # #         {
    # #             list(gb.keys())[list(gb.keys()).index('process_name')]: gb['process_name'],
    # #             list(gb.keys())[list(gb.keys()).index('step')]: gb['step'],
    # #             list(gb.keys())[list(gb.keys()).index('turn')]: gb['turn'],
    # #             list(gb.keys())[list(gb.keys()).index('phase')]: gb['phase'],
    # #             'dataagents': deepcopy(A.agents)
    # #         }
    # #     )
    # #     A_data.agents.append(agent_data_item)  # 收集 agents  之数据为一字典数组
    # #
    # #     interagent_data_item = dict(
    # #         {
    # #             list(gb.keys())[list(gb.keys()).index('process_name')]: gb['process_name'],
    # #             list(gb.keys())[list(gb.keys()).index('step')]: gb['step'],
    # #             list(gb.keys())[list(gb.keys()).index('turn')]: gb['turn'],
    # #             list(gb.keys())[list(gb.keys()).index('phase')]: gb['phase'],
    # #             'datainteragent': deepcopy(A.interagent)
    # #         }
    # #     )
    # #
    # #     A_data.interagent.append(interagent_data_item)  # 收集interagent之数据为一字典数组
    # #     return A_data
    # #     pass
    # #
    # # @classmethod
    # # def export_agent_data(cls, A_data: AgentDataCollection, gb: dict):
    # #     """
    # #     导出实验结果数据
    # #
    # #     Args:
    # #         A_data:
    # #         gb(dict): 引擎全局变量
    # #
    # #     Returns:
    # #
    # #     """
    # #
    # #     ## 整理 agents  之数据为一数据框
    # #     agent_data_export = pd.DataFrame()
    # #     agent_data = pd.DataFrame()
    # #     numRow, numCol = np.shape(A_data.agents[0]['dataagents'].A_all)
    # #     for (i1, v1) in enumerate(A_data.agents):
    # #         # agent_data['id_data'] = np.full(numRow, v1['id_data'])
    # #         agent_data['process_name'] = np.full(numRow, v1['process_name'])
    # #         agent_data['step'] = np.full(numRow, v1['step'])
    # #         agent_data['turn'] = np.full(numRow, v1['turn'])
    # #         agent_data['phase'] = np.full(numRow, v1['phase'])
    # #         fieldNames = list(v1['dataagents'].__dict__.keys())
    # #         fieldValues = list(v1['dataagents'].__dict__.values())
    # #         for (i2, v2) in enumerate(fieldValues):
    # #             agent_data[fieldNames[i2]] = v2
    # #             pass
    # #         agent_data_export = pd.concat([agent_data_export, agent_data])  # 追加`agent_data`至`agent_data_expert`
    # #         pass  # for
    # #     agent_data_export.insert(0, 'id', range(len(agent_data_export)))  # 添加id列
    # #     agent_data_export.insert(1, 'id_data', np.repeat(range(len(agent_data_export) // gb['num_agent']), gb['num_agent']))  # 添加id_data列
    # #     agent_data_export.to_csv(path.join(gb['folderpath_experiments_output_data'], "agent_exp=" + str(gb['id_experiment']) + ".csv"), index=False)  # 导出为csv格式；
    # #
    # #
    # #     ## 整理interagent之数据为一数据框
    # #     interagent_data_export = pd.DataFrame()
    # #     interagent_data = pd.DataFrame()
    # #     # numRow, numCol = np.shape(A_data.interagent[0]['datainteragent'].A_interagent)
    # #     numRow, numCol = gb['num_agent'], gb['num_agent']
    # #     for (i1, v1) in enumerate(A_data.interagent):
    # #         # interagent_data['id_data'] = np.full(numRow * numCol, v1['id_data'])
    # #         # interagent_data['id_data'] = v1['id_data']
    # #         interagent_data['process_name'] = np.full(numRow * numCol, v1['process_name'])
    # #         interagent_data['step'] = np.full(numRow * numCol, v1['step'])
    # #         interagent_data['turn'] = np.full(numRow * numCol, v1['turn'])
    # #         interagent_data['phase'] = np.full(numRow * numCol, v1['phase'])
    # #         interagent_data['row'] = np.repeat(range(1, numRow + 1), numCol)
    # #         interagent_data['col'] = np.tile(range(1, numCol + 1), numRow)
    # #         fieldNames = list(v1['datainteragent'].__dict__.keys())
    # #         fieldValues = list(v1['datainteragent'].__dict__.values())
    # #         for (i2, v2) in enumerate(fieldValues):
    # #             # if type(v2)==IdsType:
    # #             #     print("这个是id类型！")
    # #             if (v2.dtype == np.float_ or v2.dtype == np.bool_ or v2.dtype == np.int16):
    # #                 interagent_data[fieldNames[i2]] = v2.flatten()  # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
    # #             elif v2.dtype == list:
    # #                 ## 转换信息列表为矩阵形式  #HACK能否用现成的功能函数代替？
    # #                 m2 = np.full((numRow, numCol), False)
    # #                 if v2 is []:
    # #                     continue
    # #                 for (i3, v3) in enumerate(v2):
    # #                     if v3 is []:
    # #                         m2[i3, :] = False
    # #                         continue
    # #                         pass  # if
    # #                     for i4 in v3:
    # #                         if i4 in v3:
    # #                             m2[i3, i4] = True
    # #                             pass  # if
    # #                         else:
    # #                             m2[i3, i4] = False
    # #                             pass  # else
    # #                         pass  # for
    # #                 interagent_data[fieldNames[i2]] = m2.T.flatten()  # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
    # #                 pass  # if
    # #             pass  # for
    # #         interagent_data_export = pd.concat([interagent_data_export, interagent_data])  # 追加当前`interagent_data`至`interagent_data_expert`
    # #         pass  # for
    # #     interagent_data_export.insert(0, 'id', range(len(interagent_data_export)))  # 添加id列
    # #     interagent_data_export.insert(1, 'id_data', np.repeat(range(len(interagent_data_export) // gb['num_agent'] ** 2), gb['num_agent'] ** 2))  # 添加id_data列
    # #     interagent_data_export.to_csv(path.join(gb['folderpath_experiments_output_data'], "interagent_exp=" + str(gb['id_experiment']) + ".csv"), index=False)  # 导出为csv格式；
    # #
    # #     pass  # function
    # #

    # @classmethod
    # def export_parameter_data(cls, gb: dict, combination_of_para: Union[list, pd.DataFrame], para: Optional[dict] = None):
    #     """
    #     导出控制参数数据
    #
    #     Args:
    #         gb (dict): 引擎全局变量
    #         combination_of_para (list): 控制参数集之组合
    #         para (Optional[dict]): 参数变量。默认为 None
    #
    #     Returns:
    #
    #     """
    #
    #     gb['num_experiment'] = len(combination_of_para)  # 获取实验组之实验个数
    #     if para is None:  # 如果参数变量为空，则直接从 combination_of_para 中获取参数变量相关的信息
    #         # df_010 = pd.DataFrame(combination_of_para, columns=combination_of_para[0].keys())  # 转换字典列表为数据框
    #         pass  # if
    #     else:
    #         df_010 = pd.DataFrame(combination_of_para, columns=para.keys())  # 转换字典列表为数据框
    #         pass  # if
    #
    #     # # gb['num_agent'] = len(para['list_id_agent'])  if gb['num_agent'] is None else gb['num_agent']
    #     # list_types = [type(df_010.iloc[0, i]) for i in range(df_010.columns.__len__())]  # 获取列表，元素为数据框之各列之元素之类型
    #     # id_type_is_array = list_types.index(np.ndarray)  # 获取索引值为类型为数组类型的
    #
    #     # ## 获取个体个数
    #     # is_need_to_get_num_agent = False
    #     # if 'num_agent' in gb.keys():
    #     #     if gb['num_agent'] is None:
    #     #         is_need_to_get_num_agent = True
    #     #         pass  # if
    #     # else:
    #     #     is_need_to_get_num_agent = True
    #     #     pass  # if
    #     #
    #     # if is_need_to_get_num_agent:
    #     #     gb['num_agent'] = len(para[list(para.keys())[id_type_is_array]][0])  # 获取字典 `para` 在索引 `id_type_is_array` 对应的变量。该变量是一个列表。获取该列表第一个元素。该元素是一个数组。获取该数组大小，作为个体个数
    #
    #     # ## 导出实验参数为 pkl、csv、Excel xlsx格式到输出文件夹
    #     # df_combinationOfPara = df_010.copy()
    #     # df_combinationOfPara.insert(loc=0, column='exp_id', value=np.arange(1, gb['num_experiment'] + 1))  # 添加实验组id
    #     # df_combinationOfPara.insert(loc=1, column='is_done', value=[False] * gb['num_experiment'])  # 添加是否完成标记
    #     # # 检查是否已经存在，如果文件已经存在则不再导出
    #     # if not Path(gb['folderpath_experiments_output_parameters'], r"parameters.pkl").exists():
    #     #     pd.to_pickle(df_combinationOfPara, Path(gb['folderpath_experiments_output_parameters'], r"parameters.pkl"))
    #     # if not Path(gb['folderpath_experiments_output_parameters'], r"parameters.csv").exists():
    #     #     df_combinationOfPara.to_csv(Path(gb['folderpath_experiments_output_parameters'], r"parameters.csv"), index=False)
    #     # if not Path(gb['folderpath_experiments_output_parameters'], r"parameters.xlsx").exists():
    #     #     df_combinationOfPara.to_excel(Path(gb['folderpath_experiments_output_parameters'], r"parameters.xlsx"), index=False)
    #     #     pass  # if
    #
    #     ## 导出实验参数为 pkl、csv、Excel xlsx格式到输出文件夹
    #     df_combinationOfPara = combination_of_para.copy()
    #     # df_combinationOfPara.insert(loc=0, column='exp_id', value=np.arange(1, gb['num_experiment'] + 1))  # 添加实验组id
    #     df_combinationOfPara.insert(loc=1, column='is_done', value=[False] * gb['num_experiment'])  # 添加是否完成标记
    #
    #     ### 如果参数库当中的参数文件夹中的参数文件有更新，那么就要在后续重新生成参数作业数据
    #     mtime_of_file_parameters_py = Path(gb['folderpath_parameters'], r"set_parameters_variables.py").resolve().stat().st_mtime
    #     mtime_of_file_parameters_pkl = Path(gb['folderpath_parameters'], r"parameters.pkl").resolve().stat().st_mtime
    #     filepath_parameters_works_pkl = Path(gb['folderpath_experiments_output_parameters'], r"parameters_works.pkl").resolve()
    #     if filepath_parameters_works_pkl.exists():  # 检查parameters_works.pkl文件是否存在
    #         mtime_of_file_parameters_works_pkl = filepath_parameters_works_pkl.stat().st_mtime  # 获取parameters_works.pkl文件的最后修改时间
    #         if (mtime_of_file_parameters_pkl > mtime_of_file_parameters_works_pkl) or (mtime_of_file_parameters_py > mtime_of_file_parameters_works_pkl):
    #             is_generate_parameters_works_data = True
    #             print("参数文件有更新，需要重新导出参数作业数据。")
    #         else:
    #             is_generate_parameters_works_data = False
    #             print("参数文件没有更新，不需要重新导出参数作业数据。")
    #     else:
    #         is_generate_parameters_works_data = True
    #         print("参数作业数据文件不存在，需要重新导出参数作业数据。")
    #         pass  # if
    #     if is_generate_parameters_works_data:
    #         Tools._delete_and_recreate_folder(Path(gb['folderpath_engine'], "engine/libraries/parameters"), is_auto_confirmation=gb['is_auto_confirmation'])
    #         Tools._copy_files_from_other_folders(gb['folderpath_parameters'], Path(gb['folderpath_engine'], "engine/libraries/parameters"), is_auto_confirmation=gb['is_auto_confirmation'])
    #         Tools._copy_files_from_other_folders(gb['folderpath_parameters'], gb['folderpath_experiments_output_parameters'], is_auto_confirmation=gb['is_auto_confirmation'])  # 导出一份到输出文件夹
    #         # shutil.copy(Path(gb['folderpath_parameters'], r"set_parameters_variables.py"), gb['folderpath_experiments_output_parameters'])  # 导出一份生成参数的代码文件到输出文件夹
    #         from engine.core.define.define_parameterVariables import para
    #
    #         # pd.to_pickle(df_combinationOfPara, filepath_parameters_works_pkl)
    #         # df_combinationOfPara.to_csv(Path(gb['folderpath_experiments_output_parameters'], r"parameters.csv"), index=False)
    #         # df_combinationOfPara.to_excel(Path(gb['folderpath_experiments_output_parameters'], r"parameters.xlsx"), index=False)
    #         pass
    #
    #     pass  # function

    @classmethod
    def export_config_data(cls, gb: dict):
        """
        导出字典类型的配置数据（全局数据）为 pkl 格式

        Args:
            config_data (dict): 配置数据

        Returns:

        """

        with open(Path(gb['folderpath_experiments_output_config'], r"config.pkl"), "wb") as f:
            pickle.dump(gb, f)

        # pickle.dump(config_data, open(Path(gb['folderpath_experiments_output_data'], r"config.pkl"), "wb"))  # 导出为pkl格式

    # @classmethod
    # def compress_result_data(cls, agent_origin: pd.DataFrame, interagent_origin: pd.DataFrame):
    #     """
    #     压缩实验结果数据
    #
    #     Args:
    #         agent_origin (pd.DataFrame): 原始的 agents 实验结果数据
    #         interagent_origin (pd.DataFrame): 原始的 interagent 实验结果数据
    #
    #     Returns:
    #         agent_compress (pd.DataFrame): 压缩后的 agents 实验结果数据
    #         interagent_compress (pd.DataFrame): 压缩后的 interagent 实验结果数据
    #
    #     """
    #     len_result_data = len(agent_origin)
    #     agent_compress = pd.DataFrame(columns=agent_origin.columns, index=range(len_result_data))
    #     # 遍历每一列
    #     for column in agent_origin.columns:
    #         if (type(agent_origin.at[0, column]) == np.ndarray and type(agent_origin.at[0, column][0]) == MoneyType):  # 如果是 MoneyType 型的 numpy 数组
    #             agent_compress.at[0, column] = agent_origin.loc[0, column].copy()
    #             for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，计算差值
    #                 diff = agent_origin.at[i, column] - agent_origin.at[i - 1, column]
    #                 agent_compress.at[i, column] = csr_array(diff.reshape(1, -1))
    #                 pass  # for
    #             agent_compress.at[len_result_data - 1, column] = agent_origin.at[len_result_data - 1, column].copy()
    #         elif (type(agent_origin.at[0, column]) == np.ndarray and (type(agent_origin.at[0, column][0]) == IdsType or type(agent_origin.at[0, column][0]) == np.int64)):  # 如果是 IdsType 型的 numpy 数组
    #             agent_compress.at[0, column] = agent_origin.at[0, column].copy()
    #             for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，计算不同
    #                 diff = agent_origin.at[i, column] != agent_origin.at[i - 1, column]
    #                 agent_compress.at[i, column] = csr_array(diff.astype(IdsType).reshape(1, -1))
    #                 pass  # for
    #             agent_compress.at[len_result_data - 1, column] = agent_origin.at[len_result_data - 1, column].copy()
    #         elif (type(agent_origin.at[0, column]) == np.ndarray and type(agent_origin.at[0, column][0]) == np.bool_):  # 如果是布尔型的 numpy 数组
    #             agent_compress.at[0, column] = agent_origin.at[0, column].copy()
    #             for i in range(1, len_result_data - 1, 1):
    #                 diff = agent_origin.at[i, column] != agent_origin.at[i - 1, column]
    #                 agent_compress.at[i, column] = csr_array(diff.reshape(1, -1))  # 转换为稀疏数组
    #                 pass  # for
    #             agent_compress.at[len_result_data - 1, column] = agent_origin.at[len_result_data - 1, column].copy()
    #         elif (type(agent_origin.at[0, column]) == np.ndarray and (type(agent_origin.at[0, column][0]) == NameType or type(agent_origin.at[0, column][0]) == AagentsrType or type(agent_origin.at[0, column][0]) == str)):  # 如果是字符串类型的 numpy 数组
    #             agent_compress.at[0, column] = agent_origin.at[0, column].copy()
    #             for i in range(1, len_result_data - 1, 1):
    #                 diff = (agent_origin.at[i, column] == agent_origin.at[i - 1, column])
    #                 agent_compress.at[i, column] = agent_origin.at[i, column].copy()
    #                 agent_compress.at[i, column][diff] = ''
    #                 if diff.all():  # 如果元素全为相同，则整个数组直接设置为 None，否则相同的元素设置为空字符串
    #                     agent_compress.at[i, column] = None
    #                 else:
    #                     agent_compress.at[i, column][diff] = ''
    #                     pass  # if
    #                 pass  # for
    #             agent_compress.at[len_result_data - 1, column] = agent_origin.at[len_result_data - 1, column].copy()
    #         elif (type(agent_origin.at[0, column]) == np.ndarray and agent_origin.at[0, column][0] == None):  # 如果值为 None 的 numpy 数组
    #             agent_compress.at[0, column] = agent_origin.at[0, column].copy()
    #             for i in range(1, len_result_data - 1, 1):
    #                 agent_compress.at[i, column] = None  # 这里设定，只要元素存在 None，则整个数组都没有被使用，直接设为 None
    #                 pass  # for
    #             agent_compress.at[len_result_data - 1, column] = agent_origin.at[len_result_data - 1, column].copy()
    #         elif (type(agent_origin.at[0, column]) == str):  # 如果是字符串类型
    #             agent_compress.at[0, column] = agent_origin.at[0, column]
    #             for i in range(1, len_result_data - 1, 1):
    #                 if (agent_origin.at[i, column] == agent_origin.at[i - 1, column]):
    #                     agent_compress.at[i, column] = None
    #                 else:
    #                     agent_compress.at[i, column] = agent_origin.at[i, column]
    #                     pass  # if
    #                 pass  # for
    #             agent_compress.at[len_result_data - 1, column] = agent_origin.at[len_result_data - 1, column]
    #         else:
    #             agent_compress[column] = agent_origin[column].copy()
    #             pass  # if
    #
    #         pass  # for
    #
    #     interagent_compress = pd.DataFrame(columns=interagent_origin.columns).reindex(range(len_result_data))
    #     # 遍历每一列
    #     for column in interagent_origin.columns:
    #         if (type(interagent_origin.at[0, column]) == np.ndarray and type(interagent_origin.at[0, column][0, 0]) == MoneyType):  # 如果是 MoneyType 型的 numpy 数组
    #             interagent_compress.at[0, column] = interagent_origin.at[0, column].copy()
    #             for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，计算差值
    #                 diff = interagent_origin.at[i, column] - interagent_origin.at[i - 1, column]
    #                 interagent_compress.at[i, column] = csr_array(diff)
    #                 pass  # for
    #             interagent_compress.at[len_result_data - 1, column] = interagent_origin.at[len_result_data - 1, column].copy()
    #         elif (type(interagent_origin.at[0, column]) == np.ndarray and (type(interagent_origin.at[0, column][0, 0]) == IdsType or type(interagent_origin.at[0, column][0, 0]) == np.int64)):  # 如果是 IdsType 型的 numpy 数组
    #             interagent_compress.at[0, column] = interagent_origin.at[0, column].copy()
    #             for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，计算不同
    #                 diff = interagent_origin.at[i, column] != interagent_origin.at[i - 1, column]
    #                 interagent_compress.at[i, column] = csr_array(diff.astype(IdsType))
    #                 pass  # for
    #             interagent_compress.at[len_result_data - 1, column] = interagent_origin.at[len_result_data - 1, column].copy()
    #         elif (type(interagent_origin.at[0, column]) == np.ndarray and type(interagent_origin.at[0, column][0, 0]) == np.bool_):  # 如果是布尔型的 numpy 数组
    #             interagent_compress.at[0, column] = interagent_origin.at[0, column].copy()
    #             for i in range(1, len_result_data - 1, 1):
    #                 diff = interagent_origin.at[i, column] != interagent_origin.at[i - 1, column]
    #                 interagent_compress.at[i, column] = csr_array(diff)  # 转换为稀疏数组
    #                 pass  # for
    #             interagent_compress.at[len_result_data - 1, column] = interagent_origin.at[len_result_data - 1, column].copy()
    #         elif (type(interagent_origin.at[0, column]) == np.ndarray and (type(interagent_origin.at[0, column][0]) == NameType or type(interagent_origin.at[0, column][0]) == AagentsrType or type(interagent_origin.at[0, column][0]) == str)):  # 如果是字符串类型的 numpy 数组
    #             interagent_compress.at[0, column] = interagent_origin.at[0, column].copy()
    #             for i in range(1, len_result_data - 1, 1):
    #                 diff = (interagent_origin.at[i, column] == interagent_origin.at[i - 1, column])
    #                 interagent_compress.at[i, column] = interagent_origin.at[i, column].copy()
    #                 interagent_compress.at[i, column][diff] = ''
    #                 if diff.all():  # 如果元素全为相同，则整个数组直接设置为 None，否则相同的元素设置为空字符串
    #                     interagent_compress.at[i, column] = None
    #                 else:
    #                     interagent_compress.at[i, column][diff] = ''
    #                     pass  # if
    #                 pass  # for
    #             interagent_compress.at[len_result_data - 1, column] = interagent_origin.at[len_result_data - 1, column].copy()
    #         elif (type(interagent_origin.at[0, column]) == np.ndarray and interagent_origin.at[0, column][0, 0] == None):  # 如果值为 None 的 numpy 数组
    #             interagent_compress.at[0, column] = interagent_origin.at[0, column].copy()
    #             for i in range(1, len_result_data - 1, 1):
    #                 interagent_compress.at[i, column] = None  # 这里设定，只要元素存在 None，则整个数组都没有被使用，直接设为 None
    #                 pass  # for
    #             interagent_compress.at[len_result_data - 1, column] = interagent_origin.at[len_result_data - 1, column].copy()
    #         elif (type(interagent_origin.at[0, column]) == str):  # 如果是字符串类型
    #             interagent_compress.at[0, column] = interagent_origin.at[0, column]
    #             for i in range(1, len_result_data - 1, 1):
    #                 if (interagent_origin.at[i, column] == interagent_origin.at[i - 1, column]):
    #                     interagent_compress.at[i, column] = None
    #                 else:
    #                     interagent_compress.at[i, column] = interagent_origin.at[i, column]
    #                     pass  # if
    #                 pass  # for
    #             interagent_compress.at[len_result_data - 1, column] = interagent_origin.at[len_result_data - 1, column]
    #         else:  # 其他数据类型，直接复制原来的数据
    #             interagent_compress[column] = interagent_origin[column].copy()
    #             pass  # if
    #
    #         pass  # for
    #
    #     return agent_compress, interagent_compress
    #     pass  # function
    #
    # @classmethod
    # def decompress_result_data(cls, agent_compress: pd.DataFrame, interagent_compress: pd.DataFrame):
    #     """
    #     解压实验结果数据。
    #
    #     解压后的数据应该与原始的实验结果数据一样。
    #
    #     Args:
    #         agent_compress (pd.DataFrame): 压缩后的 agents 实验结果数据
    #         interagent_compress (pd.DataFrame): 压缩后的 interagent 实验结果数据
    #
    #     Returns:
    #         agent_decompress (pd.DataFrame): 解压后的 agents 实验结果数据
    #         interagent_decompress (pd.DataFrame): 解压后的 interagent 实验结果数据
    #     """
    #
    #     len_result_data = len(agent_compress)
    #     agent_decompress = pd.DataFrame(columns=agent_compress.columns, index=range(len_result_data))
    #     # 遍历每一列
    #     for column in agent_compress.columns:
    #         if (type(agent_compress.at[0, column]) == np.ndarray and type(agent_compress.at[0, column][0]) == MoneyType):  # 如果是 MoneyType 型的 numpy 数组
    #             agent_decompress.at[0, column] = agent_compress.at[0, column].copy()
    #             agent_decompress.at[1, column] = agent_compress.at[0, column] + agent_compress.at[1, column].toarray().ravel()
    #             for i in range(2, len_result_data - 1, 1):  # 从第三行开始遍历每一行直到倒数第二行，累加差值
    #                 diff = agent_compress.at[i, column].toarray().ravel()
    #                 agent_decompress.at[i, column] = agent_decompress.at[i - 1, column] + diff
    #                 pass  # for
    #             agent_decompress.at[len_result_data - 1, column] = agent_compress.at[len_result_data - 1, column].copy()
    #         elif (type(agent_compress.at[0, column]) == np.ndarray and (type(agent_compress.at[0, column][0]) == IdsType or type(agent_compress.at[0, column][0]) == np.int64)):  # 如果是 IdsType 型的 numpy 数组
    #             last_not_none = agent_compress.at[0, column].copy()
    #             agent_decompress.at[0, column] = last_not_none.copy()
    #             for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，还原不同
    #                 diff = agent_compress.at[i, column].toarray().ravel()
    #                 if not diff.all():  # 设定只有这种可能性
    #                     agent_decompress.at[i, column] = last_not_none.copy()
    #                     pass  # if
    #                 pass  # for
    #             agent_decompress.at[len_result_data - 1, column] = agent_compress.at[len_result_data - 1, column].copy()
    #         elif (type(agent_compress.at[0, column]) == np.ndarray and type(agent_compress.at[0, column][0]) == np.bool_):  # 如果是布尔型的 numpy 数组
    #             agent_decompress.at[0, column] = agent_compress.at[0, column].copy()
    #             agent_decompress.at[1, column] = agent_compress.at[0, column] ^ agent_compress.at[1, column].toarray().ravel()
    #             for i in range(2, len_result_data - 1, 1):
    #                 diff = agent_compress.at[i, column].toarray().ravel()
    #                 agent_decompress.at[i, column] = agent_decompress.at[i - 1, column] ^ diff
    #                 pass  # for
    #             agent_decompress.at[len_result_data - 1, column] = agent_compress.at[len_result_data - 1, column].copy()
    #         elif (type(agent_compress.at[0, column]) == np.ndarray and (type(agent_compress.at[0, column][0]) == NameType or type(agent_compress.at[0, column][0]) == AagentsrType or type(agent_compress.at[0, column][0]) == str)):  # 如果是字符串类型的 numpy 数组
    #             last_not_none = agent_compress.at[0, column].copy()
    #             agent_decompress.at[0, column] = last_not_none.copy()
    #             for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，还原不同
    #                 if agent_compress.at[i, column] is None:  # 如果是 None，则直接设置为前一行的值，否则与上一个非 None 值计算不同的部分，然后赋值
    #                     agent_decompress.at[i, column] = last_not_none.copy()
    #                 else:
    #                     last_last_not_none = last_not_none.copy()
    #                     last_not_none = agent_compress.at[i, column].copy()
    #                     diff = (last_not_none == '')
    #                     agent_decompress.at[i, column] = last_not_none.copy()
    #                     agent_decompress.at[i, column][diff] = last_last_not_none[diff]
    #                     pass  # if
    #                 pass  # for
    #             agent_decompress.at[len_result_data - 1, column] = agent_compress.at[len_result_data - 1, column].copy()
    #         elif (type(agent_compress.at[0, column]) == np.ndarray and agent_compress.at[0, column][0] == None):  # 如果值为 None 的 numpy 数组
    #             agent_decompress.at[0, column] = agent_compress.at[0, column]
    #             for i in range(1, len_result_data - 1, 1):
    #                 agent_decompress.at[i, column] = agent_compress.at[0, column].copy()  # 直接赋值为第一行的值
    #                 pass  # for
    #             agent_decompress.at[len_result_data - 1, column] = agent_compress.at[len_result_data - 1, column].copy()
    #         elif (type(agent_compress.at[0, column]) == str):  # 如果是字符串类型
    #             last_not_none = agent_compress.at[0, column]
    #             agent_decompress.at[0, column] = last_not_none
    #             for i in range(1, len_result_data - 1, 1):
    #                 if agent_compress.at[i, column] is None:  # 如果是 None，则直接设置为前一行的值，否则与上一个非 None 值计算不同的部分，然后赋值
    #                     agent_decompress.at[i, column] = last_not_none
    #                 else:
    #                     last_not_none = agent_compress.at[i, column]
    #                     agent_decompress.at[i, column] = last_not_none
    #                     pass  # if
    #                 pass  # for
    #             agent_decompress.at[len_result_data - 1, column] = agent_compress.at[len_result_data - 1, column]
    #         else:  # 其他数据类型，直接复制原来的数据
    #             agent_decompress[column] = agent_compress[column].copy()
    #             pass  # if
    #
    #         pass  # for
    #
    #     interagent_decompress = pd.DataFrame(columns=interagent_compress.columns, index=range(len_result_data))
    #     # 遍历每一列
    #     for column in interagent_compress.columns:
    #         if (type(interagent_compress.at[0, column]) == np.ndarray and type(interagent_compress.at[0, column][0, 0]) == MoneyType):  # 如果是 MoneyType 型的 numpy 数组
    #             interagent_decompress.at[0, column] = interagent_compress.at[0, column].copy()
    #             interagent_decompress.at[1, column] = interagent_compress.at[0, column] + interagent_compress.at[1, column].toarray()
    #             for i in range(2, len_result_data - 1, 1):  # 从第三行开始遍历每一行直到倒数第二行，累加差值
    #                 diff = interagent_compress.at[i, column].toarray()
    #                 interagent_decompress.at[i, column] = interagent_decompress.at[i - 1, column] + diff
    #                 pass  # for
    #             interagent_decompress.at[len_result_data - 1, column] = interagent_compress.at[len_result_data - 1, column].copy()
    #         elif (type(interagent_compress.at[0, column]) == np.ndarray and (type(interagent_compress.at[0, column][0, 0]) == IdsType or type(interagent_compress.at[0, column][0, 0]) == np.int64)):  # 如果是 IdsType 型的 numpy 数组
    #             last_not_none = interagent_compress.at[0, column].copy()
    #             interagent_decompress.at[0, column] = last_not_none.copy()
    #             for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，还原不同
    #                 diff = interagent_compress.at[i, column].toarray()
    #                 if not diff.all():  # 设定只有这种可能性
    #                     interagent_decompress.at[i, column] = last_not_none.copy()
    #                     pass  # if
    #                 pass  # for
    #             interagent_decompress.at[len_result_data - 1, column] = interagent_compress.at[len_result_data - 1, column].copy()
    #         elif (type(interagent_compress.at[0, column]) == np.ndarray and type(interagent_compress.at[0, column][0, 0]) == np.bool_):  # 如果是布尔型的 numpy 数组
    #             interagent_decompress.at[0, column] = interagent_compress.at[0, column].copy()
    #             interagent_decompress.at[1, column] = interagent_compress.at[0, column] + interagent_compress.at[1, column].toarray()
    #             for i in range(2, len_result_data - 1, 1):
    #                 diff = interagent_compress.at[i, column].toarray()
    #                 interagent_decompress.at[i, column] = interagent_decompress.at[i - 1, column] ^ diff
    #                 pass  # for
    #             interagent_decompress.at[len_result_data - 1, column] = interagent_compress.at[len_result_data - 1, column].copy()
    #         elif (type(interagent_compress.at[0, column]) == np.ndarray and (type(interagent_compress.at[0, column][0]) == NameType or type(interagent_compress.at[0, column][0]) == AagentsrType or type(interagent_compress.at[0, column][0]) == str)):  # 如果是字符串类型的 numpy 数组
    #             last_not_none = interagent_compress.at[0, column].copy()
    #             interagent_decompress.at[0, column] = last_not_none.copy()
    #             for i in range(1, len_result_data - 1, 1):  # 从第二行开始遍历每一行直到倒数第二行，还原不同
    #                 if interagent_compress.at[i, column] is None:  # 如果是 None，则直接设置为前一行的值，否则与上一个非 None 值计算不同的部分，然后赋值
    #                     interagent_decompress.at[i, column] = last_not_none.copy()
    #                 else:
    #                     last_last_not_none = last_not_none.copy()
    #                     last_not_none = interagent_compress.at[i, column].copy()
    #                     diff = (last_not_none == '')
    #                     interagent_decompress.at[i, column] = last_not_none.copy()
    #                     interagent_decompress.at[i, column][diff] = last_last_not_none[diff]
    #                     pass  # if
    #                 pass  # for
    #             interagent_decompress.at[len_result_data - 1, column] = interagent_compress.at[len_result_data - 1, column].copy()
    #         elif (type(interagent_compress.at[0, column]) == np.ndarray and interagent_compress.at[0, column][0, 0] == None):  # 如果值为 None 的 numpy 数组
    #             interagent_decompress.at[0, column] = interagent_compress.at[0, column]
    #             for i in range(1, len_result_data - 1, 1):
    #                 interagent_decompress.at[i, column] = interagent_compress.at[0, column].copy()  # 直接赋值为第一行的值
    #                 pass  # for
    #             interagent_decompress.at[len_result_data - 1, column] = interagent_compress.at[len_result_data - 1, column].copy()
    #         elif (type(interagent_compress.at[0, column]) == str):  # 如果是字符串类型
    #             last_not_none = interagent_compress.at[0, column]
    #             interagent_decompress.at[0, column] = last_not_none
    #             for i in range(1, len_result_data - 1, 1):
    #                 if interagent_compress.at[i, column] is None:  # 如果是 None，则直接设置为前一行的值，否则与上一个非 None 值计算不同的部分，然后赋值
    #                     interagent_decompress.at[i, column] = last_not_none
    #                 else:
    #                     last_not_none = interagent_compress.at[i, column]
    #                     interagent_decompress.at[i, column] = last_not_none
    #                     pass  # if
    #                 pass  # for
    #             interagent_decompress.at[len_result_data - 1, column] = interagent_compress.at[len_result_data - 1, column]
    #         else:  # 其他数据类型，直接复制原来的数据
    #             interagent_decompress[column] = interagent_compress[column].copy()
    #             pass  # if
    #
    #         pass  # for
    #
    #     return agent_decompress, interagent_decompress
    #     pass  # function

    pass  # class
