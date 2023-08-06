def binarySearch(array, element, start, end):
    if start > end:
        return -1

    mid = (start + end) // 2
    if element == array[mid]:
        return mid

    if element < array[mid]:
        return binarySearch(array, element, start, mid-1)
    else:
        return binarySearch(array, element, mid+1, end)
