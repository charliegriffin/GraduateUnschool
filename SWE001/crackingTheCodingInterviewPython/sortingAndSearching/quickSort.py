import numpy as np
# quick sort algorithm
# sorts by choosing a random element, then partitioning, and continuing to swap

def quickSort(list):
    quickSortHelper(list,0,len(list)-1)
    return list
    
def quickSortHelper(list,first,last): '''same base case as merge sort'''
    if first<last:
        splitpoint = partition(list,first,last)
        ''' rightmark is the splitpoint, now we divide and repeat recursively'''
        quickSortHelper(list, first, splitpoint-1)
        quickSortHelper(list, splitpoint+1, last)

def partition(list,first,last):
    pivotvalue = list[first]
    leftmark = first + 1
    rightmark = last
    done = False
    while not done:
        while leftmark <= rightmark and list[leftmark] <= pivotvalue:
            leftmark = leftmark + 1 # inc leftmark until bigger than pivot
        while list[rightmark] >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark - 1 # dec rightmark until smaller than pivot
        if rightmark < leftmark:
            done = True
        else:                         # exchange
            temp = list[leftmark]
            list[leftmark] = list[rightmark]
            list[rightmark] = temp
    temp = list[first] 
    list[first] = list[rightmark]
    list[rightmark] = temp
    
    return rightmark
    
def quickSortTest():
    randList = [np.random.randint(0,100) for i in xrange(10)]
    print '\nunsorted',randList,'\nsorted',quickSort(randList)
    randList = [np.random.randint(0,100) for i in xrange(100)]
    print '\nunsorted',randList,'\nsorted',quickSort(randList)
    randList = [np.random.randint(0,100) for i in xrange(1000)]
    print '\nunsorted',randList,'\nsorted',quickSort(randList)
    randList = [np.random.randint(0,1000000) for i in xrange(1000000)]
    print '\nunsorted',randList,'\nsorted',quickSort(randList)


quickSortTest()

''' wow, this is incredibly fast for large lists'''        