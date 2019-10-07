import copy
import tree
import random

def typeCheck(params):
    if not type(params) is list or len(params) == 0:
        raise TypeError
    return copy.deepcopy(params)

def mergeSort(params):
    params = typeCheck(params)
    return _doMergeSort(params)

def _doMergeSort(params):
    length = len(params)
    if length <= 1:
        return params

    center = int(round(length / 2))
    leftArray = _doMergeSort(params[0:center])
    rightArray = _doMergeSort(params[center:length])
    results = []
    
    while len(leftArray) > 0:
        if len(rightArray) > 0:
            if leftArray[0] < rightArray[0]:
                results.append(leftArray[0])
                del leftArray[0]
            else:
                results.append(rightArray[0])
                del rightArray[0]
        else:
            results.append(leftArray[0])
            del leftArray[0]
    
    while len(rightArray) > 0:
        results.append(rightArray[0])
        del rightArray[0]

    return results



def bubbleSort(params):
    params = typeCheck(params)
    length = len(params)
    targetIdx = 0
    while targetIdx < length - 1:
        for idx in range(1, length - targetIdx):
            idx *= -1
            if params[idx] < params[idx - 1]:
                temp = params[idx]
                params[idx] = params[idx - 1]
                params[idx - 1] = temp
        targetIdx += 1
    return params

def selectionSort(params):
    params = typeCheck(params)
    targetIdx = 0
    length = len(params)
    while targetIdx < length:
        minIdx = targetIdx
        minData = params[targetIdx]
        for i in range(targetIdx + 1, length):
            if minData > params[i]:
                minIdx = i
                minData = params[i]
        if minIdx != targetIdx:
            tempData = params[targetIdx]
            params[targetIdx] = params[minIdx]
            params[minIdx] = tempData
        targetIdx += 1
    return params

def insertionSort(params):
    params = typeCheck(params)
    targetIdx = 1
    length = len(params)
    while targetIdx < length:
        data = params[targetIdx]
        insertionIdx = targetIdx - 1
        while insertionIdx >= 0:
            if params[insertionIdx] < data:
                break
            insertionIdx -= 1
        insertionIdx += 1
        if insertionIdx != targetIdx:
            del params[targetIdx]
            params.insert(insertionIdx, data)
        targetIdx += 1
    return params

def quickSort(params):
    params = typeCheck(params)
    _doQuickSort(params, 0, len(params) - 1)
    return params

def _doQuickSort(params, left, right):
    if left >= right or left < 0:
        return
    pivot = _partition(params, left, right)
    _doQuickSort(params, left, pivot - 1)
    _doQuickSort(params, pivot + 1, right)


def _partition(params, left, right):
    pivot = right
    right -= 1
    pivotData = params[pivot]
    
    while left < pivot:

        while left < pivot:
            if params[left] > pivotData:
                break
            left += 1

        while right > left:
            if params[right] < pivotData:
                break
            right -= 1
        if left == pivot: # The pivot data is the biggest data
            return pivot
        elif left == right: # The left index is now new pivot!
            temp = params[left]
            params[left] = params[pivot]
            params[pivot] = temp
            return left
        elif params[left] > pivotData \
            and params[right] < pivotData: # Swap data
            temp = params[left]
            params[left] = params[right]
            params[right] = temp
        


def binarySort(params):
    params = typeCheck(params)
    results = []
    bTree = tree.BinaryTree()
    for data in params:
        bTree.insert(data)
    bTree.searchNode(lambda n : results.append(n.getData()) if n.getData() is not None else False)
    return results

def maxHeapSort(params):
    params = typeCheck(params)
    results = []

    heap = tree.MaxHeap()
    for data in params:
        heap.insert(data)
    while heap.getNodeCount() > 0:
        results.append(heap.removeNode())

    """heap = tree.Heap()
    for data in params:
        heap.insert(data)
    while heap.getNodeCount() > 0:
        node = heap.getRootNode()
        results.append(node.getData())
        heap.removeNode()"""

    return results

def minHeapSort(params):
    params = typeCheck(params)
    results = []

    heap = tree.MinHeap()
    for data in params:
        heap.insert(data)
    while heap.getNodeCount() > 0:
        results.append(heap.removeNode())

    """heap = tree.Heap(isMaxHeap=False)
    for data in params:
        heap.insert(data)
    while heap.getNodeCount() > 0:
        node = heap.getRootNode()
        results.append(node.getData())
        heap.removeNode()"""

    return results