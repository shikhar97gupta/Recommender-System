import random

def quicksort(arr1, arr2, start, stop):
    if(start < stop):
        pivotindex = partitionrand(arr1, arr2, start, stop)
        quicksort(arr1, arr2, start , pivotindex-1)
        quicksort(arr1, arr2, pivotindex + 1, stop)
        
def partitionrand(arr1, arr2, start, stop):
    randpivot = random.randrange(start, stop)
    arr1[start], arr1[randpivot] = arr1[randpivot], arr1[start]
    arr2[start], arr2[randpivot] = arr2[randpivot], arr2[start]
    return partition(arr1, arr2, start, stop)

def partition(arr1, arr2, start, stop):
    pivot = start
    i = start + 1
    for j in range(start + 1, stop + 1):
        if arr1[j] <= arr1[pivot]:
            arr1[i] , arr1[j] = arr1[j] , arr1[i]
            arr2[i] , arr2[j] = arr2[j] , arr2[i]
            i = i + 1
    arr1[pivot] , arr1[i - 1] = arr1[i - 1] , arr1[pivot]
    arr2[pivot] , arr2[i - 1] = arr2[i - 1] , arr2[pivot]
    pivot = i - 1
    return (pivot)