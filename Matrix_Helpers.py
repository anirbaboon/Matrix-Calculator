
from __future__ import annotations
from typing import Union


def dot_product(row: list, column: list):
    """
    >>> dot_product([1,2,3], [1,2,1])
    8
    """

    assert len(row) == len(column)

    products = []
    for i in range(len(row)):
        products.append(row[i] * column[i])
    ans = 0
    for i in products:
        ans += i
    return ans


def all_zeros(rows: list[list]):
    """
    Returns True if the nested list consists entirely of zeros.

    Returns False otherwise.
    """

    for row in rows:
        for n in row:
            if n!= 0:
                return False
    return True


def zero_rows(rows: list[list]) -> list[int]:
    """
    Returns the list of indices of <rows>, where there are rows of all zeros.

    Returns an Empty list if <rows> has no rows of all zeros.
    """

    indices = []  # Accumulates the indices
    for index in range(len(rows) - 1):
        zero_row = 1  # It is a zero row
        for num in rows[index]:
            if num != 0:
                zero_row = 0  # It is not a zero row
        if zero_row == 1:
            indices.append(index)
    return indices


def zeros_at_the_bottom(rows: list[list]) -> bool:
    """
    Returns True if all rows consisting entirely of zeros are the bottom.

    Returns False otherwise.
    """

    indices = zero_rows(rows)
    total_rows = []

    for i in range(len(rows)):
        total_rows.append(i)

    bottom_rows = total_rows[len(rows) - len(indices):]

    return bottom_rows == indices


def all_leading_ones(rows: list[list]) -> bool:
    """
    Returns True if all rows in <rows> have a leading 1 or only have zeros.
    Returns False otherwise.
    """

    for row in rows:
        if leading_one(row) is False:
            return False
    return True


def leading_one(row: list) -> bool:
    """

    """
    # Helper for all_leading_ones

    valid = 0
    for num in row:
        if valid == 0 and num not in [0, 1]:
            return False
        if valid == 0 and num == 1:
            valid = 1
    return True


def leading_ones_to_the_right(rows: list[list]) -> bool:
    """

    """
    indices = leading_ones_to_the_right_helper(rows)
    found = 0
    for index in range(len(indices)):
        if found == 0:
            if indices[index] == 0.5:
                first_zero_row = index
                found = 1

    if found == 1:
        sliced_indices = indices[:first_zero_row]
    else:
        sliced_indices = indices

    if len(sliced_indices) > 1:
        a = sliced_indices[0]
        for num in sliced_indices[1:]:
            if num <= a:
                return False
            a = num
    return True


def leading_ones_to_the_right_helper(rows: list[list]) -> list:
    """
    Returns the list of indices of the leading ones in <rows>.
    """
    indices = []
    for row in rows:
        found = 0
        for i in range(len(row)):
            if found == 0 and row[i] == 1:
                indices.append(i)
                found = 1
            if i == (len(row) - 1) and found == 0:
                indices.append(0.5)  # Index 0.5 represents a row of zeros
    return indices


def is_rref_helper(rows: list[list]) -> bool:
    """
    Returns true if each leading one in is the only non-zero entry in its
    respective column.
    Returns False otherwise.
    Assumes that the given "Matrix" is already in a REF form.
    """

    indices = leading_ones_to_the_right_helper(rows)

    for num in range(len(indices)):  # num is the index of row in rows also
        column_index = indices[num]
        row_index = 0
        if column_index != 0.5:
            for row in rows:
                if row_index != num:
                    if row[column_index] != 0: # ci is not int?
                        return False
                row_index += 1
    return True


def first_non_zero_entry(rows: list, columns: list, start: int) -> list:
    """
    Returns a list containing the first non-zero entry from the top-left and
    the index of it's corresponding row in <rows>, and the index
    of the corresponding column, respectively. Also moves the corresponding
    row to the top.

    Returns 0 as the first entry of the returned list if there are no
    non-zero entries.
    """
    ans = []
    column_index = start
    for ci in range(start, len(columns)):
        for ri in range(start, len(columns[ci])):
            if columns[ci][ri] != 0:
                num = columns[ci][ri]
                ans = [num, ri, ci]
                rows.insert(start, rows[ri])
                rows.pop(ri)
                return ans
    if ans is []:
        return [0, 0, 0]

    # ans = []
    #
    # for row_index in range(start, len(rows)):
    #     row = rows[row_index]
    #     for column_index in range(len(rows[row_index])):
    #         real_row_index = row_index
    #         if row[column_index] != 0:
    #             ans.append(row[column_index])
    #             row = rows.pop(real_row_index)
    #             rows.insert(start, row)
    #             ans.append(start)
    #             ans.append(column_index)
    #             return ans
    #         elif real_row_index == (len(rows)-1) and column_index == (len(
    #                 rows[row_index])-1):
    #             ans.append(0)
    #             ans.append(real_row_index)
    #             ans.append(column_index)
    #             return ans

    # found = 0
    # ans = []
    # for i2 in range(start, len(rows)):  # Row index
    #     for i in range(start, len(rows[0])):  # Column index adjusted for
    #         # <start>
    #         real_index = i2 + start
    #         if found == 0 and rows[real_index][i] != 0:
    #             ans.append(rows[real_index][i])
    #             ans.append(real_index)
    #             found = 1
    #             row = rows.pop(real_index)
    #             rows.insert(start, row)
    #             return ans
    #         elif found == 0 and rows[real_index] == rows[-1]:
    #             ans.append(0)
    #             ans.append(real_index)
    # return ans


def row_reduce(rows: list[list], indices: list[int]) -> None:
    """
    Row reduces all the rows below and above the given row index.

    <indices> = [column index, row index]
    """

    column_index = indices[0]
    row_index = indices[1]

    for i in range(len(rows)):
        if i != row_index:
            num = rows[i][column_index]
            multiplied_row = multiply_row_by(rows[row_index], num)
            subtracted_row = subtract_row_by(rows[i], multiplied_row)
            rows.pop(i)
            rows.insert(i, subtracted_row)


def multiply_row_by(row: list, num: float) -> list:  # row_reduce helper
    """
    Multiplies <row> with <num> without mutating <row>
    """
    rows = duplicate_rows([row])
    duplicated_row = rows[0]

    for i in range(len(duplicated_row)):
        number = duplicated_row.pop(i)
        number *= num
        duplicated_row.insert(i, number)

    return duplicated_row


def subtract_row_by(row1: list, row2: list) -> list:
    """
    Subtract <row> by <num> without mutating <row>.
    """
    rows = duplicate_rows([row1])
    duplicated_row = rows[0]

    for i in range(len(duplicated_row)):
        num = duplicated_row.pop(i)
        num -= row2[i]
        if num == int(num):
            num = int(num)  # Will turn 4.0 into 4
        else:
            num = num  # Should turn decimal values to fractions (1.5 to 3/2)
        duplicated_row.insert(i, num)

    return duplicated_row


def move_zero_row(rows: list) -> None:
    """"
    Removes any zero rows to the end (bottom).
    """
    lst = zero_rows(rows)
    if lst is not []:
        for i in lst:
            rows += [rows[i]]
            rows.pop(i)


def duplicate_rows(rows: list[list]) -> list:
    """
    """

    new_row = []
    for row in rows:
        r = []
        for n in row:
            r.append(n)
        new_row.append(r)

    return new_row



if __name__ == '__main__':
    import doctest
    doctest.testmod()

