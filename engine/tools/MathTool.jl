"""
数学计算工具
"""

"计算两点之间形成的向量之模长、角度"
calc_norm_angle(x_0::Float64, y_0::Float64, x_1::Float64, y_1::Float64) = √((x_1 - x_0)^2 + (y_1 - y_0)^2), atan((y_1 - y_0) / (x_1 - x_0))
calc_norm_angle(v_0::SVector{2,Float64}, v_1::SVector{2,Float64}) = norm(v_1 - v_0), atan(v_1[2] - v_0[2], v_1[1] - v_0[1])


"根据向量之模长、角度计算向量坐标"
calc_vector(r::Float64, ϕ::Float64) = (r * cos(ϕ), r * sin(ϕ))

"根据两点计算向量"
calc_vector(x_0::Float64, y_0::Float64, x_1::Float64, y_1::Float64) = [x_1 - x_0, y_1 - y_0]
calc_vector(p_0::SVector{2,Float64}, p_1::SVector{2,Float64}) = p_1 - p_0
# calc_vector(p_0::Tuple, p_1::Tuple) = (p_1[1] - p_0[1], p_1[2] - p_0[2])


