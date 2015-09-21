# encoding: UTF-8

#
# Copyright (c) 2015 Facility for Rare Isotope Beams
#

"""
Unit tests for IMPACT lattice support.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from StringIO import StringIO

from phyutil.phylib.lattice import impact



class TestReadLattice(unittest.TestCase):
    """Read IMPACT Lattice Test"""

    LATTICE1 = """! Generated by PhysUtil - 2015-08-21 11:18:06.071710
!! Name: ls1ts1_layout.csv, Desc: sequence
4 1
6 1000 2 0 1
65 65 129 4 0.14 0.14 0.1025446
3 0 0 1
1000
0.0
1.48852718947e-10
0.0022734189 8.8312578e-05 0.0 1.0 1.0 0.0 0.0
0.0022734189 8.8312578e-05 0.0 1.0 1.0 0.0 0.0
0.076704772 3.4741445e-06 0.0 1.0 1.0 0.0 0.0
0.0 500000.0 931494320.0 0.138655462185 80500000.0 0.0 99.9
!!["DRIFT", "VALVE", 0.072, 0.07200000000000273, {}]
0.072 4 20 0 0.02 /
!!["DRIFT", "DRIFT", 0.1350635, 0.19094024999999704, {}]
0.1350635 4 20 0 0.02 /
!!["LS1_CA01:CAV1_D1127", "CAV", 0.24, 0.44706350000001294, {"AMP[V]": 4, "PHA[deg]": 6}]
0.24 20 20 103 0.64 80500000.0 -6.524 421 0.017 /
"""

    def test_lattice1(self):
        self.lattice = impact.read_lattice(StringIO(self.LATTICE1)) 
        # header line 1
        self.assertEqual(self.lattice.nprocessors, 4)
        # header line 2
        self.assertEqual(self.lattice.ndimensions, 6)
        self.assertEqual(self.lattice.nparticles, 1000)
        self.assertEqual(self.lattice.integrator, 2)
        self.assertEqual(self.lattice.errorStudy, 0)
        self.assertEqual(self.lattice.outputMode, 1)
        # header line 3
        self.assertItemsEqual(self.lattice.meshSize, [ 65, 65, 129 ])
        self.assertEqual(self.lattice.meshMode, 4)
        for idx, value in enumerate([ 0.14, 0.14 ]):
            self.assertAlmostEqual(self.lattice.pipeSize[idx], value)
        self.assertAlmostEqual(self.lattice.periodSize, 0.1025446)
        # header line 4
        self.assertEqual(self.lattice.inputMode, 3)
        self.assertEqual(self.lattice.restart, 0)
        self.assertEqual(self.lattice.subcycle, 0)
        self.assertEqual(self.lattice.nstates, 1)
        # header line 5
        self.assertEqual(self.lattice.nparticles, 1000)
        # header line 6
        self.assertEqual(self.lattice.current, 0.0)
        # header line 7
        self.assertEqual(self.lattice.charge, 1.48852718947e-10)
        # header line 8
        self.assertAlmostEqual(self.lattice.distSigma[0], 0.0022734189)
        self.assertAlmostEqual(self.lattice.distLambda[0], 8.8312578e-05)
        self.assertAlmostEqual(self.lattice.distMu[0], 0.0)
        self.assertAlmostEqual(self.lattice.mismatch[0], 1.0)
        self.assertAlmostEqual(self.lattice.emismatch[0], 1.0)
        self.assertAlmostEqual(self.lattice.offset[0], 0.0)
        self.assertAlmostEqual(self.lattice.eoffset[0], 0.0)
        # header line 9
        self.assertAlmostEqual(self.lattice.distSigma[1], 0.0022734189)
        self.assertAlmostEqual(self.lattice.distLambda[1], 8.8312578e-05)
        self.assertAlmostEqual(self.lattice.distMu[1], 0.0)
        self.assertAlmostEqual(self.lattice.mismatch[1], 1.0)
        self.assertAlmostEqual(self.lattice.emismatch[1], 1.0)
        self.assertAlmostEqual(self.lattice.offset[1], 0.0)
        self.assertAlmostEqual(self.lattice.eoffset[1], 0.0)
        # header line 10
        self.assertAlmostEqual(self.lattice.distSigma[2], 0.076704772)
        self.assertAlmostEqual(self.lattice.distLambda[2], 3.4741445e-06)
        self.assertAlmostEqual(self.lattice.distMu[2], 0.0)
        self.assertAlmostEqual(self.lattice.mismatch[2], 1.0)
        self.assertAlmostEqual(self.lattice.emismatch[2], 1.0)
        self.assertAlmostEqual(self.lattice.offset[2], 0.0)
        self.assertAlmostEqual(self.lattice.eoffset[2], 0.0)
        # header line 11
        self.assertAlmostEqual(self.lattice.initialCurrent, 0.0)
        self.assertAlmostEqual(self.lattice.initialEnergy, 500000.0)
        self.assertAlmostEqual(self.lattice.particleMass, 931494320.0)
        self.assertAlmostEqual(self.lattice.initialCharge, 0.138655462185)
        self.assertAlmostEqual(self.lattice.scalingFreq, 80500000.0)
        self.assertAlmostEqual(self.lattice.initialPhase, 0.0)
        self.assertAlmostEqual(self.lattice.beamPercent, 99.9)
        # lattice elements
        elements = self.lattice.elements
        # value element
        self.assertEqual(elements[0].name, "DRIFT")
        self.assertEqual(elements[0].etype, "VALVE")
        self.assertAlmostEqual(elements[0].length, 0.072)
        self.assertAlmostEqual(elements[0].position, 0.072)
        # dift element
        self.assertEqual(elements[1].name, "DRIFT")
        self.assertEqual(elements[1].etype, "DRIFT")
        self.assertAlmostEqual(elements[1].length, 0.1350635)
        self.assertAlmostEqual(elements[1].position, 0.19094025)
        # cavity element
        self.assertEqual(elements[2].name, "LS1_CA01:CAV1_D1127")
        self.assertEqual(elements[2].etype, "CAV")
        self.assertAlmostEqual(elements[2].length, 0.24)
        self.assertAlmostEqual(elements[2].position, 0.4470635)
        self.assertEquals(len(elements[2].fields), 2)
        self.assertIn("AMP", [ f.name for f in elements[2].fields ])
        self.assertIn("PHA", [ f.name for f in elements[2].fields ])
        for f in elements[2].fields:
            if f.name == "AMP":
                self.assertEqual(f.unit, "V")
                self.assertEqual(f.index, 4)
            elif f.name == "PHA":
                self.assertEqual(f.unit, "deg")
                self.assertEqual(f.index, 6)

    LATTICE2 = """! Generated by PhysUtil - 2015-08-21 11:18:06.071710
!! Name: ls1ts1_layout.csv, Desc: sequence
2 1
6 3000 1 0 3
33 33 65 4 0.16 0.18 0.44
3 0 0 2
1000 2000
0.01  0.02
1.48e-10 2.28e-10
0.00276 4.68274e-05 0.11 1.1 1.4 0.07 0.08
0.00387 5.92732e-05 0.21 1.2 1.5 0.08 0.07
0.07674 8.09374e-06 0.31 1.3 1.6 0.09 0.06
0.05 400000.0 936.0 0.24325653 6500000.0 0.0 99.9
!!["DRIFT", "DRIFT", 0.0761235, 0.6558303399999943, {}]
0.0761235 4 20 0 0.02 /
!!["LS1_CA01:SOL1_D1131", "SOL", 0.1, 0.74333034, {"B[T]": 4}]
0.1 1 20 3 5.34 0 0.02 /
!!["LS1_CA01:DCH_D1131", "HCOR", 0.0, 0.74333034, {"ANG[rad]": 6}]
0.0 0 0 -21 0.02 0.0 0.0 0.0 0.0 0.0 0.0 /
!!["LS1_CA01:DCV_D1131", "VCOR", 0.0, 0.74333034, {"ANG[rad]": 8}]
0.0 0 0 -21 0.02 0.0 0.0 0.0 0.0 0.0 0.0 /
!!["LS1_CA01:SOL1_D1131", "SOL", 0.1, 0.8433303399999943, {"B[T]": 4}]
0.1 1 20 3 5.34 0 0.02 /
"""

    def test_lattice2(self):
        self.lattice = impact.read_lattice(StringIO(self.LATTICE2)) 
        # header line 1
        self.assertEqual(self.lattice.nprocessors, 2)
        # header line 2
        self.assertEqual(self.lattice.ndimensions, 6)
        self.assertEqual(sum(self.lattice.nparticles), 3000)
        self.assertEqual(self.lattice.integrator, 1)
        self.assertEqual(self.lattice.errorStudy, 0)
        self.assertEqual(self.lattice.outputMode, 3)
        # header line 3
        self.assertItemsEqual(self.lattice.meshSize, [ 33, 33, 65 ])
        self.assertEqual(self.lattice.meshMode, 4)
        for idx, value in enumerate([ 0.16, 0.18 ]):
            self.assertAlmostEqual(self.lattice.pipeSize[idx], value)
        self.assertAlmostEqual(self.lattice.periodSize, 0.44)
        # header line 4
        self.assertEqual(self.lattice.inputMode, 3)
        self.assertEqual(self.lattice.restart, 0)
        self.assertEqual(self.lattice.subcycle, 0)
        self.assertEqual(self.lattice.nstates, 2)
        # header line 5
        for idx, value in enumerate([ 1000, 2000 ]):
            self.assertEqual(self.lattice.nparticles[idx], value)
        # header line 6
        for idx, value in enumerate([ 0.01, 0.02 ]):
            self.assertAlmostEqual(self.lattice.current[idx], value)
        # header line 7
        for idx, value in enumerate([1.48e-10, 2.28e-10 ]):
            self.assertEqual(self.lattice.charge[idx], value)
        # header line 8
        self.assertAlmostEqual(self.lattice.distSigma[0], 0.00276)
        self.assertAlmostEqual(self.lattice.distLambda[0], 4.68274e-05)
        self.assertAlmostEqual(self.lattice.distMu[0], 0.11)
        self.assertAlmostEqual(self.lattice.mismatch[0], 1.1)
        self.assertAlmostEqual(self.lattice.emismatch[0], 1.4)
        self.assertAlmostEqual(self.lattice.offset[0], 0.07)
        self.assertAlmostEqual(self.lattice.eoffset[0], 0.08)
        # header line 9
        self.assertAlmostEqual(self.lattice.distSigma[1], 0.00387)
        self.assertAlmostEqual(self.lattice.distLambda[1], 5.92732e-05)
        self.assertAlmostEqual(self.lattice.distMu[1], 0.21)
        self.assertAlmostEqual(self.lattice.mismatch[1], 1.2)
        self.assertAlmostEqual(self.lattice.emismatch[1], 1.5)
        self.assertAlmostEqual(self.lattice.offset[1], 0.08)
        self.assertAlmostEqual(self.lattice.eoffset[1], 0.07)
        # header line 10
        self.assertAlmostEqual(self.lattice.distSigma[2], 0.07674)
        self.assertAlmostEqual(self.lattice.distLambda[2], 8.09374e-06)
        self.assertAlmostEqual(self.lattice.distMu[2], 0.31)
        self.assertAlmostEqual(self.lattice.mismatch[2], 1.3)
        self.assertAlmostEqual(self.lattice.emismatch[2], 1.6)
        self.assertAlmostEqual(self.lattice.offset[2], 0.09)
        self.assertAlmostEqual(self.lattice.eoffset[2], 0.06)
        # header line 11
        self.assertAlmostEqual(self.lattice.initialCurrent, 0.05)
        self.assertAlmostEqual(self.lattice.initialEnergy, 400000.0)
        self.assertAlmostEqual(self.lattice.particleMass, 936.0)
        self.assertAlmostEqual(self.lattice.initialCharge, 0.24325653)
        self.assertAlmostEqual(self.lattice.scalingFreq, 6500000.0)
        self.assertAlmostEqual(self.lattice.initialPhase, 0.0)
        self.assertAlmostEqual(self.lattice.beamPercent, 99.9)
        # lattice elements
        elements = self.lattice.elements
        # value element
        self.assertEqual(elements[0].name, "DRIFT")
        self.assertEqual(elements[0].etype, "DRIFT")
        self.assertAlmostEqual(elements[0].length, 0.0761235)
        self.assertAlmostEqual(elements[0].position, 0.6558303)
        # solenoid element
        self.assertEqual(elements[1].name, "LS1_CA01:SOL1_D1131")
        self.assertEqual(elements[1].etype, "SOL")
        self.assertAlmostEqual(elements[1].length, 0.1)
        self.assertAlmostEqual(elements[1].position, 0.74333034)
        self.assertEquals(len(elements[1].fields), 1)
        self.assertEquals(elements[1].fields[0].name, "B")
        self.assertEqual(elements[1].fields[0].unit, "T")
        self.assertEqual(elements[1].fields[0].index, 4)
        # horiz. corrector element
        self.assertEqual(elements[2].name, "LS1_CA01:DCH_D1131")
        self.assertEqual(elements[2].etype, "HCOR")
        self.assertAlmostEqual(elements[2].length, 0.0)
        self.assertAlmostEqual(elements[2].position, 0.74333034)
        self.assertEquals(len(elements[2].fields), 1)
        self.assertEquals(elements[2].fields[0].name, "ANG")
        self.assertEqual(elements[2].fields[0].unit, "rad")
        self.assertEqual(elements[2].fields[0].index, 6)
        # vert. corrector element
        self.assertEqual(elements[3].name, "LS1_CA01:DCV_D1131")
        self.assertEqual(elements[3].etype, "VCOR")
        self.assertAlmostEqual(elements[3].length, 0.0)
        self.assertAlmostEqual(elements[3].position, 0.74333034)
        self.assertEquals(len(elements[3].fields), 1)
        self.assertEquals(elements[3].fields[0].name, "ANG")
        self.assertEqual(elements[3].fields[0].unit, "rad")
        self.assertEqual(elements[3].fields[0].index, 8)
        # solenoid element
        self.assertEqual(elements[4].name, "LS1_CA01:SOL1_D1131")
        self.assertEqual(elements[4].etype, "SOL")
        self.assertAlmostEqual(elements[4].length, 0.1)
        self.assertAlmostEqual(elements[4].position, 0.8433303)
        self.assertEquals(len(elements[4].fields), 1)
        self.assertEquals(elements[4].fields[0].name, "B")
        self.assertEqual(elements[4].fields[0].unit, "T")
        self.assertEqual(elements[4].fields[0].index, 4)

