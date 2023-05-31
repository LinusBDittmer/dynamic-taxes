'''

PyTest Test class for loader.py

'''

import unittest
import subprocess
import dynamictaxes as dt

class TestLoader(unittest.TestCase):

    def setUp(self):
        dt.debug_init_configs()
        self.loader = dt.Loader()

    def tearDown(self):
        del self.loader

    def test_attributes(self):
        methods = ["reset", "load_from_dir", "load_from_json", "save_to_json"]
        variables = ["ta_spectrum"]
        for method in methods:
            self.assertTrue(hasattr(self.loader, method))
            self.assertTrue(callable(getattr(self.loader, method)))
        for variable in variables:
            self.assertTrue(hasattr(self.loader, variable))
            self.assertTrue(not callable(getattr(self.loader, variable)))

