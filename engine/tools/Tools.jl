"""
各种工具集
"""

"""
按照指定的层级压平字典。

# Args:
- `dict::Dict`: 要压平的字典
- `depth::Int`: 指定的压平到的层级
- `parent_key::String`: 父键
- `sep::String`: 分隔符
- `current_depth::Int`: 当前层级

Returns:
    压平后的字典

Example:
```Julia
# 定义一个嵌套的字典
nested_dict = Dict("a" => Dict("b" => 1, "c" => Dict("d" => 2, "e" => 3)), "f" => 4)

# 使用 flatten_dict 函数将嵌套的字典扁平化
flattened_dict = flatten_dict(nested_dict, 1)

# 打印扁平化后的字典
println(flattened_dict) 
```
结果是
```
Dict{Symbol, Int64} with 4 entries:
  :f     => 4
  :a_b   => 1
  :a_c_e => 3
  :a_c_d => 2
```

"""
function flatten_dict(dict::Dict, depth::Int, parent_key="", sep="_", current_depth=1)
    items = []
    for (k, v) in dict
        new_key = parent_key != "" ? "$parent_key$sep$k" : k
        if typeof(v) <: Dict && current_depth < depth
            items = append!(items, flatten_dict(v, depth, new_key, sep, current_depth + 1))
        else
            push!(items, (new_key => v))
        end
    end
    return Dict(items)
end

"""
转换字典之键名类型从 String 为 Symbol 类型。

如果键名中有空格，则将空格替换为下划线。如果键值类型是 Path 类型，则不转换。

# Args:
- `dict::Dict`: 要转换的字典

Returns:
    转换后的字典
"""
function transform_dict_key_to_symbol(dict::Dict)
    new_dict = Dict{Symbol,Any}()
    for (key, value) in dict
        modified_key = replace(key, " " => "_")  # 将键名中的空格替换为下划线
        new_dict[Symbol(modified_key)] = value
    end
    return new_dict
end


"""
转换字典中数据类型为 String 的键值为 Path 类型别名。

# Args:
- `dict::Dict`: 要转换的字典

Returns:
    转换后的字典

"""
function transform_string_to_path_in_a_dict(dict::Dict)
    for (key, value) in dict
        if (startswith(key, "folderpath_") || startswith(key, "filepath_")) && typeof(value) == String
            # dict[key] = Path(value)
            dict[key] = joinpath(value)::Path
        end
    end
    return dict
end


"""
转换 DataFrame 中的列名与列中的字符串为 Symbol 类型。

# Args:
- `df::DataFrame`: 要转换的 DataFrame

Returns:
    转换后的 DataFrame

"""
function transform_String_type_to_Symbol_type_in_a_DataFrame(df::DataFrame)
    # 将列名转换为 Symbol 类型
    rename!(df, Symbol.(names(df)))

    # 遍历每一列
    for col in names(df)
        # 如果列中的值是 String 类型，则将其转换为 Symbol 类型
        if eltype(df[!, col]) == String
            df[!, col] = map(Symbol, df[!, col])
        end
    end

    return df
end


"""
转换字典之键名键值之数据类型类型。

转换内容包括：
1. 转换 PyPandasDataFrame 为 DataFrame；
2. 转换字典中数据类型为 String 的键值为 Path 类型别名；
3. 转换每一个类型为 DataFrame 的键值从 String 类型到 Symbol 类型；
4. 转换字典之 String 类型的键名为 Symbol 类型；


# Args:
- `dict::Dict`: 要转换的字典

Returns:
    转换后的字典

"
"""
function transform_key_and_values_types_in_a_dict(dict::Dict)

    # 遍历字典键值，转换 PyPandasDataFrame 为 DataFrame。
    for (key, value) in dict
        if typeof(value) == PyPandasDataFrame
            dict[key] = transform_PyPandasDataFrame_to_DataFrame!(value)
        end
    end

    # 转换字典中数据类型为 String 的键值为 Path 类型别名
    dict = transform_string_to_path_in_a_dict(dict)

    # 转换每一个类型为 DataFrame 的键值从 String 类型到 Symbol 类型
    for (key, value) in dict
        if typeof(value) == DataFrame
            dict[key] = transform_String_type_to_Symbol_type_in_a_DataFrame(value)
        end
    end

    # 转换字典之 String 类型的键名为 Symbol 类型
    dict = transform_dict_key_to_symbol(dict)

    # 遍历字典键值，转换字典中数据类型为 Python 之 PosixPath 的键值为 Julia 之 Path 类型别名
    pathlib = pyimport("pathlib")
    for (key, value) in dict
        if pyisinstance(value, pathlib.Path)
            dict[key] = joinpath(value)::Path
        end
    end


    return dict
end



"""
将待输出的消息同时写入到文件和控制台，并强制写入硬盘。

# Args:
- `content::String`: 要写入的消息

Returns:
    写入的消息。同时实时写入到文件、输出到控制台
"""
macro print_to_file_and_console(content)
    # if globals[:is_test]
    return esc(
        quote
            write(file_outputlog_txt, $(content))
            write(file_outputlog_txt, "\n")
            println($(content))
        end
    )
    # end
end

