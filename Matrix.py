

from __future__ import annotations
from Matrix_Helpers import dot_product, first_non_zero_entry, all_zeros, \
    duplicate_rows, zeros_at_the_bottom, all_leading_ones, \
    leading_ones_to_the_right, is_rref_helper, row_reduce, move_zero_row


# from typing import Union
# import ast


class Matrix:
    """

    Matrices :)

    === Attributes ===

    m: The number of rows
    n: The number of columns
    unknowns: list of unknown variables
    rows: list of the rows
    columns: list of the columns

    """

    m: int
    n: int
    unknowns: list
    rows: tuple[list]
    columns: list[list]

    def __init__(self, l: list[list]):
        """

        """

        valid = 1
        size = len(l[0])
        for i in l:
            if type(i) != list or size != len(i):
                valid = 0

        if valid == 1:
            unknowns = []
            for row in l:
                for i in row:
                    if type(i) == str and i.isalpha():
                        for variable in i:
                            if variable not in unknowns:
                                unknowns.append(variable)
        else:
            raise SyntaxError('Invalid Matrix input! Input must be a nested '
                              'list.')

        columns = []

        for r in range(size):
            c = []
            for row in l:
                c.append(row[r])
            columns.append(c)

        self.m = len(l)
        self.n = size
        self.unknowns = unknowns
        self.rows = l
        self.columns = columns

        # Make the attributes private maybe

    # def rows(self):
    #     """
    #     """
    #
    #     print(' \n'.join(map(str, self.rows)))

    def size(self):
        """
        """
        print(str(self.m) + ' x ' + str(self.n))

    def print(self):
        """
        """

        rows = []
        for row in self.rows:
            r = []
            for n in row:
                r.append(str(n))
            rows.append(r)

        m = 0
        for row in rows:
            for s in row:
                if len(s) > m:
                    m = len(s)

        for row in rows:
            for s in row:
                i = row.index(s)
                row.remove(s)
                ns = (' ' * (m - len(s))) + s
                row.insert(i, ns)

        for row in rows:
            print(' '.join(row))

    def scale(self, s: float):
        """
        Scales the given Matrix.
        """

        rows = []
        for row in self.rows:
            r = []
            for n in row:
                r.append(n)
            rows.append(r)

        for row in rows:
            for i in range(self.n):
                row[i] = row[i] * s

        return Matrix(rows)

    def add(self, m):
        """
        Creates a new Matrix which is the sum of the given matrices.
        """

        if type(m) != Matrix:
            return print('You can only add matrices!')
        elif (self.m != m.m) or (self.n != m.n):
            return print('You can only add matrices of the same size!')

        l = []
        for r in range(self.m):
            s = []
            for c in range(self.n):
                if isinstance(self.rows[r][c] and m.rows[r][c], int):
                    s.append(self.rows[r][c] + m.rows[r][c])
                else:
                    s.append(str(self.rows[r][c]) + '+' + str(m.rows[r][c]))
            l.append(s)

        return Matrix(l)

    def subtract(self, m):
        """
        Creates a new matrix which you get by subtracting the given matrix
        from self.
        """

        if type(m) != Matrix:
            return print('You can only add matrices')
        elif (self.m != m.m) or (self.n != m.n):
            return print('You can only add matrices of the same size!')

        l = []
        for r in range(self.m):
            s = []
            for c in range(self.n):
                if isinstance(self.rows[r][c] and m.rows[r][c], int):
                    s.append(self.rows[r][c] - m.rows[r][c])
                else:
                    s.append(str(self.rows[r][c]) + '+' + str(m.rows[r][c]))
            l.append(s)

        return Matrix(l)

    def multiplied_by(self, b: Matrix):
        """
        """

        assert self.n == b.m

        nl = []
        for row in self.rows:
            nl2 = []
            for column in b.columns:
                nl2.append(dot_product(row, column))
            nl.append(nl2)

        return Matrix(nl)

    def is_square(self):
        """
        """

        return self.m == self.n

    def power_of(self, n: int):

        assert self.is_square()  # Change Assertion Error to printed message?

        lst = [self.multiplied_by(self)]
        for i in range(n-2):
            a = lst.pop()
            b = a.multiplied_by(self)
            lst.append(b)

        return lst.pop()

    def equal_to(self, m: Matrix):
        """
        """

        return self.rows == m.rows

    def transpose(self):
        """
        """

        rows = duplicate_rows(self.columns)
        return Matrix(rows)

    def is_ref(self):
        """
        Returns True if the given Matrix is in its Row Echelon Form (REF).
        Returns False otherwise.
        """

        if all_zeros(self.rows):
            return True
        elif zeros_at_the_bottom(self.rows) and all_leading_ones(self.rows) \
                and leading_ones_to_the_right(self.rows):
            return True
        else:
            return False

    def is_rref(self):
        """
        Returns True if the given Matrix is in its Row Echelon Form (REF).
        Returns False otherwise.
        """

        return self.is_ref() and is_rref_helper(self.rows)

# To be continued..

    def rref(self):
        """
        """

        rows = duplicate_rows(self.rows)

        new_matrix = Matrix(rows)
        start = 0

        while not new_matrix.is_rref():
            lst = first_non_zero_entry(new_matrix.rows, new_matrix.columns, start)
            rows = new_matrix.rows
            for index in range(len(rows[0])):  # Column Index, can choose from any row
                num = rows[lst[1]].pop(index)
                num /= lst[0]  # Zero Division Error
                if num == int(num):
                    num = int(num)  # Will turn 4.0 into 4
                else:
                    num = num  # Should turn decimal values to fractions (1.5 to 3/2)
                rows[lst[1]].insert(index, num)
            indices = [lst[2], lst[1]]  # Column index, row index
            row_reduce(rows, indices)
            start += 1
            move_zero_row(rows)
            new_matrix = Matrix(rows)

        return new_matrix

    # Matrices that the algorithm fails:
    # 1) [ [0,2,0,2], [3,3,6,0], [2,1,4,-1] ] - Zero Division Error !SOLVED!
    # 2) [ [3,1,-4,-1], [1,0,10,5], [4,1, 6, 1] ] - wrong rref
    # 3) [1,1,-1, 4], [2, 1, 3, 0], [0, 1, -5, 8] ] - wrong rref
    # rows = duplicate_rows(A.rows)
    # new_matrix = Matrix(rows)
    # start = 0


def trees(l1, l2, l3) -> float:
    """
    """
    num = 0
    for i in range(len(l1)):
        if l2[i] == 1:
            i2 = 0
        elif l2[i] == 2:
            i2 = 1
        else:
            i2 = 2
        num += (l1[i] * l3[i2])
    return num


