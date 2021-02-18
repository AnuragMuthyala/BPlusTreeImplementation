import sys

ORDER = 3
global main_root
global r
r = True

class Node():

    def __init__(self):
        self.__vals = [0 for i in range(ORDER-1)]
        self.__filled = 0
        self.p = ['NULL' for i in range(ORDER)]
        self.__leaf = True
        self.next = 'NULL'

    def not_leaf(self):
        self.__leaf = False

    def add_value(self, v):
        if self.__filled >= ORDER-1:
            print("error")
        else:
            i = 0
            while i < self.__filled:
                if self.__vals[i] > v:
                    break
                i += 1
            
            j = self.__filled-1
            while j >= i:
                self.__vals[j+1] = self.__vals[j]
                j -= 1

            self.__vals[i] = v
            self.__filled += 1

    def traverse(self):
        print('Pass')
        for i in range(self.__filled):
            print(self.__vals[i])
        for i in range(len(self.p)):
            if self.p[i] != 'NULL':
                self.p[i].traverse()

    def insert(self, v):
        global main_root
        global r
        i = 0
        j = 0
        is_root = False
        if (r):
            r = False
            is_root = True
        if self.__leaf:
            if self.__filled < ORDER-1:
                self.add_value(v)
            else:
                a = [0 for i in range(ORDER)]
                i = 0
                j = 0
                while i < self.__filled:
                    if self.__vals[i] > v:
                        break
                    a[j] = self.__vals[i]
                    j += 1
                    i += 1
                a[j] = v
                j += 1
                while i < self.__filled:
                    a[j] = self.__vals[i]
                    j += 1
                    i += 1
                right = Node()
                self.__filled = 0
                i = 0
                while i <= ORDER // 2:
                    self.add_value(a[i])
                    i += 1
                left = self
                i = (ORDER//2) + 1
                while i < ORDER:
                    right.add_value(a[i])
                    i += 1
                right.next = left.next
                left.next = right
                if is_root:
                    main_root = Node()
                    main_root.add_value(a[ORDER//2])
                    main_root.p[0] = left
                    main_root.p[1] = right
                    main_root.not_leaf()
                    return False
                else:
                    val = a[ORDER // 2]
                    return (val, left, right)

        else:
            i = 0
            while i < self.__filled:
                if self.__vals[i] > v:
                    break
                i += 1
            t = self.p[i].insert(v)
            if not t:
                return False
            else:
                if self.__filled < ORDER-1:
                    self.add_value(t[0])
                    self.p[self.__filled - 1] = t[1]
                    self.p[self.__filled] = t[2]
                    return False
                else:
                    a = [0 for i in range(ORDER)]
                    points = ['NULL' for i in range(ORDER+1)]
                    i = 0
                    j = 0
                    k = 0
                    while i < self.__filled:
                        if self.__vals[i] > t[0]:
                            break
                        a[j] = self.__vals[i]
                        j += 1
                        i += 1
                    a[j] = t[0]
                    k = j
                    j += 1
                    while i < self.__filled:
                        a[j] = self.__vals[i]
                        j += 1
                        i += 1
                    if k == 0:
                        points[0] = t[1]
                        points[1] = t[2]
                        points[2] = self.p[1]
                        points[3] = self.p[2]
                    elif k == 1:
                        points[0] = self.p[0]
                        points[1] = t[1]
                        points[2] = t[2]
                        points[3] = self.p[2] 
                    else:
                        points[0] = self.p[0]
                        points[1] = self.p[1]
                        points[2] = t[1]
                        points[3] = t[2]
                    right = Node()
                    self.__filled = 0
                    for i in range(len(self.p)):
                        self.p[i] = 'NULL'
                    i = 0
                    k = 0
                    while i < ORDER // 2:
                        self.add_value(a[i])
                        self.p[k] = points[i]
                        i += 1
                        k += 1
                    self.p[k] = points[i]
                    k += 1
                    left = self
                    i = (ORDER//2) + 1
                    k = 0
                    while i < ORDER:
                        right.add_value(a[i])
                        right.p[k] = points[i]
                        i += 1
                        k += 1
                    right.p[k] = points[i]
                    right.not_leaf()
                    if is_root:
                        main_root = Node()
                        main_root.add_value(a[ORDER//2])
                        main_root.p[0] = left
                        main_root.p[1] = right
                        main_root.not_leaf()
                        return False
                    else:
                        val = a[ORDER // 2]
                        return (val, left, right)

    def find(self, v):
        if self.__leaf:
            for i in range(self.__filled):
                if v == self.__vals[i]:
                    return True
            return False
        else:
            i = 0
            while i < self.__filled:
                if v == self.__vals[i]:
                    return True
                elif v < self.__vals[i]:
                    val = self.p[i].find(v)
                    return val
                i += 1
            val = self.p[i].find(v)
            return val

    def count(self, v, count):
        if self.__leaf:
            for i in range(self.__filled):
                if v == self.__vals[i]:
                    count += 1
            return count
        else:
            i = 0
            while i < self.__filled:
                if v == self.__vals[i]:
                    count += 1
                    val = self.p[i].count(v, count)
                    return val
                elif v < self.__vals[i]:
                    val = self.p[i].count(v, count)
                    return val
                i += 1
            val = self.p[i].count(v, count)
            return val

    def range_numbers(self, l, h, count):
        if self.__leaf:
            for i in range(self.__filled):
                if self.__vals[i] > h:
                    return count
                if l <= self.__vals[i] and self.__vals[i] <= h:
                    count += 1
            if self.next == 'NULL':
                return count
            count = self.next.range_numbers(l, h, count)
            return count
        else:
            i = 0
            while i < self.__filled:
                if l == self.__vals[i]:
                    val = self.p[i].range_numbers(l, h, 0)
                    return val
                elif l < self.__vals[i]:
                    val = self.p[i].range_numbers(l, h, 0)
                    return val
                i += 1
            val = self.p[i].range_numbers(l, h, 0)
            return val

n = Node()
main_root = n 
head = n
filename = sys.argv[1]

with open(filename) as o:

    while True:
        line = o.readline()

        if not line:
            break
        else:
            l = line.split(' ')
            query = l[0].upper()
            if query == 'INSERT':
                n.insert(int(l[1]))
                n = main_root

            elif query == 'FIND':
                if n.find(int(l[1])):
                    print("Yes")
                else:
                    print("No")

            elif query == 'COUNT':
                c = n.count(int(l[1]), 0)
                print(c)

            elif query == 'RANGE':
                r = n.range_numbers(int(l[1]), int(l[2]), 0)
                print(r)

            else:
                print("Error")
        r = True
