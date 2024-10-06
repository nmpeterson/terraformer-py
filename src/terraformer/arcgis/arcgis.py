from warnings import warn

from terraformer.common import (
    LineStringCoords,
    MultiLineStringCoords,
    array_intersects_array,
    coordinates_contain_point,
)
from .helpers import close_ring, ring_is_clockwise


def arcgis_to_geojson(arcgis: dict, id_attribute: str = None) -> dict:
    """Recursively converts an Esri JSON object into a GeoJSON object

    Args:
        arcgis (dict): Esri JSON object
        id_attribute (str, optional): Name of ID attribute (default: None)

    Returns:
        dict: A GeoJSON object
    """
    geojson = {}

    if features := arcgis.get("features"):
        geojson["type"] = "FeatureCollection"
        geojson["features"] = []
        for feature in features:
            geojson["features"].append(arcgis_to_geojson(feature, id_attribute))

    if (x := arcgis.get("x")) and (y := arcgis.get("y")):
        if _is_number(x) and _is_number(y):
            geojson["type"] = "Point"
            geojson["coordinates"] = [x, y]
            if (z := arcgis.get("z")) and _is_number(z):
                geojson["coordinates"].append(z)

    if points := arcgis.get("points"):
        geojson["type"] = "MultiPoint"
        geojson["coordinates"] = points[:]

    if paths := arcgis.get("paths"):
        if len(paths) == 1:
            geojson["type"] = "LineString"
            geojson["coordinates"] = paths[0][:]
        else:
            geojson["type"] = "MultiLineString"
            geojson["coordinates"] = paths[:]

    if rings := arcgis.get("rings"):
        geojson = _convert_rings_to_geojson(rings)

    if (
        (xmin := arcgis.get("xmin"))
        and (ymin := arcgis.get("ymin"))
        and (xmax := arcgis.get("xmax"))
        and (ymax := arcgis.get("ymax"))
    ):
        if all(_is_number(v) for v in [xmin, ymin, xmax, ymax]):
            geojson["type"] = "Polygon"
            geojson["coordinates"] = [
                [
                    [xmax, ymax],
                    [xmin, ymax],
                    [xmin, ymin],
                    [xmax, ymin],
                    [xmax, ymax],
                ]
            ]

    if (geometry := arcgis.get("geometry")) or (attributes := arcgis.get("attributes")):
        geojson["type"] = "Feature"
        geojson["geometry"] = arcgis_to_geojson(geometry) if geometry else None
        geojson["properties"] = attributes.copy() if attributes else None
        if attributes:
            try:
                geojson["id"] = _get_id(attributes, id_attribute)
            except KeyError:
                pass  # Don't set an (optional) id

    # If no valid geometry was encountered
    if geojson.get("geometry") == {}:
        geojson["geometry"] = None

    if (
        (spatial_reference := arcgis.get("spatialReference"), {})
        and (wkid := spatial_reference.get("wkid"))
        and wkid != 4326
    ):
        warn(f"Object converted in non-standard CRS - {spatial_reference}")

    return geojson


def _coordinates_contain_coordinates(outer: LineStringCoords, inner: LineStringCoords) -> bool:
    """Check if `outer` coordinates contain `inner` coordinates

    Args:
        outer (LineStringCoords): Array of outer coordinates
        inner (LineStringCoords): Array of inner coordinates

    Returns:
        bool: True if `outer` contains `inner`, False if not
    """
    if not array_intersects_array(outer, inner):
        if coordinates_contain_point(outer, inner[0]):
            return True
    return False


def _convert_rings_to_geojson(rings: MultiLineStringCoords) -> dict:
    """Convert an array of Esri JSON rings into a GeoJSON Polygon or MultiPolygon object

    Args:
        rings (MultiLineStringCoords): Array of rings

    Returns:
        dict: GeoJSON Polygon or MultiPolygon object
    """
    outer_rings = []
    holes = []
    for ring in rings:
        ring = close_ring(ring[:])
        if len(ring) < 4:
            continue
        if ring_is_clockwise(ring):
            polygon = [ring[::-1]]  # wind outer rings counterclockwise for RFC 7946 compliance
            outer_rings.append(polygon)
        else:
            holes.append(ring[::-1])  # wind inner rings clockwise for RFC 7946 compliance

    # Loop over all outer rings and see if they contain our hole
    uncontained_holes = []
    while len(holes):
        hole = holes.pop()
        contained = False
        for i in range(len(outer_rings) - 1, 0, -1):
            outer_ring = outer_rings[i][0]
            if _coordinates_contain_coordinates(outer_ring, hole):
                outer_rings[i].append(hole)
                contained = True
                break
        if not contained:
            uncontained_holes.append(hole)

    # If any holes weren't matched using contains, try intersects
    while len(uncontained_holes):
        hole = uncontained_holes.pop()
        intersects = False
        for i in range(len(outer_rings) - 1, 0, -1):
            outer_ring = outer_rings[i][0]
            if array_intersects_array(outer_ring, hole):
                outer_rings[i].append(hole)
                intersects = True
                break
        if not intersects:
            outer_rings.append([hole[::-1]])

    if len(outer_rings) == 1:
        return {"type": "Polygon", "coordinates": outer_rings[0]}
    else:
        return {"type": "MultiPolygon", "coordinates": outer_rings}


def _get_id(attributes: dict, id_attribute: str = None) -> str | int | float:
    """Get the ID value from a dictionary of attributes

    Args:
        attributes (dict): Dictionary of attributes
        id_attribute (str, optional): Name of ID attribute. Defaults to None, in which case OBJECTID & FID are checked.

    Raises:
        KeyError: If no valid ID attribute is found, or value is not a string, int, or float

    Returns:
        str | int | float: ID value
    """
    for key in [id_attribute, "OBJECTID", "FID"]:
        if key and (id_val := attributes.get(key)) and isinstance(id_val, (str, int, float)):
            return id_val
    raise KeyError("No valid ID attribute found")


def _is_number(obj) -> bool:
    """Check if an object is a number (int or float)

    Args:
        obj: Object to check

    Returns:
        bool: True if `obj` is a number, False otherwise
    """
    return isinstance(obj, (int, float))
