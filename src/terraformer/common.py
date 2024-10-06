"""Shared Terraformer utility functions and type aliases"""

from typing import TypeAlias

PointCoords: TypeAlias = list[float]  # [x, y, ?z]
MultiPointCoords: TypeAlias = list[PointCoords]
LineStringCoords: TypeAlias = list[PointCoords]
MultiLineStringCoords: TypeAlias = list[LineStringCoords]
PolygonCoords: TypeAlias = list[LineStringCoords]
MultiPolygonCoords: TypeAlias = list[PolygonCoords]


def array_intersects_array(a: LineStringCoords, b: LineStringCoords) -> bool:
    """Checks if two arrays of coordinates intersect

    Args:
        a (LineStringCoords): First array of coordinates
        b (LineStringCoords): Second array of coordinates

    Returns:
        bool: True if arrays intersect, False if not
    """
    for i in range(len(a) - 1):
        for j in range(len(b) - 1):
            if _edge_intersects_edge(a[i], a[i + 1], b[j], b[j + 1]):
                return True
    return False


def coordinates_contain_point(coordinates: LineStringCoords, point: PointCoords) -> bool:
    """Check if a point is contained within an array of coordinates

    Args:
        coordinates (LineStringCoords): Array of coordinates
        point (PointCoords): Point to check

    Returns:
        bool: True if point is contained, False if not
    """
    contains = False
    x_p, y_p, *_ = point
    for i in range(n := len(coordinates)):
        j = (i - 1) % n
        x_i, y_i, *_ = coordinates[i]
        x_j, y_j, *_ = coordinates[j]
        if ((y_i <= y_p and y_p < y_j) or (y_j <= y_p and y_p < y_i)) and (
            x_p < (x_j - x_i) * (y_p - y_i) / (y_j - y_i) + x_i
        ):
            contains = not contains
    return contains


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


def _edge_intersects_edge(a1: PointCoords, a2: PointCoords, b1: PointCoords, b2: PointCoords) -> bool:
    """Checks if two edges intersect

    Args:
        a1 (PointCoords): Start of first edge
        a2 (PointCoords): End of first edge
        b1 (PointCoords): Start of second edge
        b2 (PointCoords): End of second edge

    Returns:
        bool: True if edges intersect, False if not
    """
    x_a1, y_a1, *_ = a1
    x_a2, y_a2, *_ = a2
    x_b1, y_b1, *_ = b1
    x_b2, y_b2, *_ = b2

    uaT = (x_b2 - x_b1) * (y_a1 - y_b1) - (y_b2 - y_b1) * (x_a1 - x_b1)
    ubT = (x_a2 - x_a1) * (y_a1 - y_b1) - (y_a2 - y_a1) * (x_a1 - x_b1)
    uB = (y_b2 - y_b1) * (x_a2 - x_a1) - (x_b2 - x_b1) * (y_a2 - y_a1)

    if uB != 0:
        ua = uaT / uB
        ub = ubT / uB
        if ua >= 0 and ua <= 1 and ub >= 0 and ub <= 1:
            return True
    return False
