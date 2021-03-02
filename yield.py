def my_range(n):
    values = []
    i = 0
    while i < n:
        values.append(i)
        i += 1
    return values

def my_range2(n):
    print('Hej')
    i = 0
    while i < n:
        yield i
        i += 1

def main():
     g = my_range2(3)
     print(next(g))
     print(next(g))
     print(next(g))
     print(next(g))


if __name__ == '__main__':
    main()
