def binarySearch(arr, low, high, elem):
    
    mid = low + (high-low)//2

    if (high-low==0):
        return mid
    
    if (high-low==1 and arr[mid+1]==elem):
        return mid+1

    if (arr[mid]==elem):
        return binarySearch(arr, low, mid, elem)
    elif (arr[mid]<elem):
        return binarySearch(arr, mid, high, elem)

#arr = [0,1,1]
#print(binarySearch(arr, 0, len(arr)-1, 1))
