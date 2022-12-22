# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 15:35:31 2022

@author: Alexander Pilz
"""
import unittest
import requests

class test(unittest.TestCase):
    
    def test_helloWorld(self):  
        response = requests.get('http://localhost:5000/')                 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello World!')
        
#run application
if __name__ == '__main__':
    unittest.main()

