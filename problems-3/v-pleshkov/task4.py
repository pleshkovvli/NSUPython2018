import unittest
from functools import reduce
from numbers import Number

number_types = (complex, float, int)


def _most_complicated_type(one_type, other_type):
    for index, cur_type in enumerate(number_types):
        if one_type is cur_type or other_type is cur_type:
            for more_complex in reversed(number_types[0:index]):
                try:
                    more_complex(one_type), more_complex(other_type)
                    return more_complex
                except TypeError:
                    pass

            raise TypeError

    for more_complex in reversed(number_types):
        more_complex(one_type), more_complex(other_type)
        return more_complex

    raise TypeError


class NotIterableException(TypeError):
    pass


class Vector(object):
    """Class representing linear algebra vector"""
    def __init__(self, *initializer):
        """
        Create vector from given iterable
        :param initializer: iterable or array of scalar values to fill vector
        """
        try:
            vector = self._vector_from_iterable(initializer[0])
        except NotIterableException:
            vector = self._vector_from_array(initializer)

        comp_type = reduce(
            lambda acc, cur_type: _most_complicated_type(acc, cur_type),
            map(lambda x: type(x), vector)
        )

        self._vector = [comp_type(x) for x in vector]


    def _vector_from_array(self, *array):
        return [x for x in array]


    def _vector_from_iterable(self, iterable):
        try:
            return list(iterable)
        except TypeError:
            raise NotIterableException

    def __len__(self):
        """Returns length of vector"""
        return len(self._vector)

    def __getitem__(self, item):
        """Returns element at specified position"""
        return self._vector[item]

    def __eq__(self, other):
        """Checks two vectors on equality"""
        if len(self) != len(other):
            return False

        return all(self[i] == other[i] for i in range(0, len(self)))

    def __ne__(self, other):
        """Checks two vectors on non-equality"""
        return not self == other

    def __add__(self, other):
        """Returns vector, representing sum of current and other vector
        :param other: vector to sum with current vector
        :return: Vector: sum of two vectors
        """
        self._check_length(other)
        length = len(self)

        return Vector(self[i] + other[i] for i in range(0, length))

    def __sub__(self, other):
        """Returns vector, representing substraction of current and other vector
        :param other: vector to subtract from current vector
        :return: Vector: subtraction of two vectors
        """
        length = len(self)
        self._check_length(other)

        return Vector(self[i] - other[i] for i in range(0, length))

    def __mul__(self, other):
        """Scalar multiplication, if other is vector, or constant, if other is number
        :param other: vector or constant to multiply with
        :return: Vector: multiplication of two vectors
                 Number: multiplication of vector and constant
        """
        length = len(self)
        if isinstance(other, Number):
            return Vector(self[i] * other for i in range(0, length))
        else:
            self._check_length(other)
            return sum(self[i] * other[i] for i in range(0, length))

    def __rmul__(self, other):
        """Multiplication for argument on other side of vector"""
        return self * other

    def __str__(self):
        return "Vector" + str(self._vector)

    def _check_length(self, other):
        if len(self) != len(other):
            raise DifferentLengthsException(len(self), len(other))


class DifferentLengthsException(Exception):
    def __init__(self, *lengths):
        self.message = f"One length = {lengths[0]}, other length = {lengths[1]}"


class IllegalLengthException(Exception):
    def __init__(self, length):
        self.message = f"Length should be more than zero: actual={length}"


class TestVector(unittest.TestCase):
    def test_init(self):
        self.assertEqual(Vector([0, 1, 3, 5, 6]), Vector(0, 1, 3, 5, 6))

        def zeros():
            while True:
                yield 0
        self.assertEqual(Vector([0 ,0, 0, 0, 0]), Vector(zeros(), 5))
        with self.assertRaises(IllegalLengthException):
            Vector([1, 2], -1)

    def test_len(self):
        self.assertEqual(len(Vector([0, 1, 3, 5, 6])), 5)
        self.assertEqual(len(Vector([0, 1, 3, 5, 6, 8, 9], 4)), 4)
        self.assertEqual(len(Vector((1, 1, 1))), 3)

    def test_getitem(self):
        vector = Vector([0, 1, 3, 5, 6])
        self.assertEqual(vector[0], 0)
        self.assertEqual(vector[1], 1)
        self.assertEqual(vector[2], 3)
        self.assertEqual(vector[3], 5)
        self.assertEqual(vector[4], 6)

    def test_ne(self):
        self.assertNotEqual(Vector([0, 1, 3, 5, 6]), Vector([0, 1, 3, 5]))
        self.assertNotEqual(Vector([0, 1, 3, 5], 3), Vector([0, 1, 3, 5]))

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
        self.assertEqual(Vector([0, 1, 3, 5, 6]) * Vector([2, 1, 2, 1, 2]), 24)
        self.assertEqual(Vector([0, 1, 3, 5, 6]) * 4, Vector([0, 4, 12, 20, 24]))
        self.assertEqual(4 * Vector([0, 1, 3, 5, 6]), Vector([0, 4, 12, 20, 24]))

    def test_str(self):
        self.assertEqual(str(Vector([0, 1, 3, 5, 6])), "Vector[0, 1, 3, 5, 6]")


if __name__ == "__main__":
    unittest.main()
