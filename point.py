class Point:
    """
    A point identified by (x,y) coordinates.

    supports: +, -, str, repr, eq

    clone  -- construct a duplicate
    move_to  -- reset x & y
    """

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __add__(self, point: 'Point') -> 'Point':
        """Point(x1+x2, y1+y2)"""
        return Point(self.x + point.x, self.y + point.y)

    def __sub__(self, point: 'Point') -> 'Point':
        """Point(x1-x2, y1-y2)"""
        return Point(self.x - point.x, self.y - point.y)

    def __str__(self) -> str:
        return "(%s, %s)" % (self.x, self.y)

    def __repr__(self) -> str:
        return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def clone(self) -> 'Point':
        """Return a full copy of this point."""
        return Point(self.x, self.y)

    def move_to(self, x: int, y: int):
        """Reset x & y coordinates."""
        self.x = x
        self.y = y
