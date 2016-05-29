import numpy as np

# merge sort for integers

def mergeSort(list):
    '''sorts the input list using merge sort'''
    if len(list) <= 1:
        return list
    mid = len(list)//2
    left = mergeSort(list[:mid])      # slice 1st half
    right = mergeSort(list[mid:])     # slice 2nd half
    return merge(left, right)
    
def merge(left,right):
    '''takes two sorted lists and returns a single sorted list
    by comparing the elements one at a time'''
    if not left:
        return right
    if not right:
        return left
    if left[0] < right[0]:
        return [left[0]] + merge(left[1:],right)
    return [right[0]] + merge(left, right[1:])
    
def mergeSortTest():
    randList = [np.random.randint(0,100) for i in xrange(10)]
    print '\nunsorted',randList,'\nsorted',mergeSort(randList)
    randList = [np.random.randint(0,100) for i in xrange(100)]
    print '\nunsorted',randList,'\nsorted',mergeSort(randList)


mergeSortTest()
    
''' hitting max recursion depth at 1000 makes this seem much less
useful than I originally thought. Maybe I'm missing something'''
