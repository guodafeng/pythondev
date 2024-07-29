from googlesearch import search
import threading

def query(keyword):
    keyword = "Jede"

    for url in search(keyword):
        print(url)


n = 0

def add():
    global n
    for i in range(1000):
        n = n + 1
        print(f"add: {n}")

def sub():
    global n
    for i in range(1000):
        n = n - 1
        print(f"sub: {n}")

if __name__ == "__main__":
    t1 = threading.Thread(target=add)
    t2 = threading.Thread(target=sub)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("n的值为:", n)
