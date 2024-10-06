import json
import unittest

from terraformer.arcgis import arcgis_to_geojson


class TestArcGISToGeoJSON(unittest.TestCase):

    def test_exists(self):
        """Function arcgis_to_geojson() should exist"""
        self.assertTrue(arcgis_to_geojson)

    def test_point(self):
        """Should convert an ArcGIS Point to a GeoJSON Point"""
        in_json = {"x": -66.796875, "y": 20.0390625, "spatialReference": {"wkid": 4326}}
        output = arcgis_to_geojson(in_json)
        self.assertEqual(output, {"type": "Point", "coordinates": [-66.796875, 20.0390625]})

    def test_point_z(self):
        """Should convert an ArcGIS Point to a GeoJSON Point and include z values"""
        in_json = {"x": -66.796875, "y": 20.0390625, "z": 1, "spatialReference": {"wkid": 4326}}
        output = arcgis_to_geojson(in_json)
        self.assertEqual(output, {"type": "Point", "coordinates": [-66.796875, 20.0390625, 1]})

    def test_null_island(self):
        """Should convert an ArcGIS Null Island to a GeoJSON Point"""
        in_json = {"x": 0, "y": 0, "spatialReference": {"wkid": 4326}}
        output = arcgis_to_geojson(in_json)
        self.assertEqual(output, {"type": "Point", "coordinates": [0, 0]})

    def test_empty_point(self):
        """Should not pass along geometry when nothing valid is encountered in in_json"""
        in_json = {"geometry": {"x": "NaN", "y": "NaN"}, "attributes": {"foo": "bar"}}
        output = arcgis_to_geojson(in_json)
        self.assertEqual(output, {"type": "Feature", "geometry": None, "properties": {"foo": "bar"}})

    def test_polyline(self):
        """Should convert an ArcGIS Polyline to a GeoJSON LineString"""
        in_json = {
            "paths": [[[6.6796875, 47.8125], [-65.390625, 52.3828125], [-52.3828125, 42.5390625]]],
            "spatialReference": {"wkid": 4326},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "LineString",
                "coordinates": [[6.6796875, 47.8125], [-65.390625, 52.3828125], [-52.3828125, 42.5390625]],
            },
        )

    def test_polyline_z(self):
        """Should convert an ArcGIS Polyline to a GeoJSON LineString and include z values"""
        in_json = {
            "paths": [[[6.6796875, 47.8125, 1], [-65.390625, 52.3828125, 1], [-52.3828125, 42.5390625, 1]]],
            "hasZ": True,
            "spatialReference": {"wkid": 4326},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "LineString",
                "coordinates": [[6.6796875, 47.8125, 1], [-65.390625, 52.3828125, 1], [-52.3828125, 42.5390625, 1]],
            },
        )

    def test_polygon(self):
        """Should convert an ArcGIS Polygon to a GeoJSON Polygon"""
        in_json = {
            "rings": [[[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]],
            "spatialReference": {"wkid": 4326},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "Polygon",
                "coordinates": [
                    [[41.8359375, 71.015625], [21.796875, 36.5625], [56.953125, 33.75], [41.8359375, 71.015625]]
                ],
            },
        )

    def test_polygon_z(self):
        """Should convert an ArcGIS Polygon to a GeoJSON Polygon and include z values"""
        in_json = {
            "rings": [
                [[41.8359375, 71.015625, 1], [56.953125, 33.75, 1], [21.796875, 36.5625, 1], [41.8359375, 71.015625, 1]]
            ],
            "hasZ": True,
            "spatialReference": {"wkid": 4326},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [41.8359375, 71.015625, 1],
                        [21.796875, 36.5625, 1],
                        [56.953125, 33.75, 1],
                        [41.8359375, 71.015625, 1],
                    ]
                ],
            },
        )

    def test_polygon_close_rings(self):
        """Should close rings when converting an ArcGIS Polygon to a GeoJSON Polygon"""
        in_json = {
            "rings": [[[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625]]],
            "spatialReference": {"wkid": 4326},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "Polygon",
                "coordinates": [
                    [[41.8359375, 71.015625], [21.796875, 36.5625], [56.953125, 33.75], [41.8359375, 71.015625]]
                ],
            },
        )

    def test_multipoint(self):
        """Should convert an ArcGIS Multipoint to a GeoJSON MultiPoint"""
        in_json = {
            "points": [[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625]],
            "spatialReference": {"wkid": 4326},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {"type": "MultiPoint", "coordinates": [[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625]]},
        )

    def test_polyline_multi(self):
        """Should convert a ArcGIS Polyline to a GeoJSON MultiLineString"""
        in_json = {
            "paths": [[[41.8359375, 71.015625], [56.953125, 33.75]], [[21.796875, 36.5625], [41.8359375, 71.015625]]],
            "spatialReference": {"wkid": 4326},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "MultiLineString",
                "coordinates": [
                    [[41.8359375, 71.015625], [56.953125, 33.75]],
                    [[21.796875, 36.5625], [41.8359375, 71.015625]],
                ],
            },
        )

    def test_polygon_multi(self):
        """Should convert a ArcGIS Polygon to a GeoJSON MultiPolygon"""
        in_json = {
            "rings": [
                [
                    [-122.63, 45.52],
                    [-122.57, 45.53],
                    [-122.52, 45.50],
                    [-122.49, 45.48],
                    [-122.64, 45.49],
                    [-122.63, 45.52],
                    [-122.63, 45.52],
                ],
                [[-83, 35], [-74, 35], [-74, 41], [-83, 41], [-83, 35]],
            ],
            "spatialReference": {"wkid": 4326},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [-122.63, 45.52],
                            [-122.63, 45.52],
                            [-122.64, 45.49],
                            [-122.49, 45.48],
                            [-122.52, 45.5],
                            [-122.57, 45.53],
                            [-122.63, 45.52],
                        ]
                    ],
                    [[[-83, 35], [-74, 35], [-74, 41], [-83, 41], [-83, 35]]],
                ],
            },
        )

    def test_polygon_strip_invalid_rings(self):
        """Should strip invalid rings when converting ArcGIS Polygons to GeoJSON"""
        in_json = {
            "rings": [
                [
                    [-122.63, 45.52],
                    [-122.57, 45.53],
                    [-122.52, 45.50],
                    [-122.49, 45.48],
                    [-122.64, 45.49],
                    [-122.63, 45.52],
                    [-122.63, 45.52],
                ],
                [[-83, 35], [-74, 35], [-83, 35]],
            ],
            "spatialReference": {"wkid": 4326},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-122.63, 45.52],
                        [-122.63, 45.52],
                        [-122.64, 45.49],
                        [-122.49, 45.48],
                        [-122.52, 45.50],
                        [-122.57, 45.53],
                        [-122.63, 45.52],
                    ]
                ],
            },
        )

    def test_polygon_multi_close_rings(self):
        """Should properly close rings when converting an ArcGIS Polygon in a GeoJSON MultiPolygon"""
        in_json = {
            "rings": [
                [[-122.63, 45.52], [-122.57, 45.53], [-122.52, 45.50], [-122.49, 45.48], [-122.64, 45.49]],
                [[-83, 35], [-74, 35], [-74, 41], [-83, 41]],
            ],
            "spatialReference": {"wkid": 4326},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [-122.63, 45.52],
                            [-122.64, 45.49],
                            [-122.49, 45.48],
                            [-122.52, 45.5],
                            [-122.57, 45.53],
                            [-122.63, 45.52],
                        ]
                    ],
                    [[[-83, 35], [-74, 35], [-74, 41], [-83, 41], [-83, 35]]],
                ],
            },
        )

    def test_polygon_multi_holes(self):
        """Should parse an ArcGIS MultiPolygon with holes to a GeoJSON MultiPolygon"""
        in_json = {
            "rings": [
                [
                    [-100.74462180954974, 39.95017165502381],
                    [-94.50439384003792, 39.91647453608879],
                    [-94.41650267263967, 34.89313438177965],
                    [-100.78856739324887, 34.85708140996771],
                    [-100.74462180954974, 39.95017165502381],
                ],
                [
                    [-99.68993678392353, 39.341088433448896],
                    [-99.68993678392353, 38.24507658785885],
                    [-98.67919734199646, 37.86444431771113],
                    [-98.06395917020868, 38.210554846669694],
                    [-98.06395917020868, 39.341088433448896],
                    [-99.68993678392353, 39.341088433448896],
                ],
                [
                    [-96.83349180978595, 37.23732027507514],
                    [-97.31689323047635, 35.967330282988534],
                    [-96.5698183075912, 35.57512048069255],
                    [-95.42724211456674, 36.357601429255965],
                    [-96.83349180978595, 37.23732027507514],
                ],
                [
                    [-101.4916967324349, 38.24507658785885],
                    [-101.44775114873578, 36.073960493943744],
                    [-103.95263145328033, 36.03843312329154],
                    [-103.68895795108557, 38.03770050767439],
                    [-101.4916967324349, 38.24507658785885],
                ],
            ],
            "spatialReference": {"wkid": 4326},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [-100.74462180954974, 39.95017165502381],
                            [-100.78856739324887, 34.85708140996771],
                            [-94.41650267263967, 34.89313438177965],
                            [-94.50439384003792, 39.91647453608879],
                            [-100.74462180954974, 39.95017165502381],
                        ],
                        [
                            [-96.83349180978595, 37.23732027507514],
                            [-95.42724211456674, 36.357601429255965],
                            [-96.5698183075912, 35.57512048069255],
                            [-97.31689323047635, 35.967330282988534],
                            [-96.83349180978595, 37.23732027507514],
                        ],
                        [
                            [-99.68993678392353, 39.341088433448896],
                            [-98.06395917020868, 39.341088433448896],
                            [-98.06395917020868, 38.210554846669694],
                            [-98.67919734199646, 37.86444431771113],
                            [-99.68993678392353, 38.24507658785885],
                            [-99.68993678392353, 39.341088433448896],
                        ],
                    ],
                    [
                        [
                            [-101.4916967324349, 38.24507658785885],
                            [-103.68895795108557, 38.03770050767439],
                            [-103.95263145328033, 36.03843312329154],
                            [-101.44775114873578, 36.073960493943744],
                            [-101.4916967324349, 38.24507658785885],
                        ]
                    ],
                ],
            },
        )

    def test_polygon_holes_uncontained(self):
        """Should still parse holes outside the outer rings"""
        in_json = {
            "rings": [
                [[-122.45, 45.63], [-122.45, 45.68], [-122.39, 45.68], [-122.39, 45.63], [-122.45, 45.63]],
                [[-122.46, 45.64], [-122.4, 45.64], [-122.4, 45.66], [-122.46, 45.66], [-122.46, 45.64]],
            ]
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "Polygon",
                "coordinates": [
                    [[-122.45, 45.63], [-122.39, 45.63], [-122.39, 45.68], [-122.45, 45.68], [-122.45, 45.63]],
                    [[-122.46, 45.64], [-122.46, 45.66], [-122.4, 45.66], [-122.4, 45.64], [-122.46, 45.64]],
                ],
            },
        )

    def test_feature(self):
        """Should parse an ArcGIS Feature into a GeoJSON Feature"""
        in_json = {
            "geometry": {
                "rings": [[[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]],
                "spatialReference": {"wkid": 4326},
            },
            "attributes": {"foo": "bar"},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [[41.8359375, 71.015625], [21.796875, 36.5625], [56.953125, 33.75], [41.8359375, 71.015625]]
                    ],
                },
                "properties": {"foo": "bar"},
            },
        )

    def test_featureset(self):
        """Should convert ArcGIS FeatureSet to a GeoJSON FeatureCollection"""
        in_json = {
            "displayFieldName": "prop0",
            "geometryType": "esriGeometryPolygon",
            "fields": [
                {"name": "prop0", "type": "esriFieldTypeString", "alias": "prop0", "length": 20},
                {"name": "OBJECTID", "type": "esriFieldTypeOID", "alias": "OBJECTID"},
                {"name": "FID", "type": "esriFieldTypeDouble", "alias": "FID"},
            ],
            "spatialReference": {"wkid": 4326},
            "features": [
                {"geometry": {"x": 102, "y": 0.5}, "attributes": {"prop0": "value0", "OBJECTID": 0, "FID": 0}},
                {
                    "geometry": {"paths": [[[102, 0], [103, 1], [104, 0], [105, 1]]]},
                    "attributes": {"prop0": None, "OBJECTID": None, "FID": 1},
                },
                {
                    "geometry": {"rings": [[[100, 0], [100, 1], [101, 1], [101, 0], [100, 0]]]},
                    "attributes": {"prop0": None, "OBJECTID": 2, "FID": 30.25},
                },
            ],
        }
        output = arcgis_to_geojson(in_json, "prop0")
        self.assertEqual(
            output,
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
                        "properties": {"prop0": "value0", "OBJECTID": 0, "FID": 0},
                        "id": "value0",
                    },
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [[102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]],
                        },
                        "properties": {"prop0": None, "OBJECTID": None, "FID": 1},
                        "id": 1,
                    },
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]],
                        },
                        "properties": {"prop0": None, "OBJECTID": 2, "FID": 30.25},
                        "id": 2,
                    },
                ],
            },
        )

    def test_feature_objectid(self):
        """Should parse an ArcGIS Feature with OBJECTID into a GeoJSON Feature"""
        in_json = {
            "geometry": {
                "rings": [[[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]],
                "spatialReference": {"wkid": 4326},
            },
            "attributes": {"OBJECTID": 123},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [[41.8359375, 71.015625], [21.796875, 36.5625], [56.953125, 33.75], [41.8359375, 71.015625]]
                    ],
                },
                "properties": {"OBJECTID": 123},
                "id": 123,
            },
        )

    def test_feature_fid(self):
        """Should parse an ArcGIS Feature with FID into a GeoJSON Feature"""
        in_json = {
            "geometry": {
                "rings": [[[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]],
                "spatialReference": {"wkid": 4326},
            },
            "attributes": {"FID": 123},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [[41.8359375, 71.015625], [21.796875, 36.5625], [56.953125, 33.75], [41.8359375, 71.015625]]
                    ],
                },
                "properties": {"FID": 123},
                "id": 123,
            },
        )

    def test_feature_custom_id(self):
        """Should parse an ArcGIS Feature with custom ID into a GeoJSON Feature"""
        in_json = {
            "geometry": {
                "rings": [[[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]],
                "spatialReference": {"wkid": 4326},
            },
            "attributes": {"FooId": 123},
        }
        output = arcgis_to_geojson(in_json, "FooId")
        self.assertEqual(
            output,
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [[41.8359375, 71.015625], [21.796875, 36.5625], [56.953125, 33.75], [41.8359375, 71.015625]]
                    ],
                },
                "properties": {"FooId": 123},
                "id": 123,
            },
        )

    def test_feature_empty_attributes(self):
        """Should parse an ArcGIS Feature with empty attributes into a GeoJSON Feature"""
        in_json = {
            "geometry": {
                "rings": [[[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]],
                "spatialReference": {"wkid": 4326},
            },
            "attributes": {},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [[41.8359375, 71.015625], [21.796875, 36.5625], [56.953125, 33.75], [41.8359375, 71.015625]]
                    ],
                },
                "properties": None,
            },
        )

    def test_feature_no_attributes(self):
        """Should parse an ArcGIS Feature with no attributes property into a GeoJSON Feature"""
        in_json = {
            "geometry": {
                "rings": [[[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]],
                "spatialReference": {"wkid": 4326},
            }
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [[41.8359375, 71.015625], [21.796875, 36.5625], [56.953125, 33.75], [41.8359375, 71.015625]]
                    ],
                },
                "properties": None,
            },
        )

    def test_feature_no_geometry(self):
        """Should parse an ArcGIS Feature with no geometry property into a GeoJSON Feature"""
        in_json = {"attributes": {"foo": "bar"}}
        output = arcgis_to_geojson(in_json)
        self.assertEqual(output, {"type": "Feature", "geometry": None, "properties": {"foo": "bar"}})

    def test_feature_invalid_custom_id(self):
        """Should ignore an ID field that is not string or number"""
        in_json = {
            "geometry": {"x": -66.796875, "y": 20.0390625, "spatialReference": {"wkid": 4326}},
            "attributes": {"OBJECTID": 123, "some_field": {"not an number": "or a string"}},
        }
        with self.assertWarns(UserWarning):
            output = arcgis_to_geojson(in_json, "some_field")
        self.assertEqual(
            output,
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [-66.796875, 20.0390625]},
                "properties": {"OBJECTID": 123, "some_field": {"not an number": "or a string"}},
                "id": 123,  # fallback to OBJECTID
            },
        )

    def test_feature_custom_id_over_objectid(self):
        """Should use a custom ID field and not OBJECTID for when both are present"""
        in_json = {
            "geometry": {"x": -66.796875, "y": 20.0390625, "spatialReference": {"wkid": 4326}},
            "attributes": {"OBJECTID": 123, "otherIdField": 456},
        }
        output = arcgis_to_geojson(in_json, "otherIdField")
        self.assertEqual(
            output,
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [-66.796875, 20.0390625]},
                "properties": {"OBJECTID": 123, "otherIdField": 456},
                "id": 456,
            },
        )

    def test_feature_no_id(self):
        """Should not allow GeoJSON Feature with id: undefined"""
        in_json = {
            "geometry": {"x": -66.796875, "y": 20.0390625, "spatialReference": {"wkid": 4326}},
            "attributes": {"foo": "bar"},  # no 'OBJECTID' or 'FID' attribute
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [-66.796875, 20.0390625]},
                "properties": {"foo": "bar"},
                # no "id" key
            },
        )

    def test_point_custom_wkid(self):
        """Should warn when converting SRID other than 4326 without CRS attribute"""
        in_json = {"x": 392917.31, "y": 298521.34, "spatialReference": {"wkid": 27700}}
        with self.assertWarns(UserWarning):
            output = arcgis_to_geojson(in_json)
        self.assertEqual(output, {"type": "Point", "coordinates": [392917.31, 298521.34]})

    def test_input_unchanged(self):
        """Should not modify the original Esri JSON object"""
        in_json = {
            "geometry": {
                "rings": [[[41.8359375, 71.015625], [56.953125, 33.75], [21.796875, 36.5625], [41.8359375, 71.015625]]],
                "spatialReference": {"wkid": 4326},
            },
            "attributes": {"foo": "bar"},
        }
        original = json.dumps(in_json)
        arcgis_to_geojson(in_json)
        self.assertEqual(json.dumps(in_json), original)

    def test_envelope(self):
        """Should parse an ArcGIS Envelope into a GeoJSON Polygon"""
        in_json = {
            "xmax": -35.5078125,
            "ymax": 41.244772343082076,
            "xmin": -13.7109375,
            "ymin": 54.36775852406841,
            "spatialReference": {"wkid": 4326},
        }
        output = arcgis_to_geojson(in_json)
        self.assertEqual(
            output,
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-35.5078125, 41.244772343082076],
                        [-13.7109375, 41.244772343082076],
                        [-13.7109375, 54.36775852406841],
                        [-35.5078125, 54.36775852406841],
                        [-35.5078125, 41.244772343082076],
                    ]
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
