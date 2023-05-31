'''

PyTest Test class for loader.py

'''

import unittest
import subprocess
try:
    import dynamictaxes as dt
except:
    import dynamic-taxes as dt

class TestLoader(unittest.TestCase):

    def setUp(self):
        dt.init_configs()
        self.loader = dt.Loader()
        self.loader2 = dt.Loader()
        self.content = __file__[:__file__.rfind("/")+1] + "content.json"
        self.content2 = __file__[:__file__.rfind("/")+1] + "content_temp.json"

    def tearDown(self):
        subprocess.run(["rm", "-f", self.content2])
        del self.loader

    def test_load_json(self):
        self.loader.reset()
        self.loader.load_from_json(self.content)
        self.assertEqual(len(self.loader.ta_spectrum.esa_spectra), 100)

    def test_write_json(self):
        self.loader.reset()
        self.loader.load_from_json(self.content)
        self.loader.save_to_json(self.content2)
        self.loader2.load_from_json(self.content2)
        self.assertTrue(self.loader.ta_spectrum == self.loader2.ta_spectrum)


