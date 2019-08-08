class Solution:
    def setZeroes(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: void Do not return anything, modify matrix in-place instead.
        """
        rowNum = len(matrix)
        colNum = len(matrix[0])
        firstRow0 = False
        firstCol0 = False

        # use first row and first colum to mark if the row/column is 0
        # first row and firs line use specific variable
        for i in range(rowNum): 
            for j in range(colNum):
                if matrix[i][j] == 0:
                    matrix[0][j] = 0
                    matrix[i][0] = 0
                    if i == 0:
                        firstRow0 = True
                    if j == 0:
                        firstCol0 = True

        # set row to 0
        for i in range(1, rowNum):
            if matrix[i][0] == 0:
                for j in range(1,colNum):
                    matrix[i][j] = 0


        # set col to 0
        for j in range(1,colNum):
            if matrix[0][j] == 0:
                for i in range(1,rowNum):
                    matrix[i][j] = 0

        if firstRow0:
            for j in range(0, colNum):
                matrix[0][j] = 0
        if firstCol0:
            for i in range(0, rowNum):
                matrix[i][0] = 0



        
