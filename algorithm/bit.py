def insert(n, m, j, i):
    return n & (~0 << j | ~(~0 << i)) | m << i

def neighbor(num):
    return 

if __name__ == '__main__':
    m = 0b101010101010
    n = 0b111111111100001111100

    print(bin(insert(n, m, 16, 5)))
