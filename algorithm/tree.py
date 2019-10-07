
class Node:
    def __init__(self, parent = None, data = None):
        self.parentNode = parent
        self.childrenNodes = []
        self.data = data
        self.tag = None
        self.setParentListener = []
        self.appendChildListener = []
        self.removeChildListener = []

    def swapNode(self, targetNode):
        if not type(targetNode) is Node and targetNode is not None:
            raise TypeError("Not Node type")
        self.swapNodeData(targetNode)

        temp_parentNode = targetNode.parentNode
        temp_childrenNodes = targetNode.childrenNodes
        temp_setParentListener = targetNode.setParentListener
        temp_appendChildListener = targetNode.appendChildListener
        temp_removeChildListener = targetNode.removeChildListener

        targetNode.parentNode = self.parentNode
        targetNode.childrenNodes = self.childrenNodes
        targetNode.setParentListener = self.setParentListener
        targetNode.appendChildListener = self.appendChildListener
        targetNode.removeChildListener = self.removeChildListener

        self.parentNode = temp_parentNode
        self.childrenNodes = temp_childrenNodes
        self.setParentListener = temp_setParentListener
        self.appendChildListener = temp_appendChildListener
        self.removeChildListener = temp_removeChildListener
        for childNode in self.childrenNodes:
            childNode.setParent(self)
        for childNode in targetNode.childrenNodes:
            childNode.setParent(targetNode)

    def swapNodeData(self, targetNode):
        if not type(targetNode) is Node and targetNode is not None:
            raise TypeError("Not Node type")
        temp_data = targetNode.data
        temp_tag = targetNode.tag

        targetNode.data = self.data
        targetNode.tag = self.tag

        self.data = temp_data
        self.tag = temp_tag


    def addSetParentListener(self, callback):
        assert callable(callback), "The callback must be a callable object!"
        self.setParentListener.append(callback)

    def removeSetParentListener(self, callback):
        assert callable(callback), "The callback must be a callable object!"
        self.setParentListener.remove(callback)

    def addAppendChildListener(self, callback):
        assert callable(callback), "The callback must be a callable object!"
        self.appendChildListener.append(callback)

    def removeAppendChildListener(self, callback):
        assert callable(callback), "The callback must be a callable object!"
        self.appendChildListener.remove(callback)

    def addRemoveChildListener(self, callback):
        assert callable(callback), "The callback must be a callable object!"
        self.removeChildListener.append(callback)

    def removeRemoveChildListener(self, callback):
        assert callable(callback), "The callback must be a callable object!"
        self.removeChildListener.remove(callback)

    def getData(self):
        return self.data

    def getTag(self):
        return self.tag

    def getParent(self):
        return self.parentNode
    
    def getChildAt(self, idx):
        return self.childrenNodes[idx]

    def getChildrenCount(self):
        return len(self.childrenNodes)

    def setData(self, data):
        self.data = data

    def setTag(self, tag):
        self.tag = tag

    def setParent(self, node):
        if not type(node) is Node and node is not None:
            raise TypeError("Not Node type")
        self.parentNode = node
        for callback in self.setParentListener:
            callback(self, node)

    def appendChildNode(self, node):
        if not type(node) is Node:
            raise TypeError("Not Node type")
        self.childrenNodes.append(node)
        for callback in self.appendChildListener:
            callback(self, node)

    def appendChildNodes(self, nodes):
        if not type(nodes) is list:
            raise TypeError("Required list of child nodes")
        self.childrenNodes += nodes
        for node in nodes:
            for callback in self.appendChildListener:
                callback(self, node)
    
    def insertChildNode(self, node, idx=-1):
        if not type(node) is Node:
            raise TypeError("Not Node type")
        elif not type(idx) is int:
            raise TypeError("index must be an integer")
        self.childrenNodes.insert(node, idx)
        for callback in self.appendChildListener:
            callback(self, node)

    def removeChildNode(self, node):
        if not type(node) is Node:
            raise TypeError("Not Node type")
        if node in self.childrenNodes:
            self.childrenNodes.remove(node)
        for callback in self.removeChildListener:
            callback(self, node)

    def removeChildNodeAt(self, idx):
        if not type(idx) is int:
            raise TypeError("index must be an integer")
        node = self.childrenNodes[idx]
        for callback in self.removeChildListener:
            callback(self, node)
        del self.childrenNodes[idx]

    def hasChildNode(self, node):
        if not type(node) is Node:
            raise TypeError("Not Node type")
        return node in self.childrenNodes

class BasicTree:
    def __init__(self):
        self.rootNode = None
        self.level = -1
        self.orderList = ["pre-order", "in-order", "post-order", "level-order"]
        self.nodeCount = 0

    def getRootNode(self):
        return self.rootNode
    
    def getLevel(self):
        return self.level

    def getNodeCount(self):
        return self.nodeCount

    def getNodeCountAtLevel(self, level):
        return len(self.getNodesAtLevel(level))

    def getNodesAtLevel(self, level):
        if level < 0:
            level = self.level + level + 1
        if level == 0 and self.rootNode is not None:
            return [self.rootNode]
        assert level > 0 and level <= self.level, "Out of bounds!"
        
        currentLevel = 1
        targetNodes = self.rootNode.childrenNodes
        while currentLevel < level:
            newNodes = []
            for node in targetNodes:
                newNodes += node.childrenNodes
            targetNodes = newNodes
            currentLevel += 1
        return targetNodes

    def insert(self, data, level=-1, parentIdx=-1):
        node = Node(data=data)
        if self.rootNode is None:
            self.rootNode = node
            self.level = 0
            self.nodeCount += 1
            return
        
        assert(level != 0, "The level cannot be zero. Because this tree can only have one root node.")
        if self.level == 0:
            self.rootNode.appendChildNode(node)
            node.setParent(self.rootNode)
            self.level += 1
            self.nodeCount += 1
            return
        
        if (level < 0 and self.level + level + 1 > self.level) \
            or (level > 0 and level > self.level):
            targetLevelLayer = self.getNodesAtLevel(self.level)
            rootNode = targetLevelLayer[0]
            rootNode.appendChildNode(node)
            node.setParent(rootNode)
            self.level += 1
        else:
            rootNode = self.getNodesAtLevel(level - 1)[parentIdx]
            rootNode.appendChildNode(node)
            node.setParent(rootNode)
        self.nodeCount += 1

    def removeNode(self, node : Node):
        if node is self.rootNode:
            if self.rootNode.getChildrenCount() == 0:
                self.rootNode = None
                self.nodeCount -= 1
                return
            
            newRootNode = self.rootNode.getChildAt(0)
            self.rootNode.removeChildNode(newRootNode)
            newRootNode.appendChildNodes(self.rootNode.childrenNodes)
            for childNode in self.rootNode.childrenNodes:
                childNode.setParent(newRootNode)
            self.rootNode = newRootNode
            self.nodeCount -= 1
        else:
            foundNode = self.searchNode(lambda n: n is node)
            if foundNode is None:
                return
            parentNode = foundNode.getParent()
            parentNode.removeChildNode(foundNode)
            parentNode.appendChildNodes(foundNode.childrenNodes)
            for childNode in foundNode.childrenNodes:
                childNode.setParent(parentNode)
            self.nodeCount -= 1

    def searchNode(self, callback, order="pre-order"):
        assert callable(callback), "callback must be a callable function!"
        assert order in self.orderList, "Undefined order type!"
        if self.orderList.index(order) == 0: # pre-order
            return self.preOrderSearch(callback, self.rootNode)
        elif self.orderList.index(order) == 1: # in-order
            return self.inOrderSearch(callback, self.rootNode)
        elif self.orderList.index(order) == 2: # post-order
            return self.postOrderSearch(callback, self.rootNode)
        elif self.orderList.index(order) == 3: # level-order
            return self.levelOrderSearch(callback, self.rootNode)
        return None
    
    def preOrderSearch(self, callback, node):
        found = callback(node)
        if found == True:
            return node
        for childNode in node.childrenNodes:
            foundNode = self.preOrderSearch(callback, childNode)
            if foundNode is not None:
                return foundNode
        return None
    
    def inOrderSearch(self, callback, node):
        count = node.getChildrenCount()
        if count == 0:
            found = callback(node)
            if found == True:
                return node
            return None

        middleIdx = int(round(count / 2))
        for childNode in node.childrenNodes[:middleIdx]:
            foundNode = self.inOrderSearch(callback, childNode)
            if foundNode is not None:
                return foundNode
            
        found = callback(node)
        if found == True:
            return node

        for childNode in node.childrenNodes[middleIdx:]:
            foundNode = self.inOrderSearch(callback, childNode)
            if foundNode is not None:
                return foundNode
        return None
    
    def postOrderSearch(self, callback, node):
        for childNode in node.childrenNodes:
            foundNode = self.postOrderSearch(callback, childNode)
            if foundNode is not None:
                return foundNode
        found = callback(node)
        if found == True:
            return node
        return None

    def levelOrderSearch(self, callback, node):
        level = -1
        for i in range(0, self.level + 1):
            if node in self.getNodesAtLevel(i):
                level = i
                break
        assert level >= 0, "Not found provided node!"

        found = callback(node)
        if found == True:
            return node
        level += 1
        targetNodes = node.childrenNodes
        while level <= self.level:
            newNodes = []
            for node in targetNodes:
                found = callback(node)
                if found == True:
                    return node
                newNodes += node.childrenNodes
            targetNodes = newNodes
            level += 1

        return None

    def printTree(self):
        for x in self._computeTreeCoordinates():
            drawingX = 0
            relationString = ""
            dataString = ""
            prevX = 0
            prevParent = None
            for node in x["nodes"]:
                data = node["node"].getData()
                if x["level"] == 0:
                    relationString = "Printing Tree_"
                    dataString = str(data)
                    break

                while drawingX < node["x"] * 8:
                    if prevParent is node["parent"]:
                        relationString += "-"
                    else:
                        relationString += " "
                    if node["x"] * 8 - drawingX < 6:
                        dataString += " "
                    drawingX += 1

                increased = node["x"] - prevX - 1
                prevX = node["x"]
                while increased > 0:
                    if prevParent is node["parent"]:
                        relationString += "-"
                    else:
                        relationString += " "
                    dataString += "         "
                    increased -= 1
                relationString += "|"
                if data is None:
                    dataString += "x   "
                else:
                    dataString += "{0:<4d}".format(data)
                prevParent = node["parent"]
            print(relationString)
            print(dataString)

    def _computeTreeCoordinates(self, node=None, nodeInfoList=None, level=0):
        if level == 0:
            if self.rootNode is None:
                return None
            nodeInfoList = []
            for lv in range(0, self.level + 1):
                nodeInfoList.append(
                    {
                        "level": lv,
                        "next_x": 0,
                        "count": 0,
                        "nodes": []
                    }
                )
            nodeInfoList[0]["nodes"].append({
                "x": 0,
                "parent": None,
                "node": self.rootNode
            })
            currentInfo = nodeInfoList[level]
            for childNode in self.rootNode.childrenNodes:
                nodeInfoList = self._computeTreeCoordinates(childNode, nodeInfoList, level + 1)
                currentInfo["next_x"] += currentInfo["count"]
                currentInfo["count"] = 0
            return nodeInfoList
        
        if node.getChildrenCount() == 0:
            parentsInfo = nodeInfoList[level-1]
            currentInfo = nodeInfoList[level]
            currentInfo["nodes"].append({
                "x": parentsInfo["next_x"] + parentsInfo["count"],
                "parent": node.getParent(),
                "node": node
            })
            parentsInfo["count"] += 1
            return nodeInfoList
        else:
            currentInfo = nodeInfoList[level]
            parentsInfo = nodeInfoList[level-1]
            x = parentsInfo["next_x"]
            currentInfo["next_x"] = parentsInfo["next_x"]
            for childNode in node.childrenNodes:
                nodeInfoList = self._computeTreeCoordinates(childNode, nodeInfoList, level + 1)
                currentInfo["next_x"] += currentInfo["count"]
                currentInfo["count"] = 0
            parentsInfo["count"] += currentInfo["next_x"]
            currentInfo["nodes"].append({
                "x": x,
                "parent": node.getParent(),
                "node": node
            })
            return nodeInfoList

    def _computeFinalLevel(self):
        if self.rootNode is None:
            self.level = -1
            return
        currentLevel = 0
        targetNodes = self.rootNode.childrenNodes
        while len(targetNodes) > 0:
            targetNodes = [node.childrenNodes for node in targetNodes]
            currentLevel += 1
        self.level = currentLevel
        return


class BinaryTree(BasicTree):
    def insert(self, data):
        if self.rootNode is None:
            self.rootNode = Node(data=data)
            newNode = Node()
            self.rootNode.appendChildNode(newNode)
            newNode.setParent(self.rootNode)
            newNode = Node()
            self.rootNode.appendChildNode(newNode)
            newNode.setParent(self.rootNode)
            self.nodeCount += 1
            self.level = 1
            return
        
        node, level = self._findAppendableNode(self.rootNode, data)
        node.setData(data)
        newNode = Node()
        node.appendChildNode(newNode)
        newNode.setParent(node)
        newNode = Node()
        node.appendChildNode(newNode)
        newNode.setParent(node)
        self.nodeCount += 1
        if self.level < level + 1:
            self.level = level + 1

    def _findAppendableNode(self, node, data, level=0):
        leftNode = node.getChildAt(0)
        rightNode = node.getChildAt(1)
        if data < node.getData():
            if leftNode.getData() is None:
                return leftNode, level + 1
            else:
                return self._findAppendableNode(leftNode, data, level + 1)
        else:
            if rightNode.getData() is None:
                return rightNode, level + 1
            else:
                return self._findAppendableNode(rightNode, data, level + 1)

    def removeNode(self, node : Node):
        targetNode = self.searchNode(lambda n: n is node)
        if targetNode is None:
            return
        
        leftNode = targetNode.getChildAt(0)
        rightNode = targetNode.getChildAt(1)
        targetNode.childrenNodes.clear()
        appendableNode, _ = self._findAppendableNode(leftNode, rightNode.getData())
        
        parentNode = appendableNode.getParent()
        idx = parentNode.childrenNodes.index(appendableNode)
        del parentNode.childrenNodes[idx]
        parentNode.childrenNodes.insert(rightNode, idx)
        rightNode.setParent(parentNode)

        if targetNode is self.rootNode:
            self.rootNode = leftNode
            leftNode.setParent(None)
        else:
            parentNode = targetNode.getParent()
            idx = parentNode.childrenNodes.index(targetNode)
            del parentNode.childrenNodes[idx]
            parentNode.childrenNodes.insert(leftNode, idx)
            leftNode.setParent(targetNode.getParent())
        self.nodeCount -= 1
        self._computeFinalLevel()

    def searchNode(self, callback, order="in-order"):
        return super().searchNode(callback, order)

class MaxHeap:
    def __init__(self):
        self.heap = []

    def getNodeCount(self):
        return len(self.heap)
    
    def insert(self, data):
        self.heap.append(data)
        self._computeInsertion(len(self.heap) - 1)

    def _computeInsertion(self, index):
        if index <= 0:
            return
        parentIdx = int(index / 2 + 0.5) - 1
        if self.heap[parentIdx] < self.heap[index]:
            tempData = self.heap[parentIdx]
            self.heap[parentIdx] = self.heap[index]
            self.heap[index] = tempData
            self._computeInsertion(parentIdx)
    
    def removeNode(self):
        data = self.heap[0]
        self.heap.insert(0, self.heap[-1])
        del self.heap[1]
        del self.heap[-1]
        heapLength = len(self.heap)
        if heapLength == 0:
            return data
        self._computeRemoving(nodeCount=heapLength)
        return data

    def _computeRemoving(self, index=0, nodeCount=0):
        leftChildIdx = index * 2 + 1
        rightChildIdx = leftChildIdx + 1
        currentData = self.heap[index]

        if leftChildIdx >= nodeCount:
            return
        elif rightChildIdx >= nodeCount:
            targetIdx = leftChildIdx
            targetData = self.heap[leftChildIdx]
        else:
            leftData = self.heap[leftChildIdx]
            rightData = self.heap[rightChildIdx]
            targetIdx, targetData = (leftChildIdx, leftData) if leftData > rightData else (rightChildIdx, rightData)

        if targetData > currentData:
            self.heap[index] = targetData
            self.heap[targetIdx] = currentData
            self._computeRemoving(targetIdx, nodeCount)

class MinHeap:
    def __init__(self):
        self.heap = []
    
    def getNodeCount(self):
        return len(self.heap)

    def insert(self, data):
        self.heap.append(data)
        self._computeInsertion(len(self.heap) - 1)

    def _computeInsertion(self, index):
        if index <= 0:
            return
        parentIdx = int(index / 2 + 0.5) - 1
        if self.heap[parentIdx] > self.heap[index]:
            tempData = self.heap[parentIdx]
            self.heap[parentIdx] = self.heap[index]
            self.heap[index] = tempData
            self._computeInsertion(parentIdx)
    
    def removeNode(self):
        data = self.heap[0]
        self.heap.insert(0, self.heap[-1])
        del self.heap[1]
        del self.heap[-1]
        heapLength = len(self.heap)
        if heapLength == 0:
            return data
        self._computeRemoving(nodeCount=heapLength)
        return data

    def _computeRemoving(self, index=0, nodeCount=0):
        leftChildIdx = index * 2 + 1
        rightChildIdx = leftChildIdx + 1
        currentData = self.heap[index]

        if leftChildIdx >= nodeCount:
            return
        elif rightChildIdx >= nodeCount:
            targetIdx = leftChildIdx
            targetData = self.heap[leftChildIdx]
        else:
            leftData = self.heap[leftChildIdx]
            rightData = self.heap[rightChildIdx]
            targetIdx, targetData = (leftChildIdx, leftData) if leftData < rightData else (rightChildIdx, rightData)

        if targetData < currentData:
            self.heap[index] = targetData
            self.heap[targetIdx] = currentData
            self._computeRemoving(targetIdx, nodeCount)


"""
class Heap(BasicTree):
    def __init__(self, isMaxHeap=True):
        super().__init__()
        self.isMaxHeap = isMaxHeap

    def insert(self, data):
        if self.rootNode is None:
            self.rootNode = Node(data=data)
            self.nodeCount += 1
            self.level = 0
            return
        
        appendableMax = self.level * 2 if self.level >0 else 1
        finalLayerNodeCount = self.getNodeCountAtLevel(self.level)
        parentNode = None
        newNode = None
        if finalLayerNodeCount < appendableMax:
            prevLayer = self.getNodesAtLevel(self.level - 1)
            prevNodeIdx = int(finalLayerNodeCount / 2)
            parentNode = prevLayer[prevNodeIdx]
            newNode = Node(data=data)
            newNode.setParent(parentNode)
            parentNode.appendChildNode(newNode)
        else:
            parentNode = self.getNodesAtLevel(self.level)[0]
            newNode = Node(data=data)
            newNode.setParent(parentNode)
            parentNode.appendChildNode(newNode)
            self.level += 1
        self.nodeCount += 1
        
        while parentNode != None \
            and (parentNode.getData() < newNode.getData() if self.isMaxHeap \
                else parentNode.getData() > newNode.getData()):
            newNode.swapNodeData(parentNode)
            newNode = parentNode
            parentNode = parentNode.getParent()

    def removeNode(self):
        if self.nodeCount == 1:
            self.rootNode = None
            self.nodeCount -= 1
            return
        layer = self.getNodesAtLevel(self.level)
        layerLength = len(layer) - 1
        finalNode = layer[-1]
        self.rootNode.setData(finalNode.getData())
        parentNode = finalNode.getParent()
        parentNode.removeChildNode(finalNode)
        finalNode.setParent(None)
        if layerLength == 0:
            self.level -= 1
        
        targetNode = self.rootNode
        while targetNode.getChildrenCount() > 0:
            candidateNode = None
            for childNode in targetNode.childrenNodes:
                if (targetNode.getData() < childNode.getData() if self.isMaxHeap \
                    else targetNode.getData() > childNode.getData()):
                    if candidateNode is None:
                        candidateNode = childNode
                    elif self.isMaxHeap:
                        if candidateNode.getData() < childNode.getData():
                            candidateNode = childNode
                    else:
                        if candidateNode.getData() > childNode.getData():
                            candidateNode = childNode
            
            if candidateNode is None:
                break
            targetNode.swapNodeData(candidateNode)
            targetNode = candidateNode
        self.nodeCount -= 1

    def searchNode(self, callback, order="level-order"):
        return super().searchNode(callback, order)"""