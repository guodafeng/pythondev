class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        length = len(gas)
        start = 0
        while start < length:
            next_start = self.canComplete(start, gas, cost)
            if next_start == start:
                return start
            else:
                start = next_start
        return -1

    def canComplete(self, start, gas, cost):
        length = len(gas)
        gas_count = 0
        cost_count = 0
        for i in range(length):
            index = (i + start) % length
            gas_count += gas[index]
            cost_count += cost[index]
            if cost_count > gas_count:
                return i + start + 1

        return start

        
