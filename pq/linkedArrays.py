#!/usr/bin/env python
import numpy as np

class Node:

	#initializes node instance with predefined values
	def __init__(self, data, next = None, prev = None, size = 0):
		self.prev = prev
		self.next = next
		self.data = data
		self.size = size

	def setNext(self, next):
		self.next = next

	def setPrev(self, prev):
		self.prev = prev

	def setData(self, data):
		self.data = data

	def setSize(self, size):
		self.size = size

	def getNext(self):
		return self.next

	def getPrev(self):
		return self.prev

	def getSize(self):
		return self.size

class LinkedArray:

	#intializes LinkedArrays instance then sets starting values
	def __init__ (self):
		self.start = None
		self.end = None
		self.size = 0
		self.arrayLength = 1
		self.current = None
		self.currentIndex = 0
		self.parentIndex = 0
		self.toInsert = None

	#checks if start is null
	def isEmpty(self):
		return self.start is None

	#deletes all the nodes in the LinkedArrays
	def makeEmpty(self):
		self.current = self.end
        
		while self.end.getPrev():
			self.current = self.end.getPrev()
        
		self.end = None
		self.start = None

	def getSize(self):
		return self.size

	#returns the amount of total elements in the priority queue
	def size(self):
		numElements = (self.arrayLength/2) + self.end.size #this takes all the availabe spaces, takes away the last array since it might not be full then adds the filled spaces from the last array
		return numElements

	#finds the parent of the current index
	def findParent(self, cIndex):
		pIndex = cIndex // 2
		return pIndex

	#finds the child of the current index
	def findChild(self, parent):
		return parent * 2

	#swaps the parent and child if necessary (will swap if child is smaller than parent)
	def swap(self, x, c, cIndex):
		pIndex = self.findParent(cIndex)

		#compares parent to child
		if c.prev.data[pIndex] > c.data[cIndex]:
			temp = c.prev.data[pIndex]
			c.prev.data[pIndex] = x
			c.data[cIndex] = temp
			c = c.getPrev()
			return pIndex
		else:
			return -1

	#calls swap until the queue is sorted
	def sort(self, x, c):
		cIndex = 0
		while c.getPrev() and cIndex != -1 :
			cIndex = c.size-1
			cIndex = self.swap(x, c, cIndex)

	#adds the element to the end of the queue
	def add(self, x, c):
		c.data[c.size] = x
		c.size += 1

	#checks if array needs to be created (and calls for creation if necessary) then calls to add element to queue then calls for sort
	def insert(self, x):

		#if there are no arrays, make one with size one (first array)
		if self.isEmpty():
			newArray = np.zeros(1)
			self.appendArray(newArray)

		#if last array is full make a new one twice the size
		if self.end.size == self.arrayLength :
			newArray = np.zeros((self.arrayLength*2))
			self.appendArray(newArray)
	
		#add it to the end of the queue then sort the queue
		self.add(x, self.end)
		self.sort(x, self.end)

	#finds the min element in the queue (should be element in first array if sorted correctly)
	def findMin(self):
		#set min to -1 so that deletemin will catch any errors trying to get start.data[0]
		min = -1
	
		#if its empty tell the user and exit
		if self.isEmpty():
			print ("empty")
			return

		else:
			min = self.start.data[0]

		return min

	#sorts the array after deletion of min element occurs
	def deleteSort(self, parent, c):
	
		#set the left index to its first child and right index to next element (second child)
		left = self.findChild(parent)
		right = left + 1

		#if there is a next array, compare itself to its children. if it is greater than either of them, switch 
		if c.next:
			#if left is larger switch left and parent
			if c.next.data[left] < c.data[parent] and c.next.data[left] != 0 :
				temp = c.data[parent]
				c.data[parent] = c.next.data[left]
				c.next.data[left] = temp
				c = c.getNext()
				self.deleteSort(left, c)
			#if right is larger, switch right and parent
			elif c.next.data[right] < c.data[parent] and c.next.data[right] != 0:
				temp = c.data[parent]
				c.data[parent] = c.next.data[right]
				c.next.data[right] = temp
				c = c.getNext()
				self.deleteSort(right, c)
				return
		#if were at the last array, it has no child, so stop
		elif c is self.end:
			return
		#if nothing worked, just exit
		else:
			return

	#delete the minimum element 
	def deleteMin(self, start, end):
		#set min to the min element
		min = self.findMin()
	
		#if there are no arrays raise an error
		if self.isEmpty():
			raise Exception("empty")
        
		#if there is only one array, remove the only  element then delete the array
		elif start is end:
			end.data[0] = 0
			end.size -= 1
			self.arrayLength -= 1
			start = None
			end = None
			return min
		#otherwise, move the first element to the front of the array and delete its spot at the end of the queue then resort the queue
		else:
			start.data[0] = end.data[e.size -1]
			end.data[end.size-1] = 0
			end.size  -= 1
			self.arrayLength -= 1
			self.deleteSort(0, start)
	
		#if there is no longer any elements in the last array, delete the array and set end to the previous array
		if end.size == 0:
			self.end = end.getPrev()
	
		#return the min element from findMin()
		return min

	#adds the node to the end of the linkedlist of arrays
	def appendArray(self, val):
		
		#create an node with ann array of size val
		nptr = Node(val)
		
		#increase the size of the linked list
		self.size += 1
		
		#if start is empty, put the array there
		if self.isEmpty():
			self.start = nptr
			self.end = self.start
			self.arrayLength = 1
		
		#otherwise, put the array at the end of the list and double arraylength
		else:
			self.arrayLength *= 2
			self.end.next = nptr
			nptr.prev = self.end
			self.end = nptr
    
	#display the arrays
	def display(self):
		if self.size == 0:
			print ("empty")
			return
		
		if self.isEmpty():
			return
		
		if self.start.next is None:
			print(self.start.data)
			return
		
		ptr = self.start
		
		while ptr:
			print (ptr.data)
			ptr = ptr.getNext()
			print ("\n")

#test for the program
ll = LinkedArray()
for i in range(1, 50):
	if i % 2 == 0:
		ll.insert(i/2)
	else:
		ll.insert(i)

#for i in range (0, 49):
#    ll.deleteMin(ll.start, ll.end)

ll.display()
