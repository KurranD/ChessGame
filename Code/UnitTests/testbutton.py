import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.button import Button

class TestButtonMethods(unittest.TestCase):
    def test_createButtonProperly(self):
        testButton = Button(200, 200, 'Images/knight.png')
        self.assertIsNotNone(testButton)

    def test_createButtonWithErrors(self):
        self.assertRaises(ValueError, lambda: Button(-5, 200, 'Images/knight.png'))
        self.assertRaises(ValueError, lambda: Button(100, 800, 'Images/knight.png'))
        self.assertRaises(ValueError, lambda: Button(200, 200, 'Images/fake_image.png'))

if __name__ == '__main__':
    unittest.main()