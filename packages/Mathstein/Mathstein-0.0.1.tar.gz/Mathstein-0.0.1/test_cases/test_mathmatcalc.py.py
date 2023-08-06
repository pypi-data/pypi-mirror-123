#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import unittest
import context
import Mathstein.mathmatcalc as mathmatcalc



class TestMathstein(unittest.TestCase):
    
    def test_mataddition(self):
        result1=mathmatcalc.mataddition([[1,2,3],[4 ,5,6],[7 ,8,9]],[[9,8,7],[6,5,4],[3,2,1]])
        self.assertAlmostEqual(result1,[[10,10,10],[10,10,10],[10,10,10]],None,"mataddition() failed to execute")
        result2=mathmatcalc.quadraticsolver([[2,3],[4 ,5,6],[7 ,8,9]],[[9,8,7],[6,5,4],[3,2,1]])
        self.assertAlmostEqual(result2,"Addition not possible,None","mataddition() failed to execute")
    def test_matsubtraction(self):
        result1=mathmatcalc.matsubtraction([[1,2,3],[4 ,5,6],[7 ,8,9]],[[9,8,7],[6,5,4],[3,2,1]])
        self.assertAlmostEqual(result1,[[-8, -6, -4], [-2, 0, 2], [4, 6, 8]],None,"matsubtraction() failed to execute")
        result2=mathmatcalc.matsubtraction([[2,3],[4 ,5,6],[7 ,8,9]],[[9,8,7],[6,5,4],[3,2,1]])
        self.assertAlmostEqual(result2,"Subtraction not possible",None,"matsubtraction() failed to execute")
    def test_matmultiplication(self):
        result1=mathmatcalc.matmultiplication([[1,2,3],[4 ,5,6],[7 ,8,9]],[[9,8,7],[6,5,4],[3,2,1]])
        self.assertAlmostEqual(result1,[[30, 24, 18], [84, 69, 54], [138, 114, 90]],None,"matmultiplication() failed to execute")
        result2=mathmatcalc.matmultiplication([[2,3],[4 ,5,6],[7 ,8,9]],[[9,8,7],[6,5,4],[3,2,1]])
        self.assertAlmostEqual(result2,"Multiplication not possible",None,"matmultiplication() failed to execute")
    def test_matdeterminant(self):
        result1=mathmatcalc.matdeterminant([[1,2,3],[4 ,5,6],[7 ,8,9]],[[9,8,7],[6,5,4],[3,2,1]])
        self.assertAlmostEqual(result1,0,None,"matdeterminant() failed to execute")
        

if __name__=='__main__':
    unittest.main()

