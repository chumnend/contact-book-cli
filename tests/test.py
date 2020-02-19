import unittest

class SampleTest(unittest.TestCase):
    def setUp(self):
        return
    
    def test(self):
        self.assertTrue(1 == 1)
    
    def tearDown(self):
        return 
    
if __name__ == "__main__":
    unittest.main()