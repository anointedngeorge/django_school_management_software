

def dictKeyChecker(keys=[], data={}):
    flag = False
    for x in keys:
        if x in data:
            flag = True
    return flag