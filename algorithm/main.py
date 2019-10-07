import random
import sort
import timeit

def PrintNode(node):
    print(node.getData())
    return False

if __name__ == "__main__":
    processingCount = 10
    randomRange = 10000
    dataSize = 7500
    totalProcessingTime = 0
    showData = False
    sortMethos = [
        {
            "name": "Max Heap Sort",
            "callback": sort.maxHeapSort,
            "elapsed-time": 0,
            "summed-time": 0,
            "average-time": 0
        },
        {
            "name": "Min Heap Sort",
            "callback": sort.minHeapSort,
            "elapsed-time": 0,
            "summed-time": 0,
            "average-time": 0
        }
    ]
    """sortMethos = [
        {
            "name": "Merge Sort",
            "callback": sort.mergeSort,
            "elapsed-time": 0,
            "summed-time": 0,
            "average-time": 0
        },
        {
            "name": "Bubble Sort",
            "callback": sort.bubbleSort,
            "elapsed-time": 0,
            "summed-time": 0,
            "average-time": 0
        },
        {
            "name": "Selection Sort",
            "callback": sort.selectionSort,
            "elapsed-time": 0,
            "summed-time": 0,
            "average-time": 0
        },
        {
            "name": "Insertion Sort",
            "callback": sort.insertionSort,
            "elapsed-time": 0,
            "summed-time": 0,
            "average-time": 0
        },
        {
            "name": "Quick Sort",
            "callback": sort.quickSort,
            "elapsed-time": 0,
            "summed-time": 0,
            "average-time": 0
        },
        {
            "name": "Binary Sort",
            "callback": sort.binarySort,
            "elapsed-time": 0,
            "summed-time": 0,
            "average-time": 0
        },
        {
            "name": "Max Heap Sort",
            "callback": sort.maxHeapSort,
            "elapsed-time": 0,
            "summed-time": 0,
            "average-time": 0
        },
        {
            "name": "Min Heap Sort",
            "callback": sort.minHeapSort,
            "elapsed-time": 0,
            "summed-time": 0,
            "average-time": 0
        }
    ]"""
    
    for procCnt in range(0, processingCount):
        print("[%d] Generating random list..." % (procCnt + 1))
        randomList = []
        for i in range(0, dataSize):
            while True:
                x = random.randint(1, randomRange)
                if x not in randomList:
                    randomList.append(x)
                    break

        print("[%d] Processing..." % (procCnt + 1))
        if showData:
            print("Original List:\t", randomList)

        for sortInfo in sortMethos:
            begin = timeit.default_timer()
            result = sortInfo["callback"](randomList)
            elapsedTime = timeit.default_timer() - begin
            if showData:
                print("[{}] {}:\t".format((procCnt + 1), sortInfo["name"]), result)
            else:
                print("[{}] {}".format((procCnt + 1), sortInfo["name"]))
            print("[%d] Elapsed Time: %f ms" % ((procCnt + 1), (elapsedTime * 1000)))
            sortInfo["elapsed-time"] = elapsedTime
            sortInfo["summed-time"] += elapsedTime
            sortInfo["average-time"] = sortInfo["summed-time"] / (procCnt + 1)
            totalProcessingTime += elapsedTime

    print()
    print()
    print("=======================Result=======================")
    print("Total processing time: %.4f sec ( %f ms )" % (totalProcessingTime, (totalProcessingTime * 1000)))
    print("Processing Count: %d" % processingCount)
    print("Data Count: %d" % dataSize)
    print("Random Range: 1 ~ %d (No duplicates)" % randomRange)
    print("Ranking_")
    sortedResult = sorted(sortMethos, key=lambda info : info["average-time"])
    for i in range(0, len(sortedResult)):
        sortInfo = sortedResult[i]
        print("[{0}] - {1} : Final {2:f} ms, Average {3:f} ms"\
            .format((i + 1), sortInfo["name"], sortInfo["elapsed-time"] * 1000, sortInfo["average-time"] * 1000))
