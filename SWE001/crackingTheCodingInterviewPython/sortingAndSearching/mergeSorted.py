''' 11.1  You are given two sorted arrays, A and B, where A has
a large enough buffer at the end to hold B. Write a method to merge
B into A in sorted order.'''

def merge(a,b):
    '''takes two sorted lists and returns a single sorted list
    by comparing the elements one at a time'''
    if not a:
        return b
    if not b:
        return a
    if a[0] < b[0]:
        return [a[0]] + merge(a[1:],b)
    else:
        return [b[0]] + merge(a,b[1:])
        
def mergeTest():
    A = [1,3,5,7,9]
    B = [2,4,6,8,10]
    print merge(A,B)

mergeTest()
       