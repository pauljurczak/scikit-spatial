"""Test properties of spatial objects."""

import hypothesis.strategies as st
import numpy as np
import pytest
from hypothesis import given
from numpy.testing import assert_array_equal, assert_allclose

from skspatial.objects import Point, Vector, Line


# Absolute tolerance for np.isclose and np.allclose functions.
TOLERANCE = 0.01


# Define custom strategies.

st_floats_nonzero = st.floats(min_value=-1e6, max_value=1e6).filter(
    lambda x: abs(x) > TOLERANCE
)

st_arrays = st.lists(st_floats_nonzero, min_size=1, max_size=10)
st_arrays_allowed = st.lists(st_floats_nonzero, min_size=1, max_size=3)


@given(st_arrays)
def test_length(array):

    if len(array) <= 3:

        point = Point(array)
        vector = Vector(array)

        assert point != vector
        assert point.array.size == vector.array.size == 3
        assert_array_equal(point.array, vector.array)

    else:

        with pytest.raises(Exception):
            Point(array)
        with pytest.raises(Exception):
            Vector(array)


@given(st_arrays_allowed)
def test_add(array):
    """Test adding points and vectors."""
    point = Point(array)
    vector = Vector(array)

    # Add a vector to a point.
    point_2 = point.add(vector)
    point_3 = point_2.add(vector.reverse())
    assert point_3.is_close(point)

    # Add a vector to a vector.
    vector_2 = vector.add(vector)
    vector_double = Vector(2 * vector.array)
    assert vector_2.is_close(vector_double)

    with pytest.raises(Exception):
        point.add(point)

    with pytest.raises(Exception):
        vector.add(point)


@given(st_arrays_allowed)
def test_unit_vector(array):

    vector = Vector(array)
    unit_vector = vector.unit()

    assert np.isclose(unit_vector.magnitude, 1)
    assert_allclose(vector.magnitude * unit_vector.array, vector.array)


@given(st_arrays_allowed)
def test_is_close(array):

    point = Point(array)
    vector = Vector(array)

    assert point.is_close(point)
    assert vector.is_close(vector)

    with pytest.raises(Exception):
        assert point.is_close(vector)

    with pytest.raises(Exception):
        assert vector.is_close(point)


@given(st_arrays_allowed, st_arrays_allowed)
def test_line(array_1, array_2):

    point_1 = Point(array_1)
    vector = Vector(array_2)

    point_2 = point_1.add(vector)

    line_1 = Line(point_1, vector)
    line_2 = Line.from_points(point_1, point_2)

    assert line_1.is_close(line_2)

    # A point and vector are not interchangeable.
    with pytest.raises(Exception):
        Line(vector, point_1)
