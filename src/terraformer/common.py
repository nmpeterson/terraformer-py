from typing import TypeAlias

PointCoords: TypeAlias = list[float]  # [x, y, ?z]
MultiPointCoords: TypeAlias = list[PointCoords]
LineStringCoords: TypeAlias = list[PointCoords]
MultiLineStringCoords: TypeAlias = list[LineStringCoords]
PolygonCoords: TypeAlias = list[LineStringCoords]
MultiPolygonCoords: TypeAlias = list[PolygonCoords]


def points_equal(a: PointCoords, b: PointCoords) -> bool:
    """Checks that two points are identical

    Args:
        a (Point): First point
        b (Point): Second point

    Returns:
        bool: True if points are identical, False if not
    """
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True
