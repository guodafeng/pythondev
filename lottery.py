class Player(object):
    ttt = 7
    def __init__(self, id, factor):
        self.id = id
        self.factor = factor

if __name__ == "__main__":
    p1 = Player(1,1);
    print(Player.ttt)
    print(p1.ttt)
    print("change p1")

    p1.ttt = 1
    print(Player.ttt)
    print(p1.ttt)


