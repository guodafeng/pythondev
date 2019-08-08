class Test(object):
    def __init__(self):
        self.name = 'abc'

    def __enter__(self):
        print("created")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("exit")

    def test(self):
        print(self.name)

print('before')
test = Test()
test.test()


print('after')

with Test() as tt:
    print("in with")
    print(tt.name)
    tt.test()

    print("in with")
        
    
