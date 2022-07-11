from array import array
import math


class Vector:
    typecode = 'd'

    def __init__(self, components):
        self.components = array(self.typecode, components)

    def __len__(self):
        return len(self.components)

    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self.components[key])
        return self.components[key]

    def __setitem__(self, key, value):
        self.components[key] = value

    def __repr__(self):
        components = repr(self.components)[repr(self.components).find('[') + 1: repr(self.components).find(']')]
        return f'Vector({components})'

    def __str__(self):
        return repr(self)

    def __abs__(self):
        square_sum = 0
        for i in self.components:
            square_sum += i ** 2
        return square_sum ** 0.5

    def __iter__(self):
        return iter(self.components)

    def __mul__(self, scalar):
        try:
            factor = float(scalar)
        except TypeError:
            return NotImplemented
        return Vector(n * factor for n in self)

    def __rmul__(self, scalar):
        return self * scalar

    def __add__(self, other):
        if other == 0:
            return self
        try:
            pairs = zip(self.components, other.components)
            return Vector(a + b for a, b in pairs)
        except TypeError:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return Vector(-x for x in self)

    def __pos__(self):
        return Vector(self)

    def __bool__(self):
        return bool(abs(self))

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return -self + other

    def normalized(self):
        return self * (1 / abs(self))


class Matrix:
    typecode = 'd'

    def __init__(self, mtx):
        self.rows_num = len(mtx[0])
        self.cols_num = len(mtx)
        self.rows = [Vector([col[i] for col in mtx]) for i in range(self.rows_num)]
        self.cols = [Vector(col) for col in mtx]
        if not (all(len(self.rows[i]) == len(self.rows[0]) for i in range(self.rows_num)) or len(self.cols[i]) == len(
                self.cols[0]) for i in range(self.cols_num)):
            raise NotImplementedError
        self.components = array(self.typecode, [i for row in self.rows for i in row])
        self.size = (self.rows_num, self.cols_num)

    def __iter__(self):
        return iter(self.cols)

    def __len__(self):
        return len(self.cols)

    def __repr__(self):
        s = ('{:8.3f}' * self.cols_num + '\n') * self.rows_num
        return ('Matrix(\n' + s + ')').format(*self.components)

    def __add__(self, other):
        if self.rows_num == other.rows_num and self.cols_num == other.cols_num:
            return Matrix([i + j for i, j in zip(self.cols, other.cols)])
        else:
            raise NotImplementedError

    def __radd__(self, other):
        return self + other

    def __str__(self):
        return repr(self)

    def transpose(self):
        return Matrix(self.rows)

    def __getitem__(self, key):

        if isinstance(key, tuple):
            r, c = key
            if isinstance(r, slice):
                if isinstance(c, slice):
                    return Matrix([Vector([row[i] for row in self.rows[r]]) for i in range(self.cols_num)[c]])
                else:
                    return Vector([row[c] for row in self.rows[r]])
            elif isinstance(c, slice):
                return Vector([col[r] for col in self.cols[c]])
            else:
                return self.cols[c][r]

        elif isinstance(key, int):
            return self.cols[key]

    def __setitem__(self, key, value):
        r, c = key
        self.cols[c][r] = value
        self.rows[r][c] = value
        self.components[self.rows_num * r + c] = value


def dot(a, b):
    if isinstance(a, Vector) and isinstance(b, Vector):
        return sum(i * j for i, j in zip(a.components, b.components))
    elif isinstance(a, Matrix) and isinstance(b, Vector):
        return sum(i * j for i, j in zip(a, b))
    elif isinstance(a, Matrix) and isinstance(b, Matrix):
        return Matrix([dot(a, col) for col in b.cols])
    else:
        raise NotImplementedError


def angle(v1, v2):
    return math.acos(dot(v1, v2) / (abs(v1) * abs(v2)))