# ScriptName: pytoonz.py
# Author : Ben Murphy  StudentNumber: 119394463

class Track:
    def __init__(self, name, artiste, timesplayed):
        self._name = name
        self._artiste = artiste
        self._timesplayed = timesplayed

    def __str__(self):
        track_des = "%s: %s, (%i)" % (self._name, self._artiste, self._timesplayed)
        return track_des

    def get_artiste(self):
        return self._artiste

    def get_name(self):
        return self._name

    def play(self):
        self._timesplayed += 1
        return "Currently playing: %s By %s" % (self._name, self._artiste)


def test_track():
    t0 = Track("Kingslayer", "Bring Me The Horizon/Babymetal", 0)
    print(t0)
    t0.play()
    print(t0.get_artiste())
    print(t0.get_name())


class DLLNode:
    def __init__(self, item, prevnode, nextnode):
        self._element = item
        self._next = nextnode
        self._prev = prevnode


class Pytoonz:
    def __init__(self):
        self._size = 0
        self._head = DLLNode(None, None, None)
        self._tail = DLLNode(None, self._head, None)
        self._head._next = self._tail
        self._current = None

    def length(self):
        return self._size

    def get_current(self):
        if self._size == 0:
            return None
        return self._current._element

    def __str__(self):
        if self._size == 0:
            return None
        x = 0
        node = self._head._next
        while x < self.length():  # use the str from Track
            if x == 0:
                print("Playlist:")
            if node == self._current:
                print("-->", end=" ")
                print(node._element)
                x += 1
                node = node._next
                continue
            print(node._element)
            node = node._next
            x += 1
        return ""  # Not returning a string causes an error

    def add_after(self, track):  # if List is empty use the head and tail to add it in
        if self._size == 0:
            track._prev = self._head
            track._next = self._tail
            self._head._next = track
            self._tail._prev = track
            self._current = track
            self._size += 1
        else:
            track._prev = self._current
            track._next = self._current._next
            temp = self._current._next
            self._current._next = track
            temp._prev = track
            self._size += 1

    def add_track(self, track):
        if self._size == 0:
            self.add_after(track)
        else:
            original = self._current  # save the current pointer as it will be changed
            self._current = self._tail._prev
            self.add_after(track)  # adds to the end of the list
            self._current = original

    def reset(self):
        self._current = self._head._next
        if self._size == 0:
            self._current = None

    def remove_current(self):
        if self._size == 0:
            return None
        temp = self._current._prev
        temp2 = self._current._next
        temp._next = temp2
        temp2._prev = temp
        if temp == self._head and temp2 == self._tail:
            self._current = None
        else:
            if temp2 == self._tail:  # if the next node is the tail it wraps around to the first item in the list
                self._current = self._head._next
            else:
                self._current = temp2
        self._size -= 1

    def next_track(self):
        if self._size > 0:  # if the list is empty do nothing
            self._current = self._current._next
            if self._current == self._tail:
                self._current = self._head._next

    def prev_track(self):
        if self._size > 0:
            self._current = self._current._prev
            if self._current == self._head:
                self._current = self._tail._prev

    def play(self):
        try:
            print(self._current._element.play())
        except TypeError:
            print("ERROR, there is no currently selected track")


def test_list():
    t0 = Track("Kingslayer", "Bring Me The Horizon/Babymetal", 0)
    t1 = Track("Send Me An Angel", "Highly Suspect", 0)
    t2 = Track("Hush", "HELLYEAH", 0)
    node0 = DLLNode(t0, None, None)
    node1 = DLLNode(t1, None, None)
    node2 = DLLNode(t2, None, None)
    playlist = Pytoonz()
    playlist.add_after(node0)
    playlist.add_track(node1)
    playlist.add_track(node2)
    playlist.prev_track()
    playlist.next_track()
    playlist.next_track()
    playlist.next_track()
    playlist.prev_track()
    print(playlist)
    playlist.remove_current()
    playlist.play()
    print(playlist.get_current())
    print(playlist.length())


#test_list()


def test2():
    pytoonz = Pytoonz()
    track1 = Track("Looking for me", "Paul Woolford and Diplo/Lomax", 0)
    t1 = DLLNode(track1, None, None)
    track2 = Track("Giants", "Dermot Kennedy", 0)
    t2 = DLLNode(track2, None, None)
    track3 = Track("Holy", "Justin Bieber Ft Chance", 0)
    t3 = DLLNode(track3, None, None)
    pytoonz.add_track(t1)
    pytoonz.add_track(t2)
    pytoonz.add_track(t3)
    print(pytoonz)
    print(pytoonz.get_current())
    pytoonz.play()
    pytoonz.next_track()
    print(pytoonz.get_current())
    pytoonz.prev_track()
    pytoonz.remove_current()
    print(pytoonz)
    track4 = Track("Lemonade", "Internet Money / Gunna / Toliver", 0)
    t4 = DLLNode(track4, None, None)
    pytoonz.add_track(t4)
    pytoonz.next_track()
    pytoonz.play()
    print(pytoonz.length())
    print(pytoonz)


#test2()

def test3():
    playlst = Pytoonz()
    t0 = Track("Don't know What to say", "Bring Me The Horizon/Babymetal", 0)
    t1 = Track("Lydia", "Highly Suspect", 0)
    t2 = Track("Glitter and Gold", "Barns Courtney", 0)
    node0 = DLLNode(t0, None, None)
    node1 = DLLNode(t1, None, None)
    node2 = DLLNode(t2, None, None)
    print(playlst.length())
    playlst.next_track()
    playlst.next_track()
    playlst.prev_track()
    playlst.add_after(node0)
    playlst.add_track(node2)
    playlst.next_track()
    playlst.play()
    playlst.next_track()
    playlst.play()
    playlst.add_track(node1)
    playlst.next_track()
    playlst.play()
    print(playlst)
    print(playlst.length())

# test3()

def test4():
    pytoonz = Pytoonz()
    track1 = Track("Dear Diary", "Bring Me The Horizon", 0)
    track2 = Track("Mr.Brightside", "The Killers", 0)
    track3 = Track("Ode To The Mets", "The Strokes", 0)
    track4 = Track("Dark Necessities", "Red Hot Chili Peppers", 0)
    track5 = Track("Ain't No Rest For The Wicked", "Cage The Elephant", 0)
    track6 = Track("Mother Mary", "Badflower", 0)
    t1 = DLLNode(track1, None, None)
    t2 = DLLNode(track2, None, None)
    t3 = DLLNode(track3, None, None)
    t4 = DLLNode(track4, None, None)
    t5 = DLLNode(track5, None, None)
    t6 = DLLNode(track6, None, None)
    pytoonz.prev_track()
    pytoonz.add_track(t1)
    pytoonz.add_track(t3)
    pytoonz.add_track(t6)
    print(pytoonz)
    pytoonz.play()
    pytoonz.next_track()
    pytoonz.next_track()
    pytoonz.remove_current()
    print(pytoonz)
    pytoonz.add_track(t4)
    pytoonz.prev_track()
    print(pytoonz)
    pytoonz.add_after(t5)
    print(pytoonz)
    pytoonz.prev_track()
    pytoonz.play()
    pytoonz.add_after(t2)
    pytoonz.prev_track()
    pytoonz.prev_track()
    pytoonz.play()
    print(pytoonz)
    print(pytoonz.length())
    pytoonz.remove_current()
    print(pytoonz.get_current())
    pytoonz.remove_current()
    print(pytoonz.get_current())
    pytoonz.remove_current()
    print(pytoonz.length())
    print(pytoonz)

#test4()
