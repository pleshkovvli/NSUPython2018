from itertools import islice
import unittest
from functools import reduce


class Vector(object):
    """Class representing linear algebra vector"""

    _number_types = (complex, float, int)

    class NotANumericTypeException(TypeError):
        def __init__(self, *elements):
            self.message = f"${elements} cannot be both reduced to numeric type"

    def __init__(self, *initializer):
        """
        Create vector from given iterable
        :param initializer: iterable or array of scalar values to fill vector
        """
        if len(initializer) == 1:
            try:
                vector = [x for x in initializer[0]]
            except TypeError:
                vector = initializer
        else:
            vector = initializer

        comp_type = self._get_type(vector)
        self._vector = [comp_type(x) for x in vector]

    def _get_type(self, vector):
        return type(reduce(lambda acc, cur_type: self._complex_element(acc, cur_type)[0], vector))

    @staticmethod
    def _complex_element(one, other):
        one_type = type(one)
        other_type = type(other)

        for index, cur_type in enumerate(Vector._number_types):
            if one_type is cur_type or other_type is cur_type:
                for more_complex in reversed(Vector._number_types[0:index + 1]):
                    try:
                        return more_complex(one), more_complex(other)
                    except ValueError:
                        pass

                raise Vector.NotANumericTypeException(one, other)

        for cur_type in reversed(Vector._number_types):
            try:
                return cur_type(one), cur_type(other)
            except ValueError:
                pass

        raise Vector.NotANumericTypeException(one, other)

    def _check_length(self, other):
        if len(self) != len(other):
            raise DifferentLengthsException(len(self), len(other))

    def _map_vector(self, fun, other):
        return map(fun, zip(self._vector, other._vector))

    def __len__(self):
        """Returns length of vector"""
        return len(self._vector)

    def __getitem__(self, item):
        """Returns element at specified position"""
        return self._vector[item]

    def __eq__(self, other):
        """Checks two vectors on equality"""
        if not isinstance(other, Vector):
            return False

        if len(self) != len(other):
            return False

        return all(self._map_vector(lambda x: x[0] == x[1], other))

    def __ne__(self, other):
        """Checks two vectors on non-equality"""
        return not self == other

    def __add__(self, other):
        """Returns vector, representing sum of current and other vector
        :param other: vector to sum with current vector
        :return: Vector: sum of two vectors
        """
        self._check_length(other)

        return Vector([x for x in self._map_vector(lambda x: x[0] + x[1], other)])

    def __sub__(self, other):
        """Returns vector, representing substraction of current and other vector
        :param other: vector to subtract from current vector
        :return: Vector: subtraction of two vectors
        """
        self._check_length(other)

        return Vector([x for x in self._map_vector(lambda x: x[0] - x[1], other)])

    def __mul__(self, other):
        """Scalar multiplication, if other is vector, or constant, if other is number
        :param other: vector or constant to multiply with
        :return: Vector: multiplication of two vectors
                 Number: multiplication of vector and constant
        """
        if type(other) in Vector._number_types:
            return Vector(map(lambda x: x * other, self._vector))
        elif isinstance(other, Vector):
            self._check_length(other)
            return sum(self._map_vector(lambda x: x[0] * x[1], other))
        else:
            raise TypeError(f"${other} is not scalar and neither vector")

    def __rmul__(self, other):
        """Multiplication for argument on other side of vector"""
        return self * other

    def __str__(self):
        return "Vector(" + str(self._vector)[1:-1] + ")"


class DifferentLengthsException(Exception):
    def __init__(self, *lengths):
        self.message = f"One length = {lengths[0]}, other length = {lengths[1]}"


class TestVector(unittest.TestCase):
    def test_init(self):
        self.assertEqual(Vector([0, 1, 3, 5, 6]), Vector(0, 1, 3, 5, 6))

        def zeros():
            while True:
                yield 0

        self.assertEqual(Vector(0, 0, 0, 0, 0), Vector(islice(zeros(), 0, 5)))
        self.assertEqual(Vector(0.1, 23, 1, 5), Vector(0.1, 23.0, 1, 5.0))
        self.assertEqual(Vector("0.1", 23, "1", 5), Vector(0.1, "23.0", 1, 5.0))

        for x in Vector(1, 2, 4.0, 7, "11.1"):
            self.assertEqual(type(x), float)

        for x in Vector(1, 2, 4.0, 7, "11.1+1j"):
            self.assertEqual(type(x), complex)

        for x in Vector(1, 2, 4, 7, "11"):
            self.assertEqual(type(x), int)

    def test_len(self):
        self.assertEqual(len(Vector([0, 1, 3, 5, 6])), 5)
        self.assertEqual(len(Vector((1, 1, 1))), 3)

    def test_getitem(self):
        vector = Vector(0, 1, 3, 5, 6)
        self.assertEqual(vector[0], 0)
        self.assertEqual(vector[1], 1)
        self.assertEqual(vector[2], 3)
        self.assertEqual(vector[3], 5)
        self.assertEqual(vector[4], 6)

    def test_ne(self):
        self.assertNotEqual(Vector([0, 1, 3, 5, 6]), Vector([0, 1, 3, 5]))
        self.assertNotEqual(Vector(0, 1, 3), Vector([0, 1, 3, 5]))

    def test_add(self):
        self.assertEqual(Vector([0, 1, 3, 5, 6]) + Vector([2, 1, 2, 1, 2]), Vector([2, 2, 5, 6, 8]))
        self.assertEqual(
            Vector([0, 1, 3, 5, 6]) + Vector([2, 1, 2, 1, 2]),
            Vector([2, 1, 2, 1, 2]) + Vector([0, 1, 3, 5, 6])
        )

    def test_sub(self):
        self.assertEqual(Vector([0, 1, 3, 5, 6]) - Vector([2, 1, 2, 1, 2]), Vector([-2, 0, 1, 4, 4]))
        self.assertEqual(
            Vector([0, 1, 3, 5, 6]) - Vector([2, 1, 2, 1, 2]),
            Vector([-2, -1, -2, -1, -2]) + Vector([0, 1, 3, 5, 6])
        )

    def test_mul(self):
        vector = Vector([0, 1, 3, 5, 6])
        v = Vector(2, 1, 2, 1, 2)
        self.assertEqual(vector * v, 24)
        vector1 = Vector([0, 1, 3, 5, 6])
        vector_ = vector1 * 4
        second = Vector(0, 4, 12, 20, 24)
        self.assertEqual(vector_, second)
        self.assertEqual(4 * Vector(0, 1, 3, 5, 6), Vector([0, 4, 12, 20, 24]))

    def test_str(self):
        self.assertEqual(str(Vector([0, 1, 3, 5, 6])), "Vector(0, 1, 3, 5, 6)")


if __name__ == "__main__":
    unittest.main()
