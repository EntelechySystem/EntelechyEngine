"""
引擎之初始化环境
"""

# ## 包含环境
# using Pkg
# Pkg.activate(".")

## 添加自定义的路径环境变量

ENV["EXPERIMENTS_PATH"] = abspath(joinpath(@__DIR__, "../../", "Experiments"))

# if globals[:运行模式] == "批量实验作业运行模式"
#     ENV["DATA_PATH"] = abspath(joinpath(ENV["ENGINE_PATH"], "../", "Data/ExperimentsData"))
#     ENV["LIBRARY_PATH"] = abspath(joinpath(ENV["ENGINE_PATH"], "Library"))
# elseif globals[:运行模式] == "交互式观察运行模式"
#     ENV["DATA_PATH"] = abspath(joinpath(ENV["ENGINE_PATH"], "../", "Data"))
#     ENV["LIBRARY_PATH"] = abspath(joinpath(ENV["ENGINE_PATH"], "Library"))
# end

ENV["DATA_PATH"] = abspath(joinpath(ENV["ENGINE_PATH"], "../", "Data"))
ENV["LIBRARY_PATH"] = abspath(joinpath(ENV["ENGINE_PATH"], "Library"))
ENV["AGENTS_DATA_PATH"] = abspath(joinpath(ENV["DATA_PATH"], "AgentsData"))
ENV["SIMS_DATA_PATH"] = abspath(joinpath(ENV["DATA_PATH"], "SimulationsData"))
ENV["SETTINGS_DATA_PATH"] = abspath(joinpath(ENV["DATA_PATH"], "SettingsData"))
ENV["CONFIG_LIBRARY_PATH"] = abspath(joinpath(ENV["LIBRARY_PATH"], "Config"))
ENV["SETTINGS_LIBRARY_PATH"] = abspath(joinpath(ENV["LIBRARY_PATH"], "Settings"))
ENV["PARAMETERS_LIBRARY_PATH"] = abspath(joinpath(ENV["LIBRARY_PATH"], "Parameters"))
ENV["GLOBALS_LIBRARY_PATH"] = abspath(joinpath(ENV["LIBRARY_PATH"], "Globals"))



## 包括文件
include("./../Core/define_const.jl")
include("./../Tools/Tools.jl")
include("./../Tools/DataManageTools.jl")
include("./../Tools/MathTool.jl")
include("./../Tools/PhysicsTools.jl")
include("./../Core/define_type.jl")
include("./../Core/agent.jl")
include("./../Functions/agent_states.jl")
include("./../Functions/model_states.jl")
include("./../Functions/retrieve_data_tables.jl")
include("./../Functions/agents_interaction_rules.jl")
include("./../Core/model_and_agents_steps.jl")
include("./../Core/model.jl")
include("./../Functions/visualization.jl")







