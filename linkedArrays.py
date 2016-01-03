#!/usr/bin/env python
import numpy as np

class LinkedList:
    class Node:

        def __init__(self, d, n, p, s):
            self.prev = p
            self.next = n
            self.data = d
            self.size = s

        def setNext(self, n):
            self.next = n

        def setPrev(self, p):
            self.prev = p

        def setData(self, d):
            self.data = d

        def setSize(self, s):
            self.size = s

        def getNext(self):
            return self.next

        def getPrev(self):
            return self.prev

        def getData(self, i):
            if i < self.size:
                return self.data[i]
            else:
                return -1

        def getSize(self):
            return self.size

    def __init__ (self):
        self.start = None
        self.end = None
        self.size = 0
        self.arrayLength = 1
        self.current = None
        self.currentIndex = 0
        self.parentIndex = 0
        self.toInsert = None

    def isEmpty(self):
        return self.start == None

    def makeEmpty(self):
        self.current = self.end
        while self.end.getPrev() != None:
            self.current = self.end.getPrev()
        self.end = None
        self.start = None

    def getSize(self):
        return self.size

    def size(self):
        numElements = (self.arrayLength/2) + self.end.size
        return numElements

    def findParent(self, cIndex):
        if (cIndex % 2) == 0:
            pIndex = cIndex / 2
        else:
            pIndex = (cIndex - 1) /2
        return pIndex

    def findChild(self, parent):
        return parent * 2

    def swap(self, x, c, cIndex):
        pIndex = self.findParent(cIndex)

        if c.prev.data[pIndex] > c.data[cIndex]:
            temp = c.prev.data[pIndex]
            c.prev.data[pIndex] = x
            c.data[cIndex] = temp
            c = c.getPrev()
            return pIndex
        else:
            return -1

    def sort(self, x, c):
        cIndex = 0
        while c.getPrev() != None and cIndex != -1 :
            cIndex = c.size-1
            cIndex = self.swap(x, c, cIndex)

    def add(self, x, c):
        c.data[c.size] = x
        c.size += 1

    def insert(self, x):

        if self.isEmpty():
            newArray = np.zeros(1)
            self.appendArray(newArray)

        if self.end.size == self.arrayLength :
            newArray = np.zeros((self.arrayLength*2))
            self.appendArray(newArray)

        self.add(x, self.end)
        self.sort(x, self.end)

    def findMin(self):
        min = -1

        if self.isEmpty():
            print ("empty")
            return

        else:
            min = self.start.data[0]

        return min

    def deleteSort(self, parent, c):
        left = self.findChild(parent)
        right = left + 1
        if c.next != None:
            if c.next.data[left] < c.next.data[right]:
                child = left
            else:
                child = right
            if c.next.data[child] < c.data[parent] and c.next.data[child] != 0 :
                temp = c.data[parent]
                c.data[parent] = c.next.data[child]
                c.next.data[child] = temp
                c = c.getNext()
                self.deleteSort(child, c)
            else:
                return
        elif c == self.end:
            return

        else:
            return

    def deleteMin(self, s, e):
        min = self.findMin()

        if self.isEmpty():
            raise Exception("empty")
        elif s == e:
            e.data[0] = 0
            e.size -= 1
            self.arrayLength -= 1
            s = None
            e = None
            return min
        else:
            print (e == None)
            s.data[0] = e.data[e.size -1]
            e.data[e.size-1] = 0
            e.size  -= 1
            self.arrayLength -= 1
            self.deleteSort(0, s)

        if e.size == 0:
            self.end = e.getPrev()

        return min

    def appendArray(self, val):
        nptr = self.Node(val, None, None, 0)
        self.size += 1
        if self.start == None:
            self.start = nptr
            self.end = self.start
            self.arrayLength = 1
        else:
            self.arrayLength *= 2
            self.end.next = nptr
            nptr.prev = self.end
            self.end = nptr

    def insertArray(self, val, pos):
        nptr = self.Node(val, None, None, 0)
        ptr = self.start
        pos -= 1
        for i in range (0, size):
            if i == pos:
                temp = ptr.getNext()
                ptr.setNext(nptr)
                nptr.setNext(temp)
                nptr.setPrev(ptr)
                temp.setPrev(nptr)
                break
            ptr = ptr.getNext()
        self.size += 1

    def deleteArray(self, pos):
        if pos == 1:
            self.start = self.start.getNext()
            self.size -= 1
            return
        if pos == self.size:
            s = self.start
            t = self.start
            while s != self.end:
                t = s
                s = s.getNext()
            self.end = t;
            self.end.setNext(None)
            self.size -= 1
            return
        ptr = self.start
        pos -= 1
        for i in range (1, (self.size-1)):
            if i == pos:
                temp = ptr.getNext()
                temp = temp.getNext()
                ptr.setNext(temp)
                temp.setPrev(ptr)
                break
            ptr = ptr.getNext()
        self.size -= 1

    def display(self):
        if self.size == 0:
            print ("empty")
            return
        if self.start == None:
            return
        if self.start.next == None:
            print(self.start.data)
            return
        ptr = self.start
        while ptr != None:
            print (ptr.data)
            ptr = ptr.getNext()
            print ("\n")

ll = LinkedList()
for i in range(1, 50):
    if i % 3 == 0:
        ll.insert(i/3)
    else:
        ll.insert(i)

#for i in range (0, 49):
#    ll.deleteMin(ll.start, ll.end)

ll.display()
