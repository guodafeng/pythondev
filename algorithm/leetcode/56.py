# Definition for an interval.
# class Interval:
#     def __init__(self, s=0, e=0):
#         self.start = s
#         self.end = e

class Solution:
    def merge(self, intervals):
        """
        :type intervals: List[Interval]
        :rtype: List[Interval]
        """
        ret = []
        for inter in sorted(intervals, key = lambda i:i.start):
            if len(ret) > 0 and inter.start <= ret[-1].end:
                ret[-1].end = max(ret[-1].end, inter.end)
            else:
                ret.append(inter)
        return ret


    def insert(self, intervals, newInterval):
        """
        :type intervals: List[Interval]
        :type newInterval: Interval
        :rtype: List[Interval]
        """
        return self.merge(intervals + [newInterval])



        
