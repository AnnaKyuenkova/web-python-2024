def wrapper(f):
    def fun(l):
        return f(['+7 (' + n[-10:-7] + ') ' + n[-7:-4] + '-' + n[-4:-2] + '-' + n[-2:] for n in l])
    return fun

@wrapper
def sort_phone(l):
    return sorted(l)