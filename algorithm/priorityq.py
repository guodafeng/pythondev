class MinHeap():
    __data = []
    __size = 0
    def push(self, val):
        self.__data.append(val)
        self.__size += 1
        self.__ascend()
        return

    def size(self):
        return self.__size

    def pop(self):
        temp = self.__data[0]
        self.__data[0] = self.__data[self.__size-1]
        self.__data.pop()
        self.__size -= 1
        self.__descend()
        return temp

    def p(self):
        print(self.__data)

    def __parent(self, index):
        return (index - 1) // 2


    def __descend(self):
        current = 0
        childLeft = current * 2 + 1 
        childRight = current * 2 + 2 
        while childLeft < self.__size:
            compareTo = childRight
            if childRight >= self.__size or self.__data[childLeft] < self.__data[childRight]:
                compareTo = childLeft
            if self.__data[current] > self.__data[compareTo]:
                self.__data[current] , self.__data[compareTo] = self.__data[compareTo], self.__data[current]
                current = compareTo
            else:
                break  # small than child
            childLeft = current * 2 + 1 
            childRight = current * 2 + 2 


    def __ascend(self):
        last = self.__size - 1
        parent = self.__parent(last)
        while self.__data[last] < self.__data[parent] and last > 0:
            self.__data[parent],self.__data[last] = self.__data[last],self.__data[parent]
            last = parent
            parent = self.__parent(last)


if __name__ == '__main__':
    mHeap = MinHeap()
    a = [11,24,45,22,14,89,8,19,45,67,88,28, 4, 2, 9, 3]

    for e in a:
        mHeap.push(e)
    for i in range(mHeap.size()):
        print(mHeap.pop())

    mHeap.p()





