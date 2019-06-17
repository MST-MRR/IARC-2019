"""
Unit test for grayscaling image.
"""
import unittest

import cv2
import numpy as np

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from normalize.ts_converter import binarize_mat


class TestNormalizer(unittest.TestCase):
    """
    Image normalizer tester.
    """

    def test_binarize(self):
        """
        Test image binarizer.
        """
        SIZE = 512

        # joint gaussian
        x, y = np.meshgrid(np.linspace(-1, 1, SIZE), np.linspace(-1, 1, SIZE))
        d = np.sqrt(x**2 + y**2)
        sigma, mu = 1.0, 0.0
        gaussian = np.exp(-((d - mu)**2 / (2.0 * sigma**2)))

        img = binarize_mat(gaussian)

        self.assertEqual(len(np.unique(img)), 2)


if __name__ == '__main__':
    unittest.main()
