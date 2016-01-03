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
        self.send = None
        self.size = 0
        self.arrayLength = 1
        self.current = None
        self.currentIndex = 0
        self.parentIndex = 0
        self.temp = None
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

    def findParent(self):
        if (self.currentIndex % 2) == 0:
            self.parentIndex = self.currentIndex / 2
        else:
            self.parentIndex = (self.currentIndex - 1) /2

    def findChild(self, parent):
        return parent * 2

    def swap(self, x):
        self.findParent()

        if self.current.prev.data[self.parentIndex] > self.current.data[self.currentIndex]:
            self.temp = self.current.prev.data[self.parentIndex]
            self.current.prev.data[self.parentIndex] = self.x
            self.current.data[self.currentIndex] = self.temp
            self.current = self.current.prev
            return self.parentIndex
        else:
            return -1

    def sort(self, x):
        while self.current.prev != None and self.currentIndex != -1 :
            self.currentIndex = self.swap(x)

    def add(self, x):
        self.current.data[self.current.size] = x
        self.currentIndex = self.current.size
        self.current.size += 1

    def insert(self, x):

        if self.isEmpty():
            self.newArray = np.zeros(1)
            self.appendArray(self.newArray)

        if self.end.size == self.arrayLength :
            self.newArray = np.zeros((self.arrayLength*2))
            self.appendArray(self.newArray)

        self.current = self.end
        self.add(x)
        self.sort(x)

    def findMin(self):
        min = -1

        if self.isEmpty():
            print ("empty")
            return

        else:
            min = self.start.data[0]

        return min

    def deleteSort(self, parent):
        left = self.findChild(parent)
        right = left + 1
        if self.current.next != None:
            if self.current.next.data[left] < self.current.next.data[right]:
                child = left
            else:
                child = right
            if self.current.next.data[child] < self.current.data[parent] and self.current.next.data[child] != 0 :
                temp = self.current.data[parent]
                self.current.data[parent] = self.current.next.data[child]
                self.current.next.data[child] = self.temp
                self.current = self.current.getNext()
                self.deleteSort(child)
            else:
                return
        elif self.current == self.end:
            self.end.data[0] = 0

        else:
            return

    def deleteMin(self):
        min = self.findMin()
        self.current =  self.start
        if self.isEmpty():
            raise Exception("empty")
        elif self.start == self.end:
            self.end.data[0] = 0
            self.end.size -= 1
            self.arrayLength -= 1
            self.start = None
            self.end = None
            return min
        else:
            self.current.data[0] = self.end.data[self.end.size -1]
            self.end.data[self.end.size-1] = 0
            self.end.size  -= 1
            self.arrayLength -= 1
            self.deleteSort(0)

        if self.end.size == 0:
            self.end = self.end.getPrev()

        return min

    def appendArray(self, val):
        nptr = self.Node(val, None, None, 0)
        self.size += 1
        if self.start == None:
            self.start = nptr
            self.end =  self.start
            self.arrayLength = 1
        else:
            self.arrayLength *= 2
            self.end.next = nptr
            nptr.prev = self.end
            self.end = nptr

    def insertArray(self, val, pos):
        self.nptr = self.Node(val, None, None, 0)
        self.ptr = self.start
        pos -= 1
        for i in range (0, size):
            if i == pos:
                self.temp = self.ptr.getNext()
                self.ptr.setNext(self.nptr)
                self.nptr.setNext(self.temp)
                self.nptr.setPrev(self.ptr)
                self.temp.setPrev(self.nptr)
                break
            self.ptr = self.ptr.getNext()
        self.size += 1

    def deleteArray(self, pos):
        if pos == 1:
            self.start = self.start.getNext()
            self.size -= 1
            return
        if pos == self.size:
            self.s = self.start
            self.t = self.start
            while self.s != self.end:
                self.t = self.s
                self.s = self.s.getNext()
            self.end = self.t;
            self.end.setNext(None)
            self.size -= 1
            return
        self.ptr = self.start
        pos -= 1
        for i in range (1, (self.size-1)):
            if i == pos:
                self.temp = self.ptr.getNext()
                self.temp = self.temp.getNext()
                self.ptr.setNext(self.temp)
                self.temp.setPrev(self.ptr)
                break
            self.ptr = self.ptr.getNext()
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
        self.ptr = self.start
        #print (self.start.data)
        #self.ptr = self.start.getNext()
        while self.ptr != None:
            print (self.ptr.data)
            self.ptr = self.ptr.getNext()
            print ("\n")


print ("hello world")
ll = LinkedList()
for i in range(1, 50):
    if i % 2 == 0:
        ll.insert(i/2)
    else:
        ll.insert(i)

#for i in range (0, 4999):
#    ll.deleteMin()

ll.display()
