from typing import TypeAlias

Point: TypeAlias = list[float]  # [x, y, ?z]
MultiPoint: TypeAlias = list[Point]
LineString: TypeAlias = list[Point]
MultiLineString: TypeAlias = list[LineString]
Polygon: TypeAlias = list[LineString]
MultiPolygon: TypeAlias = list[Polygon]


def points_equal(a: Point, b: Point) -> bool:
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
