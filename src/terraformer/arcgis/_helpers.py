from terraformer.common import (
    LineStringCoords,
    MultiLineStringCoords,
    MultiPolygonCoords,
    PolygonCoords,
    points_equal,
)


def _close_ring(ring: LineStringCoords) -> LineStringCoords:
    """Checks if the first and last points of a ring are equal and closes the ring (i.e. ensures 1st and last points
    are identical)

    Args:
        ring (LineStringCoords): Input ring of coordinates

    Returns:
        LineStringCoords: Closed ring of coordinates
    """
    if not points_equal(ring[0], ring[-1]):
        return [*ring, ring[0]]
    return ring


def _ring_is_clockwise(ring: LineStringCoords) -> bool:
    """Determine if polygon ring coordinates are clockwise. clockwise signifies outer ring,
    counter-clockwise an inner ring or hole. This logic was found at
    <http://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order>

    Args:
        ring (LineStringCoords): Closed ring of coordinates

    Returns:
        bool: True if ring is clockwise, False if counter-clockwise
    """
    total = 0
    p1 = ring[0]
    for p2 in ring[1:]:
        total += (p2[0] - p1[0]) * (p2[1] + p1[1])
        p1 = p2
    return total >= 0


def _orient_rings(polygon: PolygonCoords) -> PolygonCoords:
    """Ensures that polygon's rings are oriented in the right direction for Esri JSON (i.e. outer rings are clockwise,
    holes are counterclockwise)

    Args:
        polygon (PolygonCoords): Input polygon to orient

    Returns:
        PolygonCoords: Correctly oriented polygon
    """
    output = []
    polygon = polygon[:]
    outer_ring = _close_ring(polygon.pop(0)[:])
    if len(outer_ring) >= 4:
        if not _ring_is_clockwise(outer_ring):
            outer_ring.reverse()
        output.append(outer_ring)
        for hole in polygon:
            hole = _close_ring(hole[:])
            if len(hole) >= 4:
                if _ring_is_clockwise(hole):
                    hole.reverse()
                output.append(hole)
    return output


def _flatten_multipolygon_rings(multipolygon: MultiPolygonCoords) -> MultiLineStringCoords:
    """Flattens holes in multipolygons to one array of polygons

    Args:
        multipolygon (MultiPolygonCoords): Input MultiPolygon to flatten

    Returns:
        MultiLineStringCoords: Flattened list of rings
    """
    output = []
    for polygon in multipolygon:
        clean_polygon = _orient_rings(polygon)
        for ring in clean_polygon[::-1]:
            output.append(ring[:])
    return output
