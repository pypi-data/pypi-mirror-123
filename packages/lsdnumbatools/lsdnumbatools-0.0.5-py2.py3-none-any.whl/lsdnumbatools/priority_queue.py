import numpy as np
import numba as nb
import math as m
from numba.experimental import jitclass

# Python3 code to implement Priority Queue
# using Singly Linked List
 
# Class to create new node which includes
# Node Data, and Node Priority

node_type = nb.deferred_type()

spec1 = [
    ("data", nb.int32),
    ("priority", nb.float64),
    ("next", node_type),

]

@jitclass(spec1)
class PriorityQueueNode:
     
  def __init__(self, value, pr):
       
    self.data = value
    self.priority = pr

node_type.define(PriorityQueueNode.class_type.instance_type)

spec2 = [
    ("front", node_type),
    ("nodata", nb.float64),
    ("greater_first", nb.boolean)

]
         
# Implementation of Priority Queue
@jitclass(spec2)
class PriorityQueue:
     
    def __init__(self, nodata = -9999, greater_first = True):
        self.front = PriorityQueueNode(-9999,nodata)
        self.nodata = nodata
        self.greater_first = greater_first
         
    # Method to check Priority Queue is Empty
    # or not if Empty then it will return True
    # Otherwise False
    def isEmpty(self):
         
        if(self.front.priority == nodata):
            return True
        else:
            return False
     
    # Method to add items in Priority Queue
    # According to their priority value
    def push(self, value, priority):
         
        # Condition check for checking Priority
        # Queue is empty or not
        if self.isEmpty() == True:
             
            # Creating a new node and assinging
            # it to class variable
            self.front = PriorityQueueNode(value,
                                           priority)
             
            # Returning 1 for successful execution
            return 1
             
        else:
            if(self.greater_first): 
                # Special condition check to see that
                # first node priority value
                if self.front.priority > priority:
                     
                    # Creating a new node
                    newNode = PriorityQueueNode(value,
                                                priority)
                     
                    # Updating the new node next value
                    newNode.next = self.front
                     
                    # Assigning it to self.front
                    self.front = newNode
                     
                    # Returning 1 for successful execution
                    return 1
                     
                else:
                     
                    # Traversing through Queue until it
                    # finds the next smaller priority node
                    temp = self.front
                     
                    while temp.next:
                         
                        # If same priority node found then current
                        # node will come after previous node
                        if priority <= temp.next.priority:
                            break
                         
                        temp = temp.next
                     
                    newNode = PriorityQueueNode(value,
                                                priority)
                    newNode.next = temp.next
                    temp.next = newNode
                     
                    # Returning 1 for successful execution
                    return 1
            else:
                # Special condition check to see that
                # first node priority value
                if self.front.priority < priority:
                     
                    # Creating a new node
                    newNode = PriorityQueueNode(value,
                                                priority)
                     
                    # Updating the new node next value
                    newNode.next = self.front
                     
                    # Assigning it to self.front
                    self.front = newNode
                     
                    # Returning 1 for successful execution
                    return 1
                     
                else:
                     
                    # Traversing through Queue until it
                    # finds the next smaller priority node
                    temp = self.front
                     
                    while temp.next:
                         
                        # If same priority node found then current
                        # node will come after previous node
                        if priority > temp.next.priority:
                            break
                         
                        temp = temp.next
                     
                    newNode = PriorityQueueNode(value,
                                                priority)
                    newNode.next = temp.next
                    temp.next = newNode
                     
                    # Returning 1 for successful execution
                    return 1
     
    # Method to remove high priority item
    # from the Priority Queue
    def pop(self):
         
        # Condition check for checking
        # Priority Queue is empty or not
        if self.isEmpty() == True:
            return
         
        else: 
             
            # Removing high priority node from
            # Priority Queue, and updating front
            # with next node
            self.front = self.front.next
            return 1
             
    # Method to return high priority node
    # value Not removing it
    def top(self):
         
        # Condition check for checking Priority
        # Queue is empty or not
        if self.isEmpty() == True:
            return
        else:
            return self.front
             
    # Method to Traverse through Priority
    # Queue
    def traverse(self):
         
        # Condition check for checking Priority
        # Queue is empty or not
        if self.isEmpty() == True:
            return
        else:
            temp = self.front
            while temp:
                # print(temp.data, end = " ")
                temp = temp.next
 