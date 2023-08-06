import heapq
import sys

class xminheap:
    def __init__(self, maxorder=2**30, data=None, sortkey=None, recoverkey=None, maxkey=None,debug=False):
        '''
            sortkey -- FN for sorting
            recoverkey -- assume sortkey is using a dict KEY, so recoverykey can be lambda x : dict[x]
            maxkey -- key for internal maxheap. convert the max to the min.
        '''
        self.__maxorder = maxorder if maxorder > 0 else 1
        self.__maxvalheap = []
        self.__maxvaldict = dict()
        self.__sortkey = sortkey or (lambda x:x)
        self.__recoverkey = recoverkey or (lambda x:x)
        self.__maxkey = maxkey 
        self.__debug = debug
        if data and type(data) is list :
            self.__heap = [self.__sortkey(i) for i in data]
            heapq.heapify(self.__heap)
        else :
            self.__heap = []

    def push(self, x):
        if len(self.__heap) < self.__maxorder  \
           or (not self.__maxkey)  \
           or (self.__maxkey and self.__sortkey(x) < self.__sortkey(self.__maxvaldict[self.__maxvalheap[0]])) :
            heapq.heappush(self.__heap, self.__sortkey(x))
            if self.__maxkey :
                heapq.heappush(self.__maxvalheap, self.__maxkey(x))
                self.__maxvaldict[self.__maxkey(x)] = x
                if self.__debug :
                    print("# {} inserted into heapq.".format(x), file=sys.stderr, flush=True )
        else :
            if self.__debug :
                print("# {} ignored as it's out of target range.".format(x), file=sys.stderr, flush=True )

    def getheap(self):
        return [self.__recoverkey(x) for x in self.__heap]

    def first(self):
        return self.__recoverkey(self.__heap[0]) if len(self.__heap) else None

    def firstNItems(self,n=2**30):
        return [self.__recoverkey(i) for i in heapq.nsmallest(n,self.__heap)]


if __name__ == "__main__":
    lst = [0,2,4,6,7,9,-1,-5,7,10,20]
    print("# top 5 minheap")
    print(lst)
    minh = xminheap(5,maxkey=lambda x:-x,)
    for i in lst :
        minh.push(i)
        print(minh.getheap())

    lst = [0,2,-2,-4,4,6,7,9,-1,-5,7,10,20]
    print("# from lst : ", lst)
    minh = xminheap(data=lst,maxorder=5)
    print(minh.getheap())
