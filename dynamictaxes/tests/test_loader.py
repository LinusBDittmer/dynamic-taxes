'''

PyTest Test class for loader.py

'''

import unittest
import subprocess
import dynamictaxes as dt

class TestLoader(unittest.TestCase):

    def setUp(self):
        dt.init_configs()
        self.loader = dt.Loader()
        self.loader2 = dt.Loader()

    def tearDown(self):
        subprocess.run(["rm", "-f", "content_temp.json"])
        del self.loader

    def test_load_json(self):
        self.loader.reset()
        self.loader.load_from_json("content.json")
        self.assertEqual(len(self.loader.ta_spectrum.esa_spectra), 100)

    def test_write_json(self):
        self.loader.reset()
        self.loader.load_from_json("content.json")
        self.loader.save_to_json("content_temp.json")
        self.loader2.load_from_json("content_temp.json")
        self.assertTrue(self.loader.ta_spectrum == self.loader2.ta_spectrum)


