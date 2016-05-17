# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Author: Kyle Lahnakoski (kyle@lahnakoski.com)
#

from __future__ import unicode_literals
from __future__ import division

import base_test_class
from tests.base_test_class import ActiveDataBaseTest, global_settings, TEST_TABLE


class TestAggOps(ActiveDataBaseTest):

    def test_simplest(self):
        test = {
            "data": [{"a": i} for i in range(30)],
            "query": {
                "from": TEST_TABLE,
                "select": {"aggregate": "count"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 30
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["count"],
                "data": [[30]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "count": 30
                }
            }
        }
        self.utils.execute_es_tests(test)

    def test_max(self):
        test = {
            "data": [{"a": i*2} for i in range(30)],
            "query": {
                "from": TEST_TABLE,
                "select": {"value": "a", "aggregate": "max"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 58
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["a"],
                "data": [[58]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "a": 58
                }
            }
        }
        self.utils.execute_es_tests(test)


    def test_median(self):
        test = {
            "data": [{"a": i**2} for i in range(30)],
            "query": {
                "from": TEST_TABLE,
                "select": {"value": "a", "aggregate": "median"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 210.5
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["a"],
                "data": [[210.5]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "a": 210.5
                }
            }
        }
        self.utils.execute_es_tests(test)


    def test_percentile(self):
        test = {
            "data": [{"a": i**2} for i in range(30)],
            "query": {
                "from": TEST_TABLE,
                "select": {"value": "a", "aggregate": "percentile", "percentile": 0.90}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 681.3
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["a"],
                "data": [[681.3]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "a": 681.3
                }
            }
        }
        self.utils.execute_es_tests(test)

    def test_stats(self):
        test = {
            "data": [{"a": i**2} for i in range(30)],
            "query": {
                "from": TEST_TABLE,
                "select": {"value": "a", "aggregate": "stats"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": {
                    "count": 30,
                    "std": 259.76901064,
                    "min": 0,
                    "max": 841,
                    "sum": 8555,
                    "median": 210.5,
                    "sos": 4463999,
                    "var": 67479.93889,
                    "avg": 285.1666667
                }
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["a"],
                "data": [[{
                    "count": 30,
                    "std": 259.76901064,
                    "min": 0,
                    "max": 841,
                    "sum": 8555,
                    "median": 210.5,
                    "sos": 4463999,
                    "var": 67479.93889,
                    "avg": 285.1666667
                }]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "a": {
                        "count": 30,
                        "std": 259.76901064,
                        "min": 0,
                        "max": 841,
                        "sum": 8555,
                        "median": 210.5,
                        "sos": 4463999,
                        "var": 67479.93889,
                        "avg": 285.1666667
                    }
                }
            }
        }
        self.utils.execute_es_tests(test)

    def test_bad_percentile(self):
        test = {
            "data": [{"a": i**2} for i in range(30)],
            "query": {
                "from": TEST_TABLE,
                "select": {"value": "a", "aggregate": "percentile", "percentile": "0.90"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 681.3
            }
        }

        self.assertRaises("Expecting percentile to be a float", self.utils.execute_es_tests, test)

    def test_many_aggs_on_one_column(self):
        # ES WILL NOT ACCEPT TWO (NAIVE) AGGREGATES ON SAME FIELD, COMBINE THEM USING stats AGGREGATION
        test = {
            "data": [{"a": i*2} for i in range(30)],
            "query": {
                "from": TEST_TABLE,
                "select": [
                    {"name": "maxi", "value": "a", "aggregate": "max"},
                    {"name": "mini", "value": "a", "aggregate": "min"},
                    {"name": "count", "value": "a", "aggregate": "count"}
                ]
            },
            "expecting_list": {
                "meta": {"format": "value"},
                "data": {"mini": 0, "maxi": 58, "count": 30}
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["mini", "maxi", "count"],
                "data": [
                    [0, 58, 30]
                ]
            }
        }
        self.utils.execute_es_tests(test)


    def test_simplest_on_value(self):
        test = {
            "data": range(30),
            "query": {
                "from": TEST_TABLE,
                "select": {"aggregate": "count"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 30
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["count"],
                "data": [[30]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "count": 30
                }
            }
        }
        self.utils.execute_es_tests(test, tjson=True)

    def test_max_on_value(self):
        test = {
            "data": [{"a": i*2} for i in range(30)],
            "query": {
                "from": TEST_TABLE,
                "select": {"value": ".", "aggregate": "max"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 58
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["max"],
                "data": [[58]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "max": 58
                }
            }
        }
        self.utils.execute_es_tests(test, tjson=True)


    def test_max_object_on_value(self):
        test = {
            "data": [{"a": i*2} for i in range(30)],
            "query": {
                "from": TEST_TABLE,
                "select": [{"value": ".", "aggregate": "max"}]
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": {"max": 58}
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["max"],
                "data": [[58]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "max": 58
                }
            }
        }
        self.utils.execute_es_tests(test, tjson=True)


    def test_median_on_value(self):
        test = {
            "data": [i**2 for i in range(30)],
            "query": {
                "from": TEST_TABLE,
                "select": {"value": ".", "aggregate": "median"}
            },
            "expecting_list": {
                "meta": {"format": "value"}, "data": 210.5
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["median"],
                "data": [[210.5]]
            },
            "expecting_cube": {
                "meta": {"format": "cube"},
                "edges": [],
                "data": {
                    "median": 210.5
                }
            }
        }
        self.utils.execute_es_tests(test, tjson=True)


    def test_many_aggs_on_value(self):
        # ES WILL NOT ACCEPT TWO (NAIVE) AGGREGATES ON SAME FIELD, COMBINE THEM USING stats AGGREGATION
        test = {
            "data": [i*2 for i in range(30)],
            "query": {
                "from": TEST_TABLE,
                "select": [
                    {"name": "maxi", "value": ".", "aggregate": "max"},
                    {"name": "mini", "value": ".", "aggregate": "min"},
                    {"name": "count", "value": ".", "aggregate": "count"}
                ]
            },
            "expecting_list": {
                "meta": {"format": "value"},
                "data": {"mini": 0, "maxi": 58, "count": 30}
            },
            "expecting_table": {
                "meta": {"format": "table"},
                "header": ["mini", "maxi", "count"],
                "data": [
                    [0, 58, 30]
                ]
            }
        }
        self.utils.execute_es_tests(test, tjson=True)

    def test_cardinality(self):
        test = {
            "data": [
                {"a": 1, "b": "x"},
                {"a": 1, "b": "x"},
                {"a": 2, "b": "x"},
                {"a": 2, "d": "x"},
                {"a": 3, "d": "x"},
                {"a": 3, "d": "x"},
                {"a": 3, "d": "x"},
            ],
            "query": {
                "from": TEST_TABLE,
                "select": [
                    {"value": "a", "aggregate": "cardinality"},
                    {"value": "b", "aggregate": "cardinality"},
                    {"value": "c", "aggregate": "cardinality"},
                    {"value": "d", "aggregate": "cardinality"}
                ]
            },
            "expecting_list": {
                "meta": {"format": "value"},
                "data": {"a": 3, "b": 1, "c": 0, "d": 1}
            }
        }
        self.utils.execute_es_tests(test, tjson=False)

    def test_union(self):
        test = {
            "data": [
                {"b": "a"},
                {"b": "b"},
                {"b": "c"},
                {"b": "d"},
                {"b": "e"},
                {"b": "f"},
                {"b": "g"},
                {"b": "h"},
                {"b": "i"},
                {"b": "j"},
                {"b": "x"},
                {"b": "x"},
                {"b": "x"},
                {"b": "y"},
                {"b": "y"},
                {"b": "y"},
                {"b": "z"},
            ],
            "query": {
                "from": TEST_TABLE,
                "select": [
                    {"value": "b", "aggregate": "union"}
                ]
            },
            "expecting_list": {
                "meta": {"format": "value"},
                "data": {"b": ["x", "y", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "z"]}
            }
        }
        self.utils.execute_es_tests(test, tjson=False)
