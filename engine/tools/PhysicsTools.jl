"""
物理学工具
"""


"""
根据入射向量、法向向量计算反射向量

# Args:
- `v::SVector{2,Float64}`: 入射向量
- `n::SVector{2,Float64}`: 法向向量

# Returns:
- `v_reflected::`: 反射向量
"""
function reflect_vector(v, n)
    n = n / norm(n)
    # R = I - 2 * n * n'
    v_reflected = v - 2 * dot(v, n) * n

    return v_reflected
end


"根据正负值反转角度（正的不变，反的反转）"
reverse_angle(ϕ::Float64, z::Int) = ϕ += z == -1 ? π : 0



"""
根据力计算加速度

# Args:
- `f::SVector{2,Float64}`: 分力
- `m::Float`: 质量

# Returns:
- `a::SVector{2,Float64}`: 分加速度
"""
calc_acceleration_by_force(f::SVector{2,Float64}, m::Float64) = f ./ m

# """
# 根据力计算加速度

# # Args:
# - `f::Tuple`: 分力
# - `m::Float`: 质量

# # Returns:
# - `a::Tuple`: 分加速度
# """
# calc_acceleration_by_force(f::Tuple, m::Float64) = (f[1] / m, f[2] / m)


"""
根据分加速度变动计算合速度

# Args:
- `Δa::SVector{2,Float64}`: 分加速度变动量
- `dt::Float64`: 时间间隔
- `v::SVector{2,Float64}`: 速度

# Returns:
- `v::SVector{2,Float64}`: 速度
"""
function update_velocity_by_component_acceleration_changed(Δa::SVector{2,Float64}, dt::Float64, v::SVector{2,Float64})
    v += Δa .* dt
    return v
end

# """
# 根据分加速度变动计算合速度

# # Args:
# - `Δa::Tuple`: 分加速度变动量
# - `dt::Float64`: 时间间隔
# - `velocity::Tuple`: 速度

# # Returns:
# - `v::Tuple`: 速度
# """
# function update_velocity_by_component_acceleration_changed(Δa::Tuple, dt::Float64, velocity::Tuple)
#     v1 = velocity[1] + Δa[1] * dt
#     v2 = velocity[2] + Δa[2] * dt
#     return (v1, v2)
# end


# """
# 计算个体施力

# # Args:
# - `pos1::Tuple`: 个体1位置
# - `pos2::Tuple`: 个体2位置
# - `force_value::Float`: 力值
# - `force_axial::Float`: 轴向力
# - `force_radial::Float`: 径向力
# - `force_torsional::Float`: 扭向力

# # Returns:
# - `force::Tuple`: 个体施加的力
# """
# function agents_interaction_calculate_force(pos1::Tuple, pos2::Tuple, force_value::Float64, force_axial::Float64, force_radial::Float64, force_torsional::Float64)
#     force = calc_vector(pos1, pos2)
#     force = (force_value * force_axial * force[1], force_value * force_axial * force[2])    #TODO 需要补充径向、扭向力影响
#     return force
# end


"""
计算个体施力

# Args:
- `pos1::SVector{2,Float64}`: 个体1位置
- `pos2::SVector{2,Float64}`: 个体2位置
- `force_value::Float`: 力值
- `force_axial::Float`: 轴向力
- `force_radial::Float`: 径向力
- `force_torsional::Float`: 扭向力

# Returns:
- `force::SVector{2,Float64}`: 个体施加的力
"""
function agents_interaction_calculate_force(pos1::SVector{2,Float64}, pos2::SVector{2,Float64}, force_value::Float64, force_axial::Float64, force_radial::Float64, force_torsional::Float64)
    force = calc_vector(pos1, pos2)
    force *= force_value * force_axial   #TODO 需要补充径向、扭向力影响
    return force
end


# """
# 根据所受的分力变动更新计算个体所受合力

# # Args:
# - `f_net::NTuple{2,Float64}`: 更新前所受的合力
# - `Δf_component::NTuple{2,Float64}`: 所受的分力变动量

# # Returns:
# - `f_net::NTuple{2,Float64}`: 更新后所受的合力
# """
# update_net_force_by_component_changed(f_net::NTuple{2,Float64}, Δf_component::NTuple{2,Float64}) = (f_net[1] + Δf_component[1], f_net[2] + Δf_component[2])

"""
根据所受的分力变动更新计算个体所受合力

# Args:
- `f_net::SVector{2,Float64}`: 更新前所受的合力
- `Δf_component::SVector{2,Float64}`: 所受的分力变动量

# Returns:
- `f_net::SVector{2,Float64}`: 更新后所受的合力
"""
update_net_force_by_component_changed(f_net::SVector{2,Float64}, Δf_component::SVector{2,Float64}) = f_net + Δf_component

# """
# 根据力之邻接矩阵计算个体所受合力

# # Args:
# - `agent_id::Int`: 个体 ID
# - `adjacency_matrix_x::SparseMatrixCSC{Float64,Int}`: 力之 x 方向邻接矩阵
# - `adjacency_matrix_y::SparseMatrixCSC{Float64,Int}`: 力之 y 方向邻接矩阵

# # Returns:
# - `f_net::NTuple{2,Float64}`: 个体所受合力
# """
# function calc_net_force(agent_id::Int, adjacency_matrix_x::SparseMatrixCSC{Float64,Int}, adjacency_matrix_y::SparseMatrixCSC{Float64,Int})
#     f_net = (sum(adjacency_matrix_x[:, agent_id]), sum(adjacency_matrix_y[:, agent_id]))
#     return f_net
# end

"""
根据力之邻接矩阵计算个体所受合力

# Args:
- `agent_id::Int`: 个体 ID
- `adjacency_matrix_x::SparseMatrixCSC{Float64,Int}`: 力之 x 方向邻接矩阵
- `adjacency_matrix_y::SparseMatrixCSC{Float64,Int}`: 力之 y 方向邻接矩阵

# Returns:
- `f_net::SVector{2,Float64}`: 个体所受合力
"""
function calc_net_force(agent_id::Int, adjacency_matrix_x::SparseMatrixCSC{Float64,Int}, adjacency_matrix_y::SparseMatrixCSC{Float64,Int})
    f_net = @SVector [sum(adjacency_matrix_x[:, agent_id]), sum(adjacency_matrix_y[:, agent_id])]
    return f_net
end


