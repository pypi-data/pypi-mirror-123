#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unittest
import context
import Mathstein.matharea as matharea



class TestMathstein(unittest.TestCase):
    
    def test_areacalculator(self):
        result1=matharea.areacalculator("x**3",[1,2])
        self.assertAlmostEqual(result1,3.7545,3,"areacalculator() failed to execute")
        result2=matharea.areacalculator("3*x**2+2",[1,2])
        self.assertAlmostEqual(result2,9.009,3,"areacalculator() failed to execute")

if __name__=='__main__':
    unittest.main()

    
    


# In[ ]:




