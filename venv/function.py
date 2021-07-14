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
                C.append(f"{component[0][x]} + {component[1][y]} == {component[2][z]} + C{C_index} * 10")
            else:
                C.append(f"{component[0][x]} + {component[1][y]} + C{C_index-1} == {component[2][z]} + C{C_index} * 10")
        else:
            if C_index == 1:
                C.append(f"{component[0][x]} + {component[1][y]} == {component[2][z]}")
            else:
                C.append(f"{component[0][x]} + {component[1][y]} + C{C_index-1} == {component[2][z]}")
        C_index += 1
    while z != 0:
        x -= 1
        z -= 1
        if x >= 0:
            if z > 0:
                C.append(f"{component[0][x]} + C{C_index-1} == {component[2][z]} + C{C_index} * 10")
            elif z == 0:
                C.append(f"{component[0][x]} + C{C_index-1} == {component[2][z]}")
        else:
            C.append(f"C{C_index-1} == {component[2][z]}")
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
    for i in range(0,3):  # them vao cac phan tu dau truoc
        if component[i][0] not in X:
            X[component[i][0]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            set_variable.append(component[i][0])
    for element in component:
        for index in range(0, len(element)):
            if element[index] not in X and index != 0:  # neu chua co trong variable va khong dung dau
                X[element[index]] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                set_variable.append(element[index])
    if not isValid(X, component):
        return "NO SOLUTION", "NO SOLUTION"
    addConstraints(component, C, set_variable)
    for i in range(0, len(component[-1])-1):  # cac bien carry
        X[f"C{i+1}"] = [0,1]
        set_variable.append(f"C{i+1}")
    return set_variable, X, C


def chooseVariable(PQ, assignment, X, C):  # chon bien de gan gia tri
    key = ""  # ket qua
    if len(PQ) == 0:  # neu PQ = 0, tuc la dang o buoc dau tien
        var = {}  # luu bien co so lan xuat hien nhieu nhat trong C
        for element in X:  # duyet tat ca cac bien
            if element in assignment:
                continue
            count = 0  # bien dem so lan xuat hien
            for constraints in C:  # duyet cac constrain
                if element in constraints and "!=" not in constraints:  # neu bien do nam trong constraint
                    count += 1
            if len(var) == 0:  # neu var = 0 thi ta them ngay vao var
                var[element] = count
            else:  # neu da co phan tu trong var
                lst = list(var.values())  # lay gia tri cua phan tu do
                if count > int(lst[0]):  # so sanh xem bien nao xuat hien nhieu hon
                    var.clear()
                    var[element] = count
        key = list(var.keys())
        key = key[0]  # thu duoc bien se gan gia tri
    else:  # neu PQ da co thi ta lay phan tu dau tien trong PQ
        key = PQ.pop(0)
    for constraints in C:  # xet cac constraint
        if key in constraints and "!=" not in constraints:  # neu key nam trong constraint
            temp = constraints.split()  # tach constraint boi khoang trang
            for element in temp:  # cac phan tu trong constraint
                if element not in assignment:  # xet cac phan tu chua duoc gan
                    if element.isalpha() and element not in PQ and element != key:  # truong hop bien chua nam trong PQ va khac key
                        PQ.append(element)
                    elif not element.isalpha() and "C" in element and element not in PQ and element != key:  # truong hop bien carry
                        PQ.append(element)
    return key


def checkConsistent(assignment, X, C):  # kiem tra tinh dung dan
    for constraints in C:  # xet cac constraint
        arr = []
        for element in assignment:  # duyet qua cac bien da gan gia tri
            if element in constraints:  # neu bien do trong constraint
                arr.append(True)
        count = 0
        for element in X:  # duyet qua cac bien trong tat ca cac bien
            if element in constraints:
                count += 1
        if len(arr) == count:  # neu constraint da co day du bien
            if not eval(constraints, {}, assignment):  # vi pham dieu kien
                return False
    return True


def backtrackingSearch(PQ, assignment, X, C):  # duyet qua tat ca cac truong hop
    if len(assignment) == len(X):  # truong hop tim ra loi giai
        return True
    var = chooseVariable(PQ, assignment, X, C)  # chon bien de gan gia tri
    for element in X[var]:
        assignment[var] = element  # gan gia tri cho bien
        if checkConsistent(assignment, X, C):  # kiem tra tinh dung dan
            result = backtrackingSearch(PQ, assignment, X, C)  # neu dung thi tiep tuc gan bien khac
            if result:  # neu co ket qua thi tra ve ngay
                return True
    assignment.popitem()  # truong hop khong co thi quay lui
    PQ.insert(0, var)
    return False


def writeOutput(assignment, flag):  # ghi ket qua vao file output.txt
    f = open("output.txt", "w")
    if flag:
        assignment = dict(sorted(assignment.items()))
        for element in assignment:
            if len(element) == 1:
                f.write(str(assignment[element]))
                f.write("")
    else:
        f.write("NO SOLUTION")
    f.close()