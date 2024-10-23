import unittest
import dynamit


class TestModelPatlak(unittest.TestCase):

    def test_model_step_case0(self):
        k = 3
        v0 = 10

        tp = [0.0, 4.3, 7.5, 12.4, 16.2]
        in_func = [0.0, 10.3, 12.1, 8.1, 4.1]

        m = dynamit.model_patlak(k, v0, tp, in_func)

        self.assertEqual(5, len(m))
        # self.assertAlmostEqual(0.0, m[0], places=3)
        # self.assertAlmostEqual(76.435, m[1], places=3)
        # self.assertAlmostEqual(183.955, m[2], places=3)
        # self.assertAlmostEqual(332.425, m[3], places=3)
        # self.assertAlmostEqual(401.965, m[4], places=3)
