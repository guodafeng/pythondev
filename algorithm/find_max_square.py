def max_square(arr):
    row_num = len(arr)
    col_num = len(arr[0])

    prev_max = [0] * col_num
    cur_max =  [0] * col_num
    result = 0
    for row in arr:
        for col_index, elm in enumerate(row):
            if elm == 1:
                left = cur_max[col_index -1] if col_index > 0 else 0
                up = prev_max[col_index]
                left_up = prev_max[col_index -1] if col_index > 0 else 0

                cur_max[col_index] = min(left,up,left_up) + 1
                result = max(result, cur_max[col_index])
            else:
                cur_max[col_index] = 0
        prev_max = cur_max
        cur_max = [0] * col_num

    return result

def test():
    data1 = [ [1,1,0,0,0,0,0],
              [1,1,1,1,1,1,0],
              [1,1,1,1,0,1,0],
              [1,1,1,1,1,1,0],
              [1,1,0,1,1,0,1],
              [1,1,1,1,1,1,1]
              ]

    print(max_square(data1))

    data2 = [ [1,1,0,0,0,0,0],
              [1,1,1,1,1,1,0],
              [1,1,1,1,1,1,0],
              [1,1,1,1,1,1,0],
              [1,1,1,1,1,0,1],
              [1,1,0,1,1,1,1]
              ]

    print(max_square(data2))
test()


