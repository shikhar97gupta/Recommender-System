import random

def kthLargest(arr1, arr2, l, r, k):
    if (k > 0 and k <= r - l + 1):
        pos = randomPartition(arr1, arr2, l, r)
        if (pos - l == k - 1):
            return arr1[pos]
        if (pos - l > k - 1): 
            return kthLargest(arr1, arr2, l, pos - 1, k)
        return kthLargest(arr1, arr2, pos + 1, r, k - pos + l - 1)
    return 999999999999
 
def swap(arr, a, b):
    temp = arr[a]
    arr[a] = arr[b]
    arr[b] = temp
 
def partition(arr1, arr2, l, r):
    x = arr1[r]
    i = l
    for j in range(l, r):
        if (arr1[j] >= x):
            swap(arr1, i, j)
            swap(arr2, i ,j)
            i += 1
    swap(arr1, i, r)
    swap(arr2, i ,r)
    return i
    
def randomPartition(arr1, arr2, l, r):
    n = r - l + 1
    pivot = int(random.random() * n)
    swap(arr1, l + pivot, r)
    swap(arr2, l + pivot, r)
    return partition(arr1, arr2, l, r)