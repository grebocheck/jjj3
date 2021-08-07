def fun(num):
    print(num*2)


def tok(num):
    print(num+13)


def jui(num):
    print(num**3)


f_list = [lambda num: fun(num), lambda num: tok(num), lambda num: jui(num)]


f_list[0](2)