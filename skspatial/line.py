from dpcontracts import require, ensure

from .array import Point, Vector


class Line:
    @require(
        "The inputs must be a point and a vector.",
        lambda args: isinstance(args.point, Point) and isinstance(args.vector, Vector),
    )
    def __init__(self, point, vector):

        self.point = point
        self.direction = vector.unit()

    def __repr__(self):

        return f"Line(point={self.point}, direction={self.direction})"

    @classmethod
    @require(
        "The inputs must be two points.",
        lambda args: all(isinstance(x, Point) for x in args[1:]),
    )
    @require("The points must be different.", lambda args: args.point_a != args.point_b)
    @ensure("The output must be a line." "", lambda _, result: isinstance(result, Line))
    def from_points(cls, point_a, point_b):
        """Define a line from two points."""
        vector_ab = Vector.from_points(point_a, point_b)

        return cls(point_a, vector_ab)

    @ensure(
        "The output must be a point." "", lambda _, result: isinstance(result, Point)
    )
    def to_point(self, t=0):
        """
        Return a point along the line using a parameter t.

        Computed as line.point + t * line.direction.

        """
        return Point(self.point.array + t * self.direction.array)
