#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import unittest
import context
import Mathstein.matheqn as matheqn


class TestMathstein(unittest.TestCase):
    
    def test_OneVarSolver(self):
        result1=matheqn.OneVarSolver("x+5-3+x=6+x-2")
        self.assertAlmostEqual(result1,2,0,"OneVarSolver() failed to execute")
        result2=matheqn.OneVarSolver("x=x")
        self.assertAlmostEqual(result2,"Infinite solutions",None,"OneVarSolver() failed to execute")
        result3=matheqn.OneVarSolver("x=x+2")
        self.assertAlmostEqual(result3,"No solution",None,"OneVarSolver() failed to execute")
    def test_MultiVarSolver(self):
        result1=matheqn.MultiVarSolver(['- 3x + y = -1','4x + y = -8'],2)
        self.assertAlmostEqual(result1,[-1.0,-4.0],None,"MultiVarSolver() failed to execute")
        result2=matheqn.MultiVarSolver(['2x + y = 2','4x + 2y = -8'],2)
        self.assertAlmostEqual(result2,"No solution possible",None,"MultiVarSolver() failed to execute")
        
        
if __name__=='__main__':
    unittest.main()


# In[ ]:




