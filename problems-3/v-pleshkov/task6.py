import unittest

from task4 import Vector


class Vector3D(Vector):
    def __init__(self, *initializer):
        super().__init__(*initializer)
        if len(self) != 3:
            raise ValueError(f"Length of Vector3D should be 3, got ${len(self)}")

    def __matmul__(self, other):
        return Vector3D(
            self[1] * other[2] - self[2] * other[1],
            -self[0] * other[2] + self[2] * other[0],
            self[0] * other[1] - self[1] * other[0],
        )

class TestVector(unittest.TestCase):
    def test_init(self):
        self.assertEqual(Vector3D([0, 1, 3]), Vector3D(0, 1, 3))

        with self.assertRaises(ValueError):
            Vector3D(1, 2, 3, 1)

        with self.assertRaises(ValueError):
            Vector3D([1, 2])

    def test_cross_product(self):
        self.assertEqual(Vector3D(4, 2, 1) @ Vector3D(1, 7, 8), Vector3D(9, -31, 26))

        self.assertEqual(Vector3D(1, 0, 0) @ Vector3D(0, 1, 0), Vector3D(0, 0, 1))
        self.assertEqual(Vector3D(0, 1, 0) @ Vector3D(0, 0, 1), Vector3D(1, 0, 0))
        self.assertEqual(Vector3D(0, 0, 1) @ Vector3D(1, 0, 0), Vector3D(0, 1, 0))

if __name__ == "__main__":
    unittest.main()