import random as r

def print_the_maze(lst):
    for E in lst:
        for e in E:
            if e == 1:
                print('🧱', end='')
            else:
                print('  ', end='')
        print()

def print_as_int(lst):
    for E in lst:
        for e in E:
            print(e, end=' ')
        print()

# NOTE Dim must be odd number
dim = 23

inner_dim = dim - 2
edge =  [1 for x in range(dim)]
test = []
test.append(edge)
for e in range(1,dim-1):
    if e % 2 == 0:
        test.append([1 if x % 2 == 0 else 0 for x in range(dim)])
    else:
        test.append([1] + [0 for x in range(1, dim -1 )] + [1])
test.append(edge)

def get_random_direction():
    rand = r.randint(0,3)
    if rand == 0:
        return (-1, 0)
    if rand == 1:
        return (0, 1)
    if rand == 2:
        return (1, 0)
    if rand == 3:
        return (0, -1)


def randomize_maze(list_of_list):
    for E in range(2,dim - 2):
        if E % 2 == 0:
            for e in range(2,dim - 2):
                if e % 2 == 0:
                    rnd = get_random_direction()
                    list_of_list[E+rnd[0]][e+rnd[1]] = 1
                else:
                    pass
    return list_of_list

def punch_hole(top_right, bottom_left, list_of_list):
    for E in range(top_right[0],bottom_left[0]):
        for e in range(top_right[1],bottom_left[1]):
            list_of_list[E][e] = 0
    return list_of_list

r_test = randomize_maze(test)
r_test = punch_hole((3,3),(8,8),r_test)
r_test = punch_hole((5,14),(16,18),r_test)
r_test = punch_hole((14,3),(18,8),r_test)

# print_as_int(r_test)
print_the_maze(r_test)