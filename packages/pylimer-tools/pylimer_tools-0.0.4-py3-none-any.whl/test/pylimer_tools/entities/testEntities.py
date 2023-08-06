
import unittest

import pandas as pd
import pandas.testing as pd_testing
from pylimer_tools.calc.calculateBondLen import (calculateBondLen,
                                                 calculateMeanBondLen)
from pylimer_tools.entities.molecule import Molecule
from pylimer_tools.entities.universum import Universum


class TestEntities(unittest.TestCase):

    def assertSeriesEqual(self, a, b, msg):
        try:
            pd_testing.assert_series_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def setUp(self):
        self.addTypeEqualityFunc(pd.Series, self.assertSeriesEqual)

    testAtoms = pd.DataFrame([
        {"id": 1, "nx": 1, "ny": 1, "nz": 1,
            "type": 1, "x": 1, "y": 1, "z": 1},
        {"id": 2, "nx": 1, "ny": 1, "nz": 1,
            "type": 1, "x": 2, "y": 1, "z": 1},
        {"id": 3, "nx": 1, "ny": 1, "nz": 1,
            "type": 1, "x": 3, "y": 1, "z": 1},
        {"id": 5, "nx": 1, "ny": 1, "nz": 1,
            "type": 1, "x": 1, "y": 3, "z": 1},
        {"id": 6, "nx": 1, "ny": 1, "nz": 1,
            "type": 2, "x": 1, "y": 1, "z": 2},
        {"id": 7, "nx": 1, "ny": 1, "nz": 1,
            "type": 2, "x": 1, "y": 1, "z": 3},
    ])
    testBonds = pd.DataFrame([
        {"to": 1, "bondFrom": 2},
        {"to": 3, "bondFrom": 2},
        {"to": 5, "bondFrom": 6},
        {"to": 6, "bondFrom": 7}
    ])

    def test_universe(self):
        universe = Universum(boxSizes=[10, 10, 10])
        self.assertIsInstance(universe, Universum)
        universe.addAtomBondData(self.testAtoms, self.testBonds)
        atom = universe.getAtom(1)
        self.assertEqual(atom.getUnderlyingData(), self.testAtoms.iloc[0])
        universe.reset()
        self.assertCountEqual([], universe.getMolecules())
        self.assertEqual(0, universe.getSize())
        # check that the except paths work too: non-existant atom ids & type
        self.assertEqual(None, universe.getAtomsWithType(1))
        self.assertEqual(None, universe.getAtom(1))

    def test_molecule(self):
        universe = Universum(boxSizes=[10, 10, 10])
        universe.addAtomBondData(self.testAtoms, self.testBonds)
        self.assertEqual(4, len(universe.getAtomsWithType(1)))
        self.assertEqual(2, len(universe.getAtomsWithType(2)))
        molecules = universe.getMolecules()
        self.assertEqual(len(molecules), 2)
        for molecule in molecules:
            self.assertIsInstance(molecule, Molecule)

        molecules = universe.getMolecules(ignoreAtomType=2)
        self.assertEqual(len(molecules), 2)
        # test iteration & return type
        for molecule in molecules:
            self.assertIsInstance(molecule, Molecule)
        # test calculations
        self.assertEqual(molecules[0].computeEndToEndDistance(), 2)
        self.assertEqual(molecules[0].computeBondLengths().mean(), 1.0)
