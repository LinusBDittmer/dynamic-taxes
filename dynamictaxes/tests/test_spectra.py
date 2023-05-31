'''

PyTest Test class for loader.py

'''

import unittest
import dynamictaxes as dt

class TestESASpectrum(unittest.TestCase):

    def setUp(self):
        dt.debug_init_configs()
        self.esa_spectrum = dt.ExcitedStateAbsorptionSpectrum()

    def tearDown(self):
        del self.loader

    def test_attributes(self):
        methods = ["render", "evaluate", "col", "gaussian"]
        variables = ["state_num", "multiplicity", "time", "energies", "transition_moments", "excited_state_labels", "cmap", "norm"]
        for method in methods:
            self.assertTrue(hasattr(self.loader, method))
            self.assertTrue(callable(getattr(self.loader, method)))
        for variable in variables:
            self.assertTrue(hasattr(self.loader, variable))
            self.assertTrue(not callable(getattr(self.loader, variable)))

class TestTASpectrum(unittest.TestCase):

    def setUp(self):
        dt.init_configs()
        self.esa_spectrum = dt.ExcitedStateAbsorptionSpectrum()

    def tearDown(self):
        del self.loader

    def test_attributes(self):
        methods = ["render", "evaluate", "col", "gaussian"]
        variables = ["state_num", "multiplicity", "time", "energies", "transition_moments", "excited_state_labels", "cmap", "norm"]
        for method in methods:
            self.assertTrue(hasattr(self.loader, method))
            self.assertTrue(callable(getattr(self.loader, method)))
        for variable in variables:
            self.assertTrue(hasattr(self.loader, variable))
            self.assertTrue(not callable(getattr(self.loader, variable)))

