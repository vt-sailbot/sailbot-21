import math
from src.utils.vec import Vec2


def true_wind(current_velocity):
    """Calculates the true wind from estimated apparent wind

    Keyword arguments:
    apparent_wind -- The apparent wind as a Vec2
    current_velocity -- The velocity as a Vec2
    t -- The time at which to estimate the true wind

    Returns:
    A Vec2 of the true wind
    """
    a = apparent_wind()  # Apparent wind
    v = current_velocity  # Current velocity
    awa = a.angle()  # Apparent wind angle
    return math.sqrt(a ** 2
                     + v ** 2
                     - 2 * a * v * math.cos(awa))


def apparent_wind():
    """Calculates the apparent wind

    Returns:
    A Vec2 of the apparent wind
    """
    return Vec2(0, 0)
