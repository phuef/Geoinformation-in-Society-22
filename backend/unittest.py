# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 15:35:31 2022

@author: Alexander Pilz
"""
import unittest
import requests
import logging
import subprocess

class test(unittest.TestCase):
    
    def test_helloWorld(self):  
        response = requests.get('http://localhost:5050/')                 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello World!')
    
    def test_brewCoffee(self):  
        response = requests.get('http://localhost:5050/brewCoffee')                 
        self.assertEqual(response.status_code, 418)
        self.assertEqual(response.content, b'The server refuses to brew coffee because it is, permanently, a teapot.')
        
#run application
if __name__ == '__main__':
    unittest.main()

