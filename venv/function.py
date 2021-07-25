import re


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
                C.append(f"{component[0][x]} + {component[1][y]} - {component[2][z]} == C{C_index} * 10")
            else:
                C.append(f"{component[0][x]} + {component[1][y]} + C{C_index-1} - {component[2][z]} == C{C_index} * 10")
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
                C.append(f"{component[0][x]} + C{C_index-1} - {component[2][z]} == C{C_index} * 10")
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
    addConstraints(component, C, set_variable)
    for i in range(0, len(component[-1])-1):  # cac bien carry
        X[f"C{i+1}"] = []
        set_variable.append(f"C{i+1}")
    return set_variable, X, C


def chooseVariable(assignment, X, C):  # chon bien de gan gia tri (theo R.H.S)
    for constraints in C:  # duyet qua tung constrains
        if "!" in constraints:  # duyet cac constraints khong là allDiff
            continue
        lst = constraints.split()
        for element in lst:  # kiem tra cac gia tri trong constraints
            if element not in assignment and element in X and len(element) == 1:  # neu chua nam trong assignment
                return element


def findCarry(assignment, X, C):  # tim bien trong constraint
    countLoop = 0  # dem so lan thuc hien tim bien
    for constraints in C:  # duyet constraint
        if "!" in constraints:  # duyet cac constraints khong là allDiff
            continue
        lst = constraints.split(" == ")  # tach ra ve trai va ce phai constraint
        count = 0  # dem so luong bien trong assignment nam trong ve trai
        count1 = 0  # dem so luong bien trong assignment nam trong constraint
        count2 = 0  # dem so luong bien trong X nam trong ve trai
        for element in assignment:  # duyet qua cac bien da gan gia tri nam trong ve trai constraint
            if element in lst[0]:
                count += 1
        for element in assignment:  # duyet qua cac bien da gan nam trong constraint
            if element in constraints:
                count1 += 1
        for element in X:  # duyet qua cac bien nam ben ve trai constraint
            if element in lst[0]:
                count2 += 1
        if count == count1 and count == count2:  # neu thoa dieu kien thi tien hanh tim bien
            RHS = lst[1].split()
            value = eval(lst[0], {}, assignment)  # tinh gia tri ve trai
            if len(RHS[0]) != 1:  # neu bien trong ve phai la bien carry thi chia value cho 10
                value /= 10
            if value != int(value):  # neu value khong la so nguyen
                while countLoop != 0:  # thuc hien pop cac bien suy luan duoc va tra ve suy luan sai
                    countLoop -= 1
                    assignment.popitem()
                return -1
            else:
                if len(RHS[0]) == 1 and value in X[RHS[0]]:  # neu bien khong la carry thi phai nam trong mien gia tri
                    assignment[RHS[0]] = int(value)
                elif len(RHS[0]) != 1:  # neu la bien carry
                    assignment[RHS[0]] = int(value)
                else:  # nguoc lai tien hanh pop va tra ve that bai
                    while countLoop != 0:
                        countLoop -= 1
                        assignment.popitem()
                    return -1
            countLoop += 1
    return countLoop  # tra ve so luong bien suy luan duoc thanh cong


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


def backtrackingSearch(assignment, X, C):  # duyet qua tat ca cac truong hop
    countLoop = 0
    if len(assignment) == len(X):  # truong hop tim ra loi giai
        if checkConsistent(assignment, X, C):  # neu thoa dieu kien
            return True
        return False
    var = chooseVariable(assignment, X, C)  # chon bien de gan gia tri
    for element in X[var]:
        assignment[var] = element  # gan gia tri cho bien
        if checkConsistent(assignment, X, C):  # kiem tra tinh dung dan
            countLoop = findCarry(assignment, X, C)  # tien hanh suy luan bien
            if countLoop == -1:  # neu suy luan that bai thi tiep tuc loop
                continue
            result = backtrackingSearch(assignment, X, C)  # neu dung thi tiep tuc gan bien khac
            if result:  # neu co ket qua thi tra ve ngay
                return True
            while countLoop != 0:  # quay lui neu suy luan that bai va pop cac bien da suy luan duoc
                assignment.popitem()
                countLoop -= 1
    assignment.popitem()  # quay lui pop bien da gan truoc do
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
