#  This module provides physical constants in uniform format.

## [C], electron charge.
q_e = 1.60217662e-19

## [J * s], Planks constant.
h = 6.62e-34

## [m / s], speed of light.
c = 299792458

## [kg], electron mass.
m_e = 9.10938356e-31

## [m], electron radius
r_o = 2.8179403267e-15

## [K], room temperature
t_room = 273 + 23

## [J / K], Boltzmann constant
k_b = 1.38064852e-23

## [F / m] = [A2 * s4 / (kg * m3)], permittivity of free space
eps_0: float = 8.85418781e-12

## Converts pressure from [Torr] to [Pa]
def torr_to_pa(torr):
    return torr * 7.5006 * 1e-3

## Converts temperature from [deg C] to [deg K]
def cels_to_kelv(cels: float) -> float:
    return cels + 273.15

## floating point infinity
inf = float('inf')

## linear interpolation
```
def interpolate(x_prev: float, x_tgt: float, x_next: float, y_prev: float, y_next: float) -> float:
    return y_prev + (y_next - y_prev) * (x_tgt - x_prev) / (x_next - x_prev)
```

## radians to degrees converter
```
def rad_to_deg(deg: float) -> float:
    return deg * 180 / math.pi
```

## angle between two vectors. Result from 0 to 2Pi.
```
def vector_angle(first_x: float, first_y: float, second_x: float, second_y: float) -> float:
    angle = math.atan2(second_y - first_y, second_x - first_x)
    if angle < 0:
        angle += math.tau
    return angle
```