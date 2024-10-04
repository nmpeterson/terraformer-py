from ._helpers import _flatten_multipolygon_rings, _orient_rings


class GeoJSONError(Exception):
    # Custom exception for GeoJSON formatting errors
    pass


def geojson_to_arcgis(geojson: dict, wkid: int = 4326, id_attribute: str = "OBJECTID") -> dict | list:
    """Recursively converts a GeoJSON object to an Esri JSON object

    Args:
        geojson (dict): Input GeoJSON object
        wkid (int, optional): WKID of the GeoJSON's spatial reference. Defaults to 4326 (WGS 84).
        id_attribute (str, optional): Name of output ID attribute. Defaults to "OBJECTID".

    Raises:
        GeoJSONError: If the GeoJSON object is invalid in some way. GeoJSON spec:
            <https://datatracker.ietf.org/doc/html/rfc7946>

    Returns:
        dict | list: An Esri JSON object (or list of objects if input is a FeatureCollection or GeometryCollection)
    """
    result = {}

    if not (geojson_object_type := geojson.get("type")):
        raise GeoJSONError("Missing/empty 'type' property")

    is_geometry_object = geojson_object_type in (
        "Point",
        "MultiPoint",
        "LineString",
        "MultiLineString",
        "Polygon",
        "MultiPolygon",
    )

    if is_geometry_object:
        result["spatialReference"] = {"wkid": wkid}
        if not (coordinates := geojson.get("coordinates")):
            raise GeoJSONError(f"Missing/empty 'coordinates' property on {geojson_object_type} object")
        if not isinstance(coordinates, list):
            raise GeoJSONError(f"Invalid 'coordinates' property: {coordinates}")

    if geojson_object_type == "Point":
        result["x"] = coordinates[0]
        result["y"] = coordinates[1]
        if len(coordinates) > 2:
            result["z"] = coordinates[2]

    elif geojson_object_type == "MultiPoint":
        result["points"] = coordinates[:]
        try:
            if coordinates[0][2] is not None:
                result["hasZ"] = True
        except IndexError:
            pass

    elif geojson_object_type == "LineString":
        result["paths"] = [coordinates[:]]
        try:
            if coordinates[0][2] is not None:
                result["hasZ"] = True
        except IndexError:
            pass

    elif geojson_object_type == "MultiLineString":
        result["paths"] = coordinates[:]
        try:
            if coordinates[0][0][2] is not None:
                result["hasZ"] = True
        except IndexError:
            pass

    elif geojson_object_type == "Polygon":
        result["rings"] = _orient_rings(coordinates[:])
        try:
            if coordinates[0][0][2] is not None:
                result["hasZ"] = True
        except IndexError:
            pass

    elif geojson_object_type == "MultiPolygon":
        result["rings"] = _flatten_multipolygon_rings(coordinates[:])
        try:
            if coordinates[0][0][0][2] is not None:
                result["hasZ"] = True
        except IndexError:
            pass

    elif geojson_object_type == "Feature":
        try:
            geometry = geojson["geometry"]
        except KeyError as e:
            raise GeoJSONError("Missing 'geometry' property on Feature object") from e
        try:
            properties = geojson["properties"]
        except KeyError as e:
            raise GeoJSONError("Missing 'properties' property on Feature object") from e
        if geometry:
            result["geometry"] = geojson_to_arcgis(geometry, wkid, id_attribute)
        if properties:
            result["attributes"] = properties.copy()
        if id_val := geojson.get("id"):
            if "attributes" not in result:
                result["attributes"] = {}
            result["attributes"][id_attribute] = id_val

    elif geojson_object_type == "FeatureCollection":
        if not (features := geojson.get("features")):
            raise GeoJSONError("Missing/empty 'features' property on FeatureCollection object")
        result = [geojson_to_arcgis(feature, wkid, id_attribute) for feature in features]

    elif geojson_object_type == "GeometryCollection":
        if not (geometries := geojson.get("geometries")):
            raise GeoJSONError("Missing/empty 'geometries' property on GeometryCollection object")
        result = [geojson_to_arcgis(geometry, wkid, id_attribute) for geometry in geometries]

    else:
        raise GeoJSONError(f"Invalid 'type' property: {geojson_object_type}")

    return result
