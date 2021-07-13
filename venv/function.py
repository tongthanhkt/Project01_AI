import re


def isValid(X, component):  # kiem tra tinh dung dan cua input
    if len(X) > 10:
        return False
    return len(component[-1]) == max(len(component[0]), len(component[1])) or len(component[-1]) == max(len(component[0]), len(component[1])) + 1


def addConstraints(component, C, set_variable):  # them constraints
    for i in range(0, len(set_variable)-1):  # thiet lap AllDIff
        for j in range(i+1, len(set_variable)):
            C.append(f"{set_variable[i]} != {set_variable[j]}")
    x = len(component[0])
    y = len(component[1])
    z = len(component[2])
    C_index = 1
    for i in range(len(component[1]), 0, -1):  # thiet lap rang buoc giua cac bien
        x -= 1
        y -= 1
        z -= 1
        if z != 0:
            if C_index == 1:
                C.append(f"{component[0][x]} + {component[1][y]} = {component[2][z]} + C{C_index} * 10")
            else:
                C.append(f"{component[0][x]} + {component[1][y]} + C{C_index-1} = {component[2][z]} + C{C_index} * 10")
        else:
            if C_index == 1:
                C.append(f"{component[0][x]} + {component[1][y]} = {component[2][z]}")
            else:
                C.append(f"{component[0][x]} + {component[1][y]} + C{C_index-1} = {component[2][z]}")
        C_index += 1
    while z != 0:
        x -= 1
        z -= 1
        if x >= 0:
            if z > 0:
                C.append(f"{component[0][x]} + C{C_index-1} = {component[2][z]} + C{C_index} * 10")
            elif z == 0:
                C.append(f"{component[0][x]} + C{C_index-1} = {component[2][z]}")
        else:
            C.append(f"C{C_index-1} = {component[2][z]}")
        C_index += 1


def initCSP():  # mo phong CSP
    f = open("input.txt", "r")  #  doc file input
    add = False
    sub = False
    temp = f.read()
    f.close()
    for i in temp:  # kiem tra toan tu
        if i == '+':
            add = True
            break
        elif i == '-':
            sub = True
            break
    component = re.split('\+|\-|\=', temp)  # tien hanh tach input
    if sub:
        component[0], component[2] = component[2], component[0]
    if len(component[0]) < len(component[1]):
        component[0], component[1] = component[1], component[0]
    X = {}  # tao dictionary luu variable and domain
    set_variable = []  # tao list chi luu variable
    C = []  # tao list luu cac constraints
    for element in component:
        for index in range(0, len(element)):
            if element[index] not in X and index != 0:  # neu chua co trong variable va khong dung dau
                X[element[index]] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                set_variable.append(element[index])
            elif element[index] not in X and index == 0:  # neu chua co trong variable va dung dau
                X[element[index]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                set_variable.append(element[index])
    if not isValid(X, component):
        return "NO SOLUTION", "NO SOLUTION"
    for i in range(0, len(component[-1])-1):  # cac bien carry
        X[f"C{i+1}"] = [0,1]
    addConstraints(component, C, set_variable)
    return X, C


def test():  # ham nay chua dung den, no dung de thay bien vao bieu thuc
    x = 100
    str = "x == 100"
    return eval(str)