#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import unittest
import context
import Mathstein.mathroot as mathroot


class TestMathstein(unittest.TestCase):
    
    def test_quadraticsolver(self):
        result1=mathroot.quadraticsolver((1,0,-4,0))
        self.assertAlmostEqual(result1,(2.0,-2.0),None,"quadraticsolver() failed to execute")
        result2=mathroot.quadraticsolver((1,0,4,0))
        self.assertAlmostEqual(result2,"No real root possible",None,"quadraticsolver() failed to execute")
    def test_cubicsolver(self):
        result1=mathroot.cubicsolver((1,0,0,-27,0))
        self.assertAlmostEqual(result1,3,None,"cubicsolver() failed to execute")
        result2=mathroot.cubicsolver((1,0,0,27,0))
        self.assertAlmostEqual(result2,"No real root possible",None,"cubicsolver() failed to execute")
    def test_biquadraticsolver(self):
        result1=mathroot.biquadraticsolver((1,0,0,0,0,16))
        self.assertAlmostEqual(result1,[-4.0, 4.0],None,"biquadraticsolver() failed to execute")
        result2=mathroot.biquadraticsolver((1,0,0,0,0,-16))
        self.assertAlmostEqual(result2,"No real root possible",None,"biquadraticsolver() failed to execute")
        

if __name__=='__main__':
    unittest.main()

