class Element:
    def __init__(self, k, v, i):
        self._key = k
        self._value = v
        self._index = i

    def __str__(self):
        result = "key: " + str(self.key()) + ", value: " + str(self.value()) + ", index: " + str(self.index())
        return result

    def __eq__(self, other):
        return self._key == other._key

    def __lt__(self, other):
        return self._key < other._key

    def index(self):
        return self._index

    def value(self):
        return self._value

    def key(self):
        return self._key

    def set_key(self, new):
        if isinstance(new, float):
            self._key = new


    def wipe(self):
        self._key = None
        self._value = None
        self._index = None


class APQ:
    def __init__(self):
        self._body = list()

    def min(self):
        return self._body[0]

    def length(self):
        return len(self._body)

    def __str__(self):
        result = ""
        for i in self._body:
            result = result + ", " + str(i)
        return result

    def bubbleUp(self, i):
        if i != 0:
            if self._body[i] < self._body[(i - 1) // 2]:
                t = self._body[(i - 1) // 2]
                self._body[i]._index = (i - 1) // 2
                self._body[(i - 1) // 2] = self._body[i]
                t._index = i
                self._body[i] = t
                self.bubbleUp((i - 1) // 2)


    def smallest_child(self, i):
        if (i * 2) + 2 > self.length() - 1:
            return (i * 2) + 1
        else:
            if self._body[(i * 2) + 1] < self._body[(i * 2) + 2]:
                return (i * 2) + 1
            else:
                return (i * 2) + 2


    def bubbleDown(self, i):
        if (i * 2) + 1 < self.length() - 1:
            schild = self.smallest_child(i)
            if self._body[i] > self._body[schild]:
                t = self._body[schild]    # save t as the the smaller child
                self._body[i]._index = schild  # swap the indexes of the the parent and child
                t._index = i
                self._body[schild] = self._body[i]
                self._body[i] = t
                self.bubbleDown(schild)



    def add(self, key, value):
        e = Element(key, value, len(self._body))
        if len(self._body) == 0:
            self._body.append(e)
            return e
        self._body.append(e)
        self.bubbleUp(e.index())
        return e

    def remove_min(self):
        elem = self.min()
        self._body[0] = self._body[self.length() - 1]
        self._body[0]._index = 0
        self._body.pop()
        self.bubbleDown(0)
        return elem

    def get_elem(self, e):
        for x in self._body:
            if x.value() == e:
                return x
        return None

    def get_key(self, element):
        return self.get_elem(element).key()


    def update_key(self, element, key):
        old = element.key()
        element.set_key(key)
        if old < key:
            self.bubbleDown(element.index())
        else:
            self.bubbleUp(element.index())

    def remove(self, element):
        i = element.index()
        t = self._body[self.length() - 1]
        t._index = i
        self._body[self.length() - 1] = element
        self._body[i] = t
        element._index = self._body[self.length() - 1]
        self._body.pop()
        if self._body[i] < self._body[(i - 1) //2]:
            self.bubbleUp(i)
        else:
            self.bubbleDown(i)
        return element



def test():
    apq = APQ()
    p = apq.add(33, "yes")
    apq.add(55, "no")
    q = apq.add(66, "ter")
    c = apq.add(21, "geh")
    apq.add(20, "n")
    d = apq.add(5, "please")
    print(apq.min())
    print(apq)
    print(p.index())
    apq.update_key(c, 56)
    apq.update_key(d, 1)
    apq.update_key(q, 0)
    print(apq)
    print(apq.smallest_child(1))
    apq.remove_min()
    print(apq)
    apq.remove_min()
    print(apq)
    fo = apq.add(30, "Ga")
    print(apq)
    apq.update_key(fo, 29)
    print(apq)



if __name__ == "__main__":
    test()
