def reconstructQueue(people):
    # people.sort(key=lambda (h, k): (-h, k))
    people.sort(key=lambda h: (-h[0], h[1]))
    return people

    queue = []
    for p in people:
        queue.insert(p[1], p)
    return queue


a = [(7,1), (5,2),(9,7,),(5,0), (9, 5),(8,4)]

print(reconstructQueue(a))

