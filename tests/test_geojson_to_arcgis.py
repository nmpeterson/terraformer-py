import json
import unittest

from terraformer.arcgis import geojson_to_arcgis


class TestGeoJSONToArcGIS(unittest.TestCase):

    def test_exists(self):
        """Function geojson_to_arcgis() should exist"""
        self.assertTrue(geojson_to_arcgis)

    def test_point(self):
        """Should convert a GeoJSON Point to an ArcGIS Point"""
        in_geojson = {"type": "Point", "coordinates": [-58.7109375, 47.4609375]}
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(output, {"x": -58.7109375, "y": 47.4609375, "spatialReference": {"wkid": 4326}})

    def test_point_z(self):
        """Should convert a GeoJSON Point to an ArcGIS Point and include z-values"""
        in_geojson = {"type": "Point", "coordinates": [-58.7109375, 47.4609375, 10]}
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(output, {"x": -58.7109375, "y": 47.4609375, "z": 10, "spatialReference": {"wkid": 4326}})

    def test_point_z0(self):
        """Should convert a GeoJSON Point to an ArcGIS Point and include a z-value of 0"""
        in_geojson = {"type": "Point", "coordinates": [-58.7109375, 47.4609375, 0]}
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(output, {"x": -58.7109375, "y": 47.4609375, "z": 0, "spatialReference": {"wkid": 4326}})

    def test_point_wkid(self):
        """Should convert a GeoJSON Point to an ArcGIS Point with a custom WKID"""
        in_geojson = {"type": "Point", "coordinates": [1.0, 2.0]}
        output = geojson_to_arcgis(in_geojson, wkid=3857)
        self.assertEqual(output, {"x": 1.0, "y": 2.0, "spatialReference": {"wkid": 3857}})

    def test_null_island(self):
        """Should convert a GeoJSON Null Island to an ArcGIS Point"""
        in_geojson = {"type": "Point", "coordinates": [0, 0]}
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(output, {"x": 0, "y": 0, "spatialReference": {"wkid": 4326}})

    def test_linestring(self):
        """Should convert a GeoJSON LineString to an ArcGIS Polyline"""
        in_geojson = {
            "type": "LineString",
            "coordinates": [[21.4453125, -14.0625], [33.3984375, -20.7421875], [38.3203125, -24.609375]],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "paths": [[[21.4453125, -14.0625], [33.3984375, -20.7421875], [38.3203125, -24.609375]]],
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_linestring_z(self):
        """Should convert a GeoJSON LineString to an ArcGIS Polyline and include z-values"""
        in_geojson = {
            "type": "LineString",
            "coordinates": [[21.4453125, -14.0625, 10], [33.3984375, -20.7421875, 15], [38.3203125, -24.609375, 12]],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "paths": [[[21.4453125, -14.0625, 10], [33.3984375, -20.7421875, 15], [38.3203125, -24.609375, 12]]],
                "hasZ": True,
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_polygon(self):
        """Should convert a GeoJSON Polygon to an ArcGIS Polygon"""
        in_geojson = {
            "type": "Polygon",
            "coordinates": [
                [[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]
            ],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "rings": [[[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]],
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_polygon_z(self):
        """Should convert a GeoJSON Polygon to an ArcGIS Polygon and include z-values"""
        in_geojson = {
            "type": "Polygon",
            "coordinates": [
                [
                    [41.8359375, 71.015625, 10],
                    [56.953125, 33.75, 15],
                    [21.796875, 36.5625, 12],
                    [41.8359375, 71.015625, 10],
                ]
            ],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "rings": [
                    [
                        [41.8359375, 71.015625, 10],
                        [56.953125, 33.75, 15],
                        [21.796875, 36.5625, 12],
                        [41.8359375, 71.015625, 10],
                    ]
                ],
                "hasZ": True,
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_polygon_hole(self):
        """Should convert a GeoJSON Polygon with a hole to an ArcGIS Polygon with 2 rings"""
        in_geojson = {
            "type": "Polygon",
            "coordinates": [
                [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
                [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]],
            ],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "rings": [
                    [[100.0, 0.0], [100.0, 1.0], [101.0, 1.0], [101.0, 0.0], [100.0, 0.0]],
                    [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]],
                ],
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_polygon_strip_invalid_rings(self):
        """Should strip invalid rings when converting a GeoJSON Polygon to an ArcGIS Polygon"""
        in_geojson = {
            "type": "Polygon",
            "coordinates": [
                [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
                [[100.2, 0.2], [100.8, 0.2], [100.2, 0.2]],
            ],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "rings": [[[100.0, 0.0], [100.0, 1.0], [101.0, 1.0], [101.0, 0.0], [100.0, 0.0]]],
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_polygon_close_rings(self):
        """Should close ring when converting a GeoJSON Polygon with a hole to an ArcGIS Polygon"""
        in_geojson = {
            "type": "Polygon",
            "coordinates": [
                [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0]],
                [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8]],
            ],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "rings": [
                    [[100.0, 0.0], [100.0, 1.0], [101.0, 1.0], [101.0, 0.0], [100.0, 0.0]],
                    [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]],
                ],
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_multipoint(self):
        """Should convert a GeoJSON MultiPoint to an ArcGIS Multipoint"""
        in_geojson = {
            "type": "MultiPoint",
            "coordinates": [[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625]],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "points": [[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625]],
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_multipoint_z(self):
        """Should convert a GeoJSON MultiPoint to an ArcGIS Multipoint and include z-values"""
        in_geojson = {
            "type": "MultiPoint",
            "coordinates": [[41.8359375, 71.015625, 10], [56.953125, 33.75, 15], [21.796875, 36.5625, 12]],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "points": [[41.8359375, 71.015625, 10], [56.953125, 33.75, 15], [21.796875, 36.5625, 12]],
                "hasZ": True,
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_multilinestring(self):
        """Should convert a GeoJSON MultiLineString to an ArcGIS Polyline"""
        in_geojson = {
            "type": "MultiLineString",
            "coordinates": [
                [[41.8359375, 71.015625], [56.953125, 33.75]],
                [[21.796875, 36.5625], [47.8359375, 71.015625]],
            ],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "paths": [
                    [[41.8359375, 71.015625], [56.953125, 33.75]],
                    [[21.796875, 36.5625], [47.8359375, 71.015625]],
                ],
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_multilinestring_z(self):
        """Should convert a GeoJSON MultiLineString to an ArcGIS Polyline"""
        in_geojson = {
            "type": "MultiLineString",
            "coordinates": [
                [[41.8359375, 71.015625, 10], [56.953125, 33.75, 15]],
                [[21.796875, 36.5625, 12], [47.8359375, 71.015625, 10]],
            ],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "paths": [
                    [[41.8359375, 71.015625, 10], [56.953125, 33.75, 15]],
                    [[21.796875, 36.5625, 12], [47.8359375, 71.015625, 10]],
                ],
                "hasZ": True,
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_multipolygon(self):
        """Should convert a GeoJSON MultiPolygon to an ArcGIS Polygon"""
        in_geojson = {
            "type": "MultiPolygon",
            "coordinates": [
                [[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]],
                [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]],
            ],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "rings": [
                    [[102.0, 2.0], [102.0, 3.0], [103.0, 3.0], [103.0, 2.0], [102.0, 2.0]],
                    [[100.0, 0.0], [100.0, 1.0], [101.0, 1.0], [101.0, 0.0], [100.0, 0.0]],
                ],
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_multipolygon_z(self):
        """Should convert a GeoJSON MultiPolygon to an ArcGIS Polygon and include z-values"""
        in_geojson = {
            "type": "MultiPolygon",
            "coordinates": [
                [[[102.0, 2.0, 10], [103.0, 2.0, 10], [103.0, 3.0, 10], [102.0, 3.0, 10], [102.0, 2.0, 10]]],
                [[[100.0, 0.0, 15], [101.0, 0.0, 15], [101.0, 1.0, 15], [100.0, 1.0, 15], [100.0, 0.0, 15]]],
            ],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "rings": [
                    [[102.0, 2.0, 10], [102.0, 3.0, 10], [103.0, 3.0, 10], [103.0, 2.0, 10], [102.0, 2.0, 10]],
                    [[100.0, 0.0, 15], [100.0, 1.0, 15], [101.0, 1.0, 15], [101.0, 0.0, 15], [100.0, 0.0, 15]],
                ],
                "hasZ": True,
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_multipolygon_hole(self):
        """Should convert a GeoJSON MultiPolygon with holes to an ArcGIS Polygon"""
        in_geojson = {
            "type": "MultiPolygon",
            "coordinates": [
                [[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]],
                [
                    [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
                    [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]],
                ],
            ],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "rings": [
                    [[102.0, 2.0], [102.0, 3.0], [103.0, 3.0], [103.0, 2.0], [102.0, 2.0]],
                    [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]],
                    [[100.0, 0.0], [100.0, 1.0], [101.0, 1.0], [101.0, 0.0], [100.0, 0.0]],
                ],
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_multipolygon_close_rings(self):
        """Should close rings when converting a GeoJSON MultiPolygon with holes to an ArcGIS Polygon"""
        in_geojson = {
            "type": "MultiPolygon",
            "coordinates": [
                [[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0]]],
                [
                    [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0]],
                    [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8]],
                ],
            ],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "rings": [
                    [[102.0, 2.0], [102.0, 3.0], [103.0, 3.0], [103.0, 2.0], [102.0, 2.0]],
                    [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]],
                    [[100.0, 0.0], [100.0, 1.0], [101.0, 1.0], [101.0, 0.0], [100.0, 0.0]],
                ],
                "spatialReference": {"wkid": 4326},
            },
        )

    def test_feature(self):
        """Should convert a GeoJSON Feature to an ArcGIS Feature"""
        in_geojson = {
            "type": "Feature",
            "id": "foo",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]
                ],
            },
            "properties": {"foo": "bar"},
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "geometry": {
                    "rings": [
                        [[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]
                    ],
                    "spatialReference": {"wkid": 4326},
                },
                "attributes": {"foo": "bar", "OBJECTID": "foo"},
            },
        )

    def test_feature_custom_id(self):
        """Should convert a GeoJSON Feature to an ArcGIS Feature with a custom ID"""
        in_geojson = {
            "type": "Feature",
            "id": "foo",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]
                ],
            },
            "properties": {"foo": "bar"},
        }
        output = geojson_to_arcgis(in_geojson, id_attribute="myId")
        self.assertEqual(
            output,
            {
                "geometry": {
                    "rings": [
                        [[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]
                    ],
                    "spatialReference": {"wkid": 4326},
                },
                "attributes": {"foo": "bar", "myId": "foo"},
            },
        )

    def test_feature_empty(self):
        """Should allow converting a GeoJSON Feature to an ArcGIS Feature with no properties or geometry"""
        in_geojson = {"type": "Feature", "id": "foo", "geometry": None, "properties": None}
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(output, {"attributes": {"OBJECTID": "foo"}})

    def test_feature_bbox(self):
        """Should convert a GeoJSON Feature with a bbox attribute to an ArcGIS Feature"""
        in_geojson = {
            "type": "Feature",
            "id": "foo",
            "bbox": [-10.0, -10.0, 10.0, 10.0],
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-10.0, -10.0], [10.0, -10.0], [10.0, 10.0], [-10.0, -10.0]]],
            },
            "properties": None,
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            {
                "geometry": {
                    "rings": [[[-10.0, -10.0], [10.0, 10.0], [10.0, -10.0], [-10.0, -10.0]]],
                    "spatialReference": {"wkid": 4326},
                },
                "attributes": {"OBJECTID": "foo"},
            },
        )

    def test_featurecollection(self):
        """Should convert a GeoJSON FeatureCollection to an array of ArcGIS Feature JSON"""
        in_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
                    "properties": {"prop0": "value0"},
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]],
                    },
                    "properties": {"prop0": "value0"},
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]],
                    },
                    "properties": {"prop0": "value0"},
                },
            ],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            [
                {
                    "geometry": {"x": 102, "y": 0.5, "spatialReference": {"wkid": 4326}},
                    "attributes": {"prop0": "value0"},
                },
                {
                    "geometry": {
                        "paths": [[[102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]]],
                        "spatialReference": {"wkid": 4326},
                    },
                    "attributes": {"prop0": "value0"},
                },
                {
                    "geometry": {
                        "rings": [[[100.0, 0.0], [100.0, 1.0], [101.0, 1.0], [101.0, 0.0], [100.0, 0.0]]],
                        "spatialReference": {"wkid": 4326},
                    },
                    "attributes": {"prop0": "value0"},
                },
            ],
        )

    def test_geometrycollection(self):
        """Should convert a GeoJSON GeometryCollection to an array of ArcGIS Geometries"""
        in_geojson = {
            "type": "GeometryCollection",
            "geometries": [
                {"type": "Polygon", "coordinates": [[[-95, 43], [-95, 50], [-90, 50], [-91, 42], [-95, 43]]]},
                {"type": "LineString", "coordinates": [[-89, 42], [-89, 50], [-80, 50], [-80, 42]]},
                {"type": "Point", "coordinates": [-94, 46]},
            ],
        }
        output = geojson_to_arcgis(in_geojson)
        self.assertEqual(
            output,
            [
                {
                    "rings": [[[-95, 43], [-95, 50], [-90, 50], [-91, 42], [-95, 43]]],
                    "spatialReference": {"wkid": 4326},
                },
                {"paths": [[[-89, 42], [-89, 50], [-80, 50], [-80, 42]]], "spatialReference": {"wkid": 4326}},
                {"x": -94, "y": 46, "spatialReference": {"wkid": 4326}},
            ],
        )

    def test_input_unchanged(self):
        """Should not modify the original GeoJSON object"""
        in_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
                    "properties": {"prop0": "value0"},
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]],
                    },
                    "properties": {"prop0": "value0"},
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]],
                    },
                    "properties": {"prop0": "value0"},
                },
            ],
        }
        original = json.dumps(in_geojson)
        geojson_to_arcgis(in_geojson)
        self.assertEqual(json.dumps(in_geojson), original)


if __name__ == "__main__":
    unittest.main()
