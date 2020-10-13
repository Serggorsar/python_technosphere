from itertools import zip_longest


class List(list):

    def __init__(self, *args):
        super(List, self).__init__(args)

    def __add__(self, other):
        return __class__(*[a + b for a, b in zip_longest(self, other, fillvalue=0)])

    def __sub__(self, other):
        return __class__(*[a - b for a, b in zip_longest(self, other, fillvalue=0)])

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)

if __name__ == "__main__":
    a = List(1, 4)
    print(a)
    b = List(3, 2, 9)
    print(a + b, a, b)
    b.append(8)
    print(a + b, a, b)
    c = List()
    print(a - b, a, b, c)
    print(a < b, b < a)
    print(a >= b, b >= a)
    print(c == List(), c <= List())
