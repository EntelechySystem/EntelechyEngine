"""
数据管理工具
"""


"""
链式快速检索数据表，通过 id 获取 id。

# Args:
- `source::Int`: 数据表之索引 ；
- `retrieved_chains::Array`: 一个元组数组，每个元组包含 2 个元素，每个元素是一个 Symbol 类型的数据，分别是数据表的名称、数据表待查询结果之列名 ；
- `tables::Dict`: 由包括各数据表构成的字典，键名是数据表名称，键值是数据表 ；

# Returns:
- `value::Int`: 数据表之值之 ID ；
"""
function retrieve_tables_chains_from_id_to_get_id(source::Int, retrieved_chains::Array{Tuple{String,String},1}, tables::Dict=tables)
    value = source
    for (table_name, column_name) in retrieved_chains
        value = tables[table_name][value, column_name]
    end
    return value
end


"""
单次快速检索数据表，通过源之 id 获取结果

# Args:
- `table::DataFrame`: 数据表 ；
- `source::Int`: 数据表之索引 ；
- `target_column::Symbol`: 数据表待查询结果之列名 ；

# Returns:
- `value::Symbol`: 数据表之结果 ；
"""
retrieve_tables_once_from_id_to_get_result(table::DataFrame, source_id::Int, target_column::Symbol) = table[source_id, target_column]


"""
单次快速检索数据表，通过源之 id 获取结果。

# Args:
- `source::Int`: 数据表之索引 ；
- `retrieved_chains::Array`: 一个元组数组，每个元组包含 2 个元素，每个元素是一个 Symbol 类型的数据，分别是数据表的名称、数据表待查询结果之列名 ；
- `tables::Dict`: 由包括各数据表构成的字典，键名是数据表名称，键值是数据表 ；

# Returns:
- `value::Symbol`: 数据表之结果 ；


"""
retrieve_tables_once_from_id_to_get_result(source::Int, retrieved_chains::Array, tables::Dict=tables) = tables[retrieved_chains[1][1]][source, retrieved_chains[1][2]]


"""
单次检索数据表，通过任意值（包括 id ）获取结果。

# Args:
- `table::DataFrame`: 数据表 ；
- `source_column::Symbol`: 数据表源列名 ；
- `source_value::Union{Symbol,String}`: 数据表之值 ；
- `target_column::Symbol`: 数据表待查询结果之列名 ；

# Returns:
- `value::Int`: 数据表之结果 ；


"""
retrieve_tables_once_from_value_to_get_result(table::DataFrame, source_column::Symbol, source_value::Union{Symbol,String,Int}, target_column::Symbol) = subset(table, source_column => x -> x .== source_value)[1, target_column]

"""
单次检索数据表，通过任意值（包括 id ）获取结果。

# Args:
- `source::Union{Symbol,String}`: 数据表之值 ；
- `retrieved_chains::Array`: 一个元组数组，每个元组包含 3 个元素，每个元素是一个 Symbol 类型的数据，分别是数据表的名称、数据表源列名、数据表待查询结果之列名 ；
- `tables::Dict`: 各数据表构成的字典，键名是数据表名称，键值是数据表 ；

# Returns:
- `value::Int`: 数据表之结果；
"""
retrieve_tables_once_from_value_to_get_result(source::Union{Symbol,String}, retrieved_chains::Array, tables::Dict=tables) = subset(tables[retrieved_chains[1][1]], retrieved_chains[1][2] => x -> x .== source)[1, retrieved_chains[1][3]]



"""
单次检索数据表，通过源 id 、汇 id 获取交互结果 #TODO 需要改成检索邻接矩阵

# Args:
- `id_source_row::Int`: 数据表之行源；
- `id_source_col::Int`: 数据表之列源；
- `retrieved_chains::Array`: 一个元组数组，每个元组包含 4 个元素，每个元素是一个 Symbol 类型的数据，分别是数据表的名称、数据表行源之列名、数据表列源之列名、数据表待查询结果之列名 ；
- `tables::Dict`: 各数据表构成的字典，键名是数据表名称，键值是数据表；

# Returns:
- `Any::`: 源和汇之交互值；

"""
function retrieve_tables_once_from_id_to_get_inter_result(id_source_row::Int, id_source_col::Int, retrieved_chains::Array, tables::Dict=tableses)
    return tables[retrieved_chains[1][1]][findall((row -> row[retrieved_chains[1][2]] == id_source_row && row[retrieved_chains[1][3]] == id_source_col), eachrow(tables[retrieved_chains[1][1]]))[1], retrieved_chains[1][4]]
end

# """
# 单次检索数据表，通过源 id 、汇 id 获取交互 id

# Args:
#     id_source_row (Int): 数据表之行源；
#     id_source_col (Int): 数据表之列源；
#     retrieved_chains (Array): 一个元组数组，每个元组包含 4 个元素，每个元素是一个 Symbol 类型的数据，分别是数据表的名称、数据表行源之列名、数据表列源之列名、数据表待查询结果之列名 ；
#     tables (Dict): 各数据表构成的字典，键名是数据表名称，键值是数据表 ；

# Returns:
#     Any: 源和汇之交互值 ；

# """
# function retrieve_tables_once_from_id_to_get_inter_id(id_source_row::Int, id_source_col::Int, retrieved_chains::Array, tables::Dict=tableses)
#     return tables[retrieved_chains[1][1]][findall((row -> row[retrieved_chains[1][2]] == id_source_row && row[retrieved_chains[1][3]] == id_source_col), eachrow(tables[retrieved_chains[1][1]]))[1], retrieved_chains[1][4]]
# end


"""
单次检索数据表，通过源之任意的值、汇之任意的值，获取交互结果

# Args:
- `table::DataFrame`: 数据表 ；
- `source_row_column::Symbol`: 数据表行源之列名；
- `source_row_value::Union{Symbol,String}`: 数据表之行源；
- `source_col_column::Symbol`: 数据表列源之列名；
- `source_col_value::Union{Symbol,String}`: 数据表之列源；
- `result_column::Symbol`: 数据表待查询结果之列名；

# Returns:
- `Any::`: 源和汇之交互值；

"""
function retrieve_tables_once_from_value_to_get_inter_result(table::DataFrame, source_row_column::Symbol, source_row_value::Union{Symbol,String,Int}, source_col_column::Symbol, source_col_value::Union{Symbol,String,Int}, result_column::Symbol)
    return subset(table, source_row_column => x -> x .== source_row_value, source_col_column => x -> x .== source_col_value)[1, result_column]
end


"""
单次检索数据表，通过源之任意的值、汇之任意的值，获取交互结果

# Args:
- `id_source_row::Int`: 数据表之行源；
- `id_source_col::Int`: 数据表之列源；
- `retrieved_chains::Array`: 一个元组数组，每个元组包含 4 个元素，每个元素是一个 Symbol 类型的数据，分别是数据表的名称、数据表行源之列名、数据表列源之列名、数据表待查询结果之列名；
- `tables::Dict`: 各数据表构成的字典，键名是数据表名称，键值是数据表；

# Returns:
- `交互值::Any`: 源和汇之交互值；

"""
function retrieve_tables_once_from_value_to_get_inter_result(source_row::Union{Symbol,String,Int}, source_col::Union{Symbol,String,Int}, retrieved_chains::Array, tables::Dict=tableses)
    return subset(tables[retrieved_chains[1][1]], retrieved_chains[1][2] => x -> x .== source_row, retrieved_chains[1][3] => x -> x .== source_col)[1, retrieved_chains[1][4]]
end




# """
# 单次检索数据表，从值到 id #HACK 以下弃用

# Args: #TODO
#     id_source (Union{UInt,Int}): 数据表的索引 ；
#     retrieved_chains (Array{Tuple{String,String},1}): 一个元组数组，每个元组包含两个字符串，分别是数据表的名称和数据表的列名 ；
#     tables (Dict): 各数据表构成的字典，键名是数据表名称，键值是数据表 ；

# Returns:
#     value_id (Int): 数据表之值之 ID ；
#     value_name (Symbol): 数据表之值之名称 ；

# """
# function retrieve_tables_once_from_value_to_get_id(source::Union{String,Symbol}, retrieved_chains::Array, tables::Dict=tables)
#     # if (source isa String || source isa Symbol)
#     table, column_val_name, column_id_name = tables[retrieved_chains[1][1]], Symbol("val_" * String(retrieved_chains[1][2])), Symbol("key_" * String(retrieved_chains[1][2]))
#     value = subset(table, column_val_name => x -> x .== source)[1, column_id_name]  # 从第一个数据表中检索
#     i += 1
#     # elseif (source isa UInt || source isa Int)
#     #     value = source
#     # else
#     #     error("source 类型错误")
#     # end

#     for (table_name, column_name) in retrieved_chains[i:end]
#         println("table_name = $table_name, column_name = $column_name") #DEBUG
#         if length(retrieved_chains[i]) == 2  # 如果检索链之元组有 2 个元素
#             column_full_name = Symbol("id_" * String(column_name))
#             value = tables[table_name][value, column_full_name]
#         end
#     end

#     value_id = value  # 获取值对应的 ID
#     table_name, column_val_name = retrieved_chains[end]
#     column_full_name = Symbol("name_" * String(column_val_name))
#     println("table name = $table_name, column full name = $column_full_name , value = $value")
#     value_name = tables[table_name][value_id, column_full_name]  # 获取值对应的名称

#     return value_id, value_name
# end


# """
# 检索数据表获取交互值

# Args:
#     source (Union{UInt,Int,String,Symbol}): 数据表的索引 ；
#     target (Union{Nothing,UInt,Int,String,Symbol}): 数据表的索引 ；
#     retrieved_chains (Array{Tuple{String,String},1}): 一个元组数组，每个元组包含两个字符串，分别是数据表的名称和数据表的列名 ；
#     tables (Dict): 各数据表构成的字典，键名是数据表名称，键值是数据表 ；

# Returns:
#     value_id (Int): 数据表之值之 ID ；
#     value_name (Symbol): 数据表之值之名称 ；

# """
# function retrieve_tables_get_inter_result(source::Union{UInt,Int,String,Symbol}, target::Union{Nothing,UInt,Int,String,Symbol}, retrieved_chains, tables::Dict=tables)
#     i = Int8(1)
#     if (source isa String || source isa Symbol)
#         table, column_val_name, column_key_name = tables[retrieved_chains[i][1]], Symbol("val_" * retrieved_chains[i][2]), Symbol("id_" * retrieved_chains[i][2])
#         value_source = subset(table, column_val_name => x -> x .== source)[1, column_key_name]  # 从第一个数据表中检索
#         i += 1
#     elseif (source isa UInt || source isa Int)
#         value_source = source
#     else
#         error("source 类型错误")
#     end

#     j = UInt8(1)
#     if target isa Nothing
#         value_target = nothing
#     elseif (target isa String || target isa Symbol)
#         table, column_val_name, column_key_name = tables[retrieved_chains[j][1]], Symbol("val_" * retrieved_chains[j][2]), Symbol("id_" * retrieved_chains[j][2])
#         value_target = subset(table, column_val_name => x -> x .== target)[1, column_key_name]  # 从第一个数据表中检索
#         j += 1
#     elseif (target isa UInt || target isa Int)
#         value_target = target
#     else
#         error("target 类型错误")
#     end

#     for _ in retrieved_chains[i:end]
#         if length(retrieved_chains[i]) == 4  # 如果检索链之元组有 4 个元素
#             table_name, column_inter_name, column_row_name, column_col_name = retrieved_chains[i]
#             column_inter_full_name, column_row_full_name, column_col_full_name = map(name -> Symbol("id_" * String(name)), [column_inter_name, column_row_name, column_col_name])
#             value = get_inter_value_from_table(tables[table_name], column_inter_full_name, column_row_full_name, value_source, column_col_full_name, value_target)
#         elseif length(retrieved_chains[i]) == 2  # 如果检索链之元组有 2 个元素
#             table_name, column_name = retrieved_chains[i]
#             column_full_name = Symbol("id_" * String(column_name))
#             value = tables[table_name][value, column_full_name]
#         end
#     end

#     value_id = value  # 获取值对应的 ID
#     value_name = tables[table_name][value_id, Symbol("name_" * String(column_name))]  # 获取值对应的名称

#     return value_id, value_name

# end



"""
从文件夹中加载所有的 CSV 文件，返回一个 DataFrames 字典，字典的键是文件名的中间部分，字典的值是对应的 DataFrame。

# Args:
- `str_folderpath::String`: 文件夹的路径 ；

# Returns:
- `dataframes::dict`: 一个字典，字典的键是文件名的中间部分，字典的值是对应的 DataFrame ；

"""
function load_CSVs_to_DataFrames(str_folderpath::String)
    dataframes = Dict()
    folderpath = joinpath(ENV["PWD"], str_folderpath)
    all_files = readdir(folderpath)
    list_filenames = filter(x -> occursin(r"^csv_rt_.*\.csv$", x), all_files)
    for filename in list_filenames
        filepath = joinpath(folderpath, filename)
        table_name = basename(filepath)
        if startswith(table_name, "csv_rt_")  # 如果文件名的前缀是 'csv_rt_'，那么就是一个关系型数据表
            df = CSV.read(filepath, DataFrame)
            table_middle_name = split(split(table_name, "_")[3], ".")[1]
            dataframes[table_middle_name] = df
        end  # if
    end  # for
    return dataframes
end

"""
从文件夹中加载所有的 pkl 文件，返回一个 DataFrames 字典，字典的键是文件名的中间部分，字典的值是对应的 DataFrame。

# Args:
- `str_folderpath::String`: 文件夹的路径 ；

# Returns:
- `dataframes::dict`: 一个字典，字典的键是文件名的中间部分，字典的值是对应的 DataFrame ；

"""
function load_PKLs_to_DataFrames(str_folderpath::String)
    pandas = pyimport("pandas")
    dataframes = Dict()
    folderpath = joinpath(ENV["PWD"], str_folderpath)
    all_files = readdir(folderpath)
    list_filenames = filter(x -> occursin(r"^.*\.pkl$", x), all_files)
    for filename in list_filenames
        filepath = joinpath(folderpath, filename)
        table_name = basename(filepath)
        file = pybuiltins.open(filepath, "rb")
        # df = CSV.read(filepath_csv, DataFrame)
        df = pandas.read_pickle(filepath)
        table_middle_name = split(table_name, ".")[1]
        dataframes[table_middle_name] = DataFrame(PyTable(df))
    end  # for
    return dataframes
end

"""
从文件夹中加载指定的 pkl 文件，返回一个字典。

# Args:
- `str_filepath::String`: 文件路径 ；

# Returns:
- `dataframes::dict`: 一个字典，字典的键是文件名的中间部分，字典的值是对应的 DataFrame ；

"""
function load_PKL_to_dict(str_filepath::String)
    pickle = pyimport("pickle")
    filepath = joinpath(ENV["PWD"], str_filepath)
    file = pybuiltins.open(filepath, "rb")
    dict = pyconvert(Dict, pickle.load(file))
    return dict
end

"""
从文件加载指定的 csv 文件，返回一个二维数组。

# Args:
- `str_filepath::String`: 文件路径 ；

# Returns:
- `array2D::Array`: 一个二维数组 ；

"""
function load_CSV_to_array2D(str_filepath::String)
    df = CSV.read(str_filepath, DataFrame, header=false)  # 读取 CSV 文件到 DataFrame
    array2D = Matrix(df)  # 将 DataFrame 转换为二维数组
    return array2D
end

"""
从文件夹中加载指定的 pkl 文件，返回一个二维矩阵。

# Args:
- `str_filepath::String`: 文件路径 ；

# Returns:
- `array2D::Array`: 一个二维矩阵 ；

"""
function load_PKL_to_array2D(str_filepath::String)
    pickle = pyimport("pickle")
    filepath = joinpath(ENV["PWD"], str_filepath)
    file = pybuiltins.open(filepath, "rb")
    array2D = pyconvert(Array, pickle.load(file))
    return array2D
end


"""
判断是否数据类型是 PyPandasDataFrame，然后转换为 DataFrame 。

# Args:
- `value::Any`: 数据值；
"""
transform_PyPandasDataFrame_to_DataFrame!(value) = typeof(value) == PyPandasDataFrame ? DataFrame(PyTable(value)) : value
#     for (key, value) in dict
#         if typeof(value) == PyPandasDataFrame
#             dict[key] = DataFrame(PyTable(value))
#         end
#     end
#     return dict
# end



